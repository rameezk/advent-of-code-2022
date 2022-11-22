from common.timing import timeit
from common.io import read_file_as_int_list
from common.windowing import window
import typing


def count_increases(windows: typing.List) -> int:
    increases = 0
    for w in windows:
        try:
            n1, n2 = w
            if n2 > n1:
                increases += 1
        except ValueError:
            # Ignore unpacking error
            ...

    return increases


@timeit
def p1():
    data = read_file_as_int_list("./input.txt")
    windows = window(data)
    increases = count_increases(windows)
    print(increases)


@timeit
def p2():
    data = read_file_as_int_list("./input.txt")
    windows = window(data, size=3)
    sums = [sum(w) for w in windows]
    window_sums = window(sums)
    increases = count_increases(window_sums)
    print(increases)


if __name__ == "__main__":
    print("======p1=====")
    p1()
    print("======p1=====")
    print("======p2=====")
    p2()
    print("======p2=====")
