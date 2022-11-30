from common.timing import timeit
from common.io import read_file_as_int_list
import typing


def adjacent(x: int, y: int) -> typing.Generator[typing.Tuple[int, int], None, None]:
    for x_d in [-1, 0, 1]:
        for y_d in [-1, 0, 1]:
            if x_d == y_d == 0:
                continue
            yield x + x_d, y + y_d


@timeit
def p1():
    coords = {}
    with open("./input.txt", "r") as file:
        for y, line in enumerate(file):
            for x, c in enumerate(line.strip()):
                coords[x, y] = int(c)

    flashes = 0
    for _ in range(100):
        to_flash = []
        for k, v in coords.items():
            coords[k] += 1
            if coords[k] > 9:
                to_flash.append(k)

        while to_flash:
            pt = to_flash.pop()
            if coords[pt] == 0:
                continue

            coords[pt] = 0
            flashes += 1

            for other in adjacent(*pt):
                if other in coords and coords[other] != 0:
                    coords[other] += 1
                    if coords[other] > 9:
                        to_flash.append(other)

    return flashes


@timeit
def p2():
    coords = {}
    with open("./input.txt", "r") as file:
        for y, line in enumerate(file):
            for x, c in enumerate(line.strip()):
                coords[x, y] = int(c)

    step = 0
    while True:
        step += 1
        to_flash = []
        for k, v in coords.items():
            coords[k] += 1
            if coords[k] > 9:
                to_flash.append(k)

        while to_flash:
            pt = to_flash.pop()
            if coords[pt] == 0:
                continue

            coords[pt] = 0

            for other in adjacent(*pt):
                if other in coords and coords[other] != 0:
                    coords[other] += 1
                    if coords[other] > 9:
                        to_flash.append(other)

        if all(val == 0 for val in coords.values()):
            break

    return step


if __name__ == "__main__":
    print("======p1=====")
    p1 = p1()
    print(p1)
    print("======p1=====")
    print("======p2=====")
    p2 = p2()
    print(p2)
    print("======p2=====")
