from common.timing import timeit
import typing


def get_top_path_heights(
    height_map: dict, coord: tuple[int, int]
) -> typing.Generator[int, None, None]:
    x, y = coord
    for y_d in range(y - 1, -1, -1):
        yield height_map[(x, y_d)]


def get_bottom_path_heights(
    height_map: dict, coord: tuple[int, int], max_y: int
) -> typing.Generator[int, None, None]:
    x, y = coord
    for y_d in range(y + 1, max_y + 1):
        yield height_map[(x, y_d)]


def get_right_path_heights(
    height_map: dict, coord: tuple[int, int], max_x: int
) -> typing.Generator[int, None, None]:
    x, y = coord
    for x_d in range(x + 1, max_x + 1):
        yield height_map[(x_d, y)]


def get_left_path_heights(
    height_map: dict, coord: tuple[int, int]
) -> typing.Generator[int, None, None]:
    x, y = coord
    for x_d in range(x - 1, -1, -1):
        yield height_map[(x_d, y)]


def is_tallest_tree_in_path(tree_height: int, path_heights: typing.Generator) -> bool:
    for path_height in path_heights:
        if tree_height <= path_height:
            return False
    return True


def is_edge(coord: tuple[int, int], max_x: int, max_y: int) -> bool:
    x, y = coord
    return x == 0 or y == 0 or x == max_x or y == max_y


def get_height_map(filename: str) -> dict:
    height_map = {}
    with open(filename) as file:
        for y, line in enumerate(file):
            for x, c in enumerate(line.strip()):
                height_map[x, y] = int(c)
    return height_map


@timeit
def solve_p1():
    height_map = get_height_map("./input.txt")

    max_x, max_y = max([k for k in height_map.keys()])
    visible_count = 0
    for coord, height in height_map.items():
        if is_edge(coord, max_x, max_y):
            visible_count += 1
            continue

        if any(
            [
                is_tallest_tree_in_path(
                    height, get_top_path_heights(height_map, coord)
                ),
                is_tallest_tree_in_path(
                    height, get_bottom_path_heights(height_map, coord, max_y)
                ),
                is_tallest_tree_in_path(
                    height, get_left_path_heights(height_map, coord)
                ),
                is_tallest_tree_in_path(
                    height, get_right_path_heights(height_map, coord, max_x)
                ),
            ]
        ):
            visible_count += 1
            continue

    return visible_count


if __name__ == "__main__":
    p1 = solve_p1()
    assert p1 == 1859
    print(p1)
