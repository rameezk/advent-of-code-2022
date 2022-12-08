from common.timing import timeit
from math import prod
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


def compute_scenic_score(
    tree_height: int, path_heights: typing.Generator[int, None, None]
) -> int:
    score = 0
    for path_height in path_heights:
        score += 1
        if path_height >= tree_height:
            return score
    return score


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
def solve_p2():
    height_map = get_height_map("./input.txt")
    max_x, max_y = max([k for k in height_map.keys()])
    max_scenic_score = 0
    for coord, height in height_map.items():
        if is_edge(coord, max_x, max_y):
            continue

        scenic_score = 1
        top_scenic_score = compute_scenic_score(
            height, get_top_path_heights(height_map, coord)
        )
        scenic_score *= top_scenic_score

        left_scenic_score = compute_scenic_score(
            height, get_left_path_heights(height_map, coord)
        )
        scenic_score *= left_scenic_score

        right_scenic_score = compute_scenic_score(
            height, get_right_path_heights(height_map, coord, max_x)
        )
        scenic_score *= right_scenic_score

        bottom_scenic_score = compute_scenic_score(
            height, get_bottom_path_heights(height_map, coord, max_y)
        )
        scenic_score *= bottom_scenic_score

        if scenic_score > max_scenic_score:
            max_scenic_score = scenic_score

    return max_scenic_score


if __name__ == "__main__":
    p2 = solve_p2()
    assert p2 == 332640
    print(p2)
