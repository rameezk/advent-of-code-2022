import typing
from collections import defaultdict

from common.timing import timeit


def parse_input(filename: str):
    with open(filename, "r") as f:
        fishes = list(map(int, f.read().strip().split(",")))
    return fishes


def simulate(fishes: typing.List[int], days: int) -> int:
    born_at = defaultdict(lambda: 0)

    for fish in fishes:
        born_at[fish] += 1

    for day in range(days):
        born_at[day] = born_at[day] + born_at[day - (6 + 1)] + born_at[day - (8 + 1)]

    sum_ = sum(born_at.values()) + len(fishes)
    return sum_


@timeit
def p1():
    fishes = parse_input("./input.txt")
    sum_ = simulate(fishes, days=80)
    print(sum_)


@timeit
def p2():
    fishes = parse_input("./input.txt")
    sum_ = simulate(fishes, days=256)
    print(sum_)


if __name__ == "__main__":
    print("======p1=====")
    p1()
    print("======p1=====")
    print("======p2=====")
    p2()
    print("======p2=====")
