from collections import defaultdict
from enum import StrEnum, auto
from itertools import pairwise


class CaveItem(StrEnum):
    ROCK = auto()
    AIR = auto()
    SAND = auto()
    HOLE = auto()


CAVE = dict[tuple[int, int], CaveItem]
HOLE = (500, 0)


def parse_cave(filename: str) -> CAVE:
    cave = defaultdict(lambda: CaveItem.AIR)

    with open(filename) as file:
        for line in file:
            path = list(
                map(
                    lambda p: list(map(int, p.strip().split(","))),
                    line.strip().split("->"),
                )
            )
            path_pairs = pairwise(path)
            for (start_x, start_y), (end_x, end_y) in path_pairs:
                if start_x == end_x:
                    step = 1 if end_y > start_y else -1
                    for y in range(start_y, end_y + step, step):
                        cave[start_x, y] = CaveItem.ROCK
                elif start_y == end_y:
                    step = 1 if end_x > start_x else -1
                    for x in range(start_x, end_x + step, step):
                        cave[x, start_y] = CaveItem.ROCK
                else:
                    raise AssertionError(f"Cannot handle this path")

    cave[HOLE] = CaveItem.HOLE
    return cave


def print_cave(cave: CAVE, min_x: int, max_x: int, min_y: int, max_y: int) -> None:
    print()
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            item = cave[x, y]
            match item:
                case CaveItem.ROCK:
                    print("#", end="")
                case CaveItem.AIR:
                    print(".", end="")
                case CaveItem.SAND:
                    print("O", end="")
                case CaveItem.HOLE:
                    print("+", end="")
                case _:
                    ...
        print()


def cave_bounds(cave: CAVE) -> tuple[int, int, int, int]:
    keys = cave.keys()
    x_s = [x for x, _ in keys]
    min_x, max_x = min(x_s), max(x_s)
    y_s = [y for _, y in keys]
    min_y, max_y = min(y_s), max(y_s)
    return min_x, max_x, min_y, max_y


def is_blocked(cave: CAVE, x, y) -> bool:
    return cave[x, y] in [CaveItem.ROCK, CaveItem.SAND]


def drop_sand(cave: CAVE, min_x: int, max_x: int, max_y: int) -> (CAVE, bool):
    x, y = HOLE

    while True:
        y += 1

        if y > max_y:
            return cave, False

        if not is_blocked(cave, x, y):
            continue
        else:
            if not is_blocked(cave, x - 1, y):
                x -= 1
                if x < min_x:
                    return cave, False
                continue

            if not is_blocked(cave, x + 1, y):
                x += 1
                if x > max_x:
                    return cave, False
                continue

            cave[x, y - 1] = CaveItem.SAND
            break

    return cave, True


def solve_p1(filename: str):
    cave = parse_cave(filename)
    min_x, max_x, _, max_y = cave_bounds(cave)

    can_continue = True
    sand_dropped = -1
    while can_continue:
        sand_dropped += 1
        cave, can_continue = drop_sand(cave, min_x, max_x, max_y)
    return sand_dropped


if __name__ == "__main__":
    p1 = solve_p1("./input.txt")
    print(p1)
    assert p1 == 808
