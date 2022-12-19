import multiprocessing
import re
from dataclasses import dataclass, replace, field
from functools import cache
from itertools import repeat
from math import ceil

from common.timing import timeit


@dataclass(kw_only=True, unsafe_hash=True)
class Blueprint:
    id_: int
    ore_robot_cost_in_ore: int
    clay_robot_cost_in_ore: int
    obsidian_robot_cost_in_ore: int
    obsidian_robot_cost_in_clay: int
    geode_robot_cost_in_ore: int
    geode_robot_cost_in_obsidian: int

    mined_ore: int = field(hash=True, default=0)
    mined_clay: int = field(hash=True, default=0)
    mined_obsidian: int = field(hash=True, default=0)

    number_of_ore_robots: int = field(hash=True, default=1)
    number_of_clay_robots: int = field(hash=True, default=0)
    number_of_obsidian_robots: int = field(hash=True, default=0)

    minutes_remaining: int = 24


def parse_blueprints(filename: str) -> list:
    blueprints = []
    with open(filename) as file:
        for line in file:
            sections = line.strip().split(".")
            blueprint_id, ore_robot_cost_in_ore = map(
                int, re.findall(r"\d+", sections[0])
            )
            clay_robot_cost_in_ore = int(re.findall(r"\d+", sections[1])[0])
            obsidian_robot_cost_in_ore, obsidian_robot_cost_in_clay = map(
                int, re.findall(r"\d+", sections[2])
            )
            geode_robot_cost_in_ore, geode_robot_cost_in_obsidian = map(
                int, re.findall(r"\d+", sections[3])
            )
            blueprint = Blueprint(
                id_=blueprint_id,
                ore_robot_cost_in_ore=ore_robot_cost_in_ore,
                clay_robot_cost_in_ore=clay_robot_cost_in_ore,
                obsidian_robot_cost_in_ore=obsidian_robot_cost_in_ore,
                obsidian_robot_cost_in_clay=obsidian_robot_cost_in_clay,
                geode_robot_cost_in_ore=geode_robot_cost_in_ore,
                geode_robot_cost_in_obsidian=geode_robot_cost_in_obsidian,
            )
            blueprints.append(blueprint)
    return blueprints


@cache
def solve(blueprint: Blueprint) -> int:
    if blueprint.minutes_remaining == 0:
        return 0

    if (
        blueprint.mined_ore >= blueprint.geode_robot_cost_in_ore
        and blueprint.mined_obsidian >= blueprint.geode_robot_cost_in_obsidian
    ):
        # We can afford to build a geode robot
        return (blueprint.minutes_remaining - 1) + solve(
            replace(
                blueprint,
                mined_ore=blueprint.mined_ore
                + blueprint.number_of_ore_robots
                - blueprint.geode_robot_cost_in_ore,
                mined_clay=blueprint.mined_clay + blueprint.number_of_clay_robots,
                mined_obsidian=blueprint.mined_obsidian
                + blueprint.number_of_obsidian_robots
                - blueprint.geode_robot_cost_in_obsidian,
                minutes_remaining=blueprint.minutes_remaining - 1,
            )
        )

    result = 0
    if blueprint.mined_ore >= blueprint.ore_robot_cost_in_ore:
        # build an ore robot
        result = max(
            result,
            solve(
                replace(
                    blueprint,
                    mined_ore=blueprint.mined_ore
                    + blueprint.number_of_ore_robots
                    - blueprint.ore_robot_cost_in_ore,
                    mined_clay=blueprint.mined_clay + blueprint.number_of_clay_robots,
                    mined_obsidian=blueprint.mined_obsidian
                    + blueprint.number_of_obsidian_robots,
                    number_of_ore_robots=blueprint.number_of_ore_robots + 1,
                    minutes_remaining=blueprint.minutes_remaining - 1,
                )
            ),
        )
    if blueprint.mined_ore >= blueprint.clay_robot_cost_in_ore:
        # build a clay robot
        result = max(
            result,
            solve(
                replace(
                    blueprint,
                    mined_ore=blueprint.mined_ore
                    + blueprint.number_of_ore_robots
                    - blueprint.clay_robot_cost_in_ore,
                    mined_clay=blueprint.mined_clay + blueprint.number_of_clay_robots,
                    mined_obsidian=blueprint.mined_obsidian
                    + blueprint.number_of_obsidian_robots,
                    number_of_clay_robots=blueprint.number_of_clay_robots + 1,
                    minutes_remaining=blueprint.minutes_remaining - 1,
                )
            ),
        )
    if (
        blueprint.mined_ore >= blueprint.obsidian_robot_cost_in_ore
        and blueprint.mined_clay >= blueprint.obsidian_robot_cost_in_clay
    ):
        # build an obsidian robot
        result = max(
            result,
            solve(
                replace(
                    blueprint,
                    mined_ore=blueprint.mined_ore
                    + blueprint.number_of_ore_robots
                    - blueprint.obsidian_robot_cost_in_ore,
                    mined_clay=blueprint.mined_clay
                    + blueprint.number_of_clay_robots
                    - blueprint.obsidian_robot_cost_in_clay,
                    mined_obsidian=blueprint.mined_obsidian
                    + blueprint.number_of_obsidian_robots,
                    number_of_obsidian_robots=blueprint.number_of_obsidian_robots + 1,
                    minutes_remaining=blueprint.minutes_remaining - 1,
                )
            ),
        )
    if (
        blueprint.mined_ore
        + blueprint.number_of_ore_robots
        - blueprint.ore_robot_cost_in_ore
        < max(
            blueprint.clay_robot_cost_in_ore,
            blueprint.obsidian_robot_cost_in_ore,
            blueprint.geode_robot_cost_in_ore,
        )
    ):
        result = max(
            result,
            solve(
                replace(
                    blueprint,
                    mined_ore=blueprint.mined_ore + blueprint.number_of_ore_robots,
                    mined_clay=blueprint.mined_clay + blueprint.number_of_clay_robots,
                    mined_obsidian=blueprint.mined_obsidian
                    + blueprint.number_of_obsidian_robots,
                    minutes_remaining=blueprint.minutes_remaining - 1,
                )
            ),
        )
    return result


def worker(blueprint: Blueprint, queue: multiprocessing.Queue):
    print(f"Starting computation of blueprint {blueprint.id_}")
    result = solve(blueprint)
    print(f"Completed computation of blueprint {blueprint.id_}")
    data = queue.get()
    data[blueprint.id_] = result
    queue.put(data)


@timeit
def solve_p1():
    blueprints = parse_blueprints("./input.txt")

    manager = multiprocessing.Manager()
    queue = manager.Queue()
    queue.put({})

    max_cpus = multiprocessing.cpu_count()

    with multiprocessing.Pool(max_cpus) as pool:
        chunksize = ceil(len(blueprints) / max_cpus)
        pool.starmap(worker, zip(blueprints, repeat(queue)), chunksize=chunksize)

    shared_results: dict = queue.get()
    total = 0
    for blueprint_id, geodes_mined in shared_results.items():
        total += blueprint_id * geodes_mined

    return total


if __name__ == "__main__":
    p1 = solve_p1()
    print(p1)
