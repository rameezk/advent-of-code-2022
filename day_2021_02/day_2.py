from common.timing import timeit


@timeit
def p1():
    x = 0
    y = 0

    with open("./input.txt", "r") as f:
        for line in f:
            direction, by = line.split(" ")
            by = int(by)
            match direction:
                case "forward":
                    x += by
                case "down":
                    y += by
                case "up":
                    y -= by
                case _:
                    ...
        print(f"{x * y}")


@timeit
def p2():
    x = 0
    y = 0
    a = 0

    with open("./input.txt", "r") as f:
        for line in f:
            direction, by = line.split(" ")
            by = int(by)
            match direction:
                case "forward":
                    x += by
                    y += by * a
                case "down":
                    a += by
                case "up":
                    a -= by
                case _:
                    ...
        print(f"{x * y}")


if __name__ == "__main__":
    print("======p1=====")
    p1()
    print("======p1=====")
    print("======p2=====")
    p2()
    print("======p2=====")
