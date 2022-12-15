import re

from common.timing import timeit


def manhattan_distance(x1: int, y1: int, x2: int, y2) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


def get_interval(x: int, y: int, distance: int, at_y: int) -> tuple[int, int] | None:
    d = abs(y - at_y)
    if d > distance:
        return None
    return x - (distance - d), x + (distance - d)


@timeit
def solve_p1():
    at_y = 2000000
    beacons = set()
    intervals = []

    with open("./input.txt") as file:
        for line in file:
            x_s, y_s, x_b, y_b = map(int, re.findall(r"-?\d+", line))
            d = manhattan_distance(x_s, y_s, x_b, y_b)
            beacons.add((x_b, y_b))

            interval = get_interval(x_s, y_s, d, at_y)
            if interval is not None:
                intervals.append(interval)

    b = set()
    for low, high in intervals:
        for j in range(low, high + 1):
            b.add((j, at_y))

    return len(b.difference(beacons))


if __name__ == "__main__":
    p1 = solve_p1()
    print(p1)
