from common.timing import timeit


def print_points(points: set[tuple[int, int]]) -> None:
    max_x = max(x for x, _ in points)
    max_y = max(y for _, y in points)

    for y in range(0, max_y + 1):
        for x in range(0, max_x + 1):
            if (x, y) in points:
                print("█", end="")
            else:
                print(" ", end="")
        print()


@timeit
def p1():
    with open("./input.txt") as file:
        input_ = file.read()

    points_s: str
    instructions: str
    points_s, instructions = input_.split("\n\n")

    points = set()

    for line in points_s.splitlines():
        x_s, y_s = line.split(",")
        points.add((int(x_s), int(y_s)))

    for line in instructions.splitlines():
        instruction_s, f_s = line.split("=")

        axis = instruction_s[-1]
        f = int(f_s)

        if axis == "x":
            # vertical fold
            points = {(x if x > f else f - (x - f), y) for x, y in points}
        elif axis == "y":
            # horizontal fold
            points = {(x, y if y > f else f - (y - f)) for x, y in points}
        else:
            raise AssertionError(f"Unknown axis {axis}")
        break

    print(len(points))


@timeit
def p2():
    with open("./input.txt") as file:
        input_ = file.read()

    points_s: str
    instructions: str
    points_s, instructions = input_.split("\n\n")

    points = set()

    for line in points_s.splitlines():
        x_s, y_s = line.split(",")
        points.add((int(x_s), int(y_s)))

    for line in instructions.splitlines():
        instruction_s, f_s = line.split("=")

        axis = instruction_s[-1]
        f = int(f_s)

        if axis == "x":
            # vertical fold
            points = {(x if x < f else f - (x - f), y) for x, y in points}
        elif axis == "y":
            # horizontal fold
            points = {(x, y if y < f else f - (y - f)) for x, y in points}
        else:
            raise AssertionError(f"Unknown axis {axis}")

    print_points(points)


if __name__ == "__main__":
    print("======p1=====")
    p1()
    print("======p1=====")
    print("======p2=====")
    p2()
    print("======p2=====")
