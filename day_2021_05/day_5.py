import typing

from common.timing import timeit


def count_points(grid) -> int:
    count = 0
    for row in grid:
        for num in row:
            if num != "." and num >= 2:
                count += 1
    return count


def draw_on_grid(grid, path):
    for x, y in path:

        if len(grid) <= y:
            for r in range(len(grid), y + 1):
                grid.append([])

        row = grid[y]
        if len(row) <= x:
            for c in range(len(row), x + 1):
                row.append(".")

        point = grid[y][x]
        if point == ".":
            grid[y][x] = 1
        else:
            grid[y][x] += 1

    return grid


def calculate_path(x1, y1, x2, y2, ignore_diagonals: bool) -> typing.List:
    x_modifier = 1 if x2 >= x1 else -1
    y_modifier = 1 if y2 >= y1 else -1
    if x1 == x2:
        # vertical
        path = list(
            zip([x1] * (abs(y2 - y1) + 1), range(y1, y2 + y_modifier, y_modifier))
        )
    elif y1 == y2:
        # horizontal
        path = list(
            zip(range(x1, x2 + x_modifier, x_modifier), [y1] * (abs(x2 - x1) + 1))
        )
    else:
        # diagonal
        if ignore_diagonals:
            path = []
        else:
            path = list(
                zip(
                    range(x1, x2 + x_modifier, x_modifier),
                    range(y1, y2 + y_modifier, y_modifier),
                )
            )

    return path


@timeit
def p1():
    grid = []
    with open("./input.txt", "r") as f:
        for line in f:
            from_, to = [command.strip() for command in line.rstrip().split("->")]
            x1, y1 = list(map(int, from_.split(",")))
            x2, y2 = list(map(int, to.split(",")))
            path = calculate_path(x1, y1, x2, y2, ignore_diagonals=True)
            draw_on_grid(grid, path)
    print(count_points(grid))


@timeit
def p2():
    grid = []
    with open("./input.txt", "r") as f:
        for line in f:
            from_, to = [command.strip() for command in line.rstrip().split("->")]
            x1, y1 = list(map(int, from_.split(",")))
            x2, y2 = list(map(int, to.split(",")))
            path = calculate_path(x1, y1, x2, y2, ignore_diagonals=False)
            draw_on_grid(grid, path)
    print(count_points(grid))


if __name__ == "__main__":
    print("======p1=====")
    p1()
    print("======p1=====")
    print("======p2=====")
    p2()
    print("======p2=====")
