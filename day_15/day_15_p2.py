import re

from common.timing import timeit


def manhattan_distance(x1: int, y1: int, x2: int, y2) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


def get_interval(x: int, y: int, distance: int, at_y: int) -> tuple[int, int] | None:
    d = distance - abs(y - at_y)
    if d < 0:
        return None
    return x - d, x + d


@timeit
def solve_p2():

    lines = []
    with open("./input.txt") as file:
        for line in file:
            x_s, y_s, x_b, y_b = map(int, re.findall(r"-?\d+", line))
            lines.append((x_s, y_s, x_b, y_b))

    valid_area = 4000000
    for at_y in range(valid_area + 1):
        intervals = []

        for x_s, y_s, x_b, y_b in lines:
            d = manhattan_distance(x_s, y_s, x_b, y_b)
            interval = get_interval(x_s, y_s, d, at_y)
            if interval is not None:
                intervals.append(interval)

        intervals.sort()
        b = []
        for low, high in intervals:
            if not b:
                b.append([low, high])
                continue

            last_low, last_high = b[-1]

            if low > last_high + 1:
                b.append([low, high])
                continue

            b[-1][1] = max(last_high, high)

        x = 0
        for low, high in b:
            if x < low:
                return x * 4000000 + at_y
            x = max(x, high + 1)
            if x > valid_area:
                break


if __name__ == "__main__":
    p2 = solve_p2()
    print(p2)
