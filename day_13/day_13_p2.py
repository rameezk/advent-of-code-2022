import functools
from enum import IntEnum


class Status(IntEnum):
    RIGHT_ORDER = -1
    CONTINUE = 0
    WRONG_ORDER = 1


def check_numbers(x: int, y: int) -> Status:
    if x < y:
        return Status.RIGHT_ORDER

    if y < x:
        return Status.WRONG_ORDER

    return Status.CONTINUE


def check(x, y) -> Status:
    if isinstance(x, int) and isinstance(y, int):
        return check_numbers(x, y)
    elif isinstance(x, int):
        return check([x], y)
    elif isinstance(y, int):
        return check(x, [y])
    elif not len(x) and len(y):
        return Status.RIGHT_ORDER
    elif len(x) and not len(y):
        return Status.WRONG_ORDER
    elif not len(x) and not len(y):
        return Status.CONTINUE
    else:
        status = check(x[0], y[0])
        if status == Status.CONTINUE:
            return check(x[1:], y[1:])
        return status


def solve_p2(filename: str):
    with open(filename) as file:
        pairs = file.read().strip().split("\n\n")

    packets = [[[2]], [[6]]]
    for idx, pair in enumerate(pairs):
        part_1, part_2 = list(map(eval, pair.splitlines()))
        packets.append(part_1)
        packets.append(part_2)

    packets_sorted = sorted(packets, key=functools.cmp_to_key(check))
    distress_signal = (packets_sorted.index([[2]]) + 1) * (
        packets_sorted.index([[6]]) + 1
    )
    return distress_signal


if __name__ == "__main__":
    p2 = solve_p2("./input.txt")
    print(p2)
