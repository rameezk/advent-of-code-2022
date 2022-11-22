from common.timing import timeit
import typing


def calculate_cheapest_fuel(
    positions: typing.List, cost_calculator: typing.Callable
) -> int:
    max_position = max(positions)
    cheapest_fuel = None

    for possible_position in range(0, max_position + 1):
        fuel_cost_to_this_position = []

        for crab_position in positions:
            cost = cost_calculator(possible_position, crab_position)
            if cheapest_fuel is not None and cost >= cheapest_fuel:
                break
            fuel_cost_to_this_position.append(cost)

        this_pos_fuel = sum(fuel_cost_to_this_position)
        if cheapest_fuel is not None and this_pos_fuel >= cheapest_fuel:
            break
        else:
            cheapest_fuel = this_pos_fuel

    return cheapest_fuel


def cost_calculator_simple_movement(pos1: int, pos2: int) -> int:
    return abs(pos1 - pos2)


def cost_calculator_stepped_movement(pos1: int, pos2: int) -> int:
    steps = abs(pos1 - pos2)
    total = 1

    if steps == 1:
        return total

    for n in range(2, steps + 1):
        total += n

    return total


@timeit
def p1():
    with open("./input.txt", "r") as f:
        positions = list(map(int, f.read().strip().split(",")))

    cheapest_position = calculate_cheapest_fuel(
        positions, cost_calculator_simple_movement
    )
    print(cheapest_position)


@timeit
def p2():
    with open("./input.txt", "r") as f:
        positions = list(map(int, f.read().strip().split(",")))

    cheapest_position = calculate_cheapest_fuel(
        positions, cost_calculator_stepped_movement
    )
    print(cheapest_position)


if __name__ == "__main__":
    print("======p1=====")
    p1()
    print("======p1=====")
    print("======p2=====")
    p2()
    print("======p2=====")
