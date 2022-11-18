from common.timing import timeit
from common.io import read_file_as_int_list


@timeit
def p1():
    _ = read_file_as_int_list("./sample.txt")


@timeit
def p2():
    _ = read_file_as_int_list("./sample.txt")


if __name__ == "__main__":
    print("======p1=====")
    p1()
    print("======p1=====")
    print("======p2=====")
    p2()
    print("======p2=====")
