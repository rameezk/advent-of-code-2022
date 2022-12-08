from common.timing import timeit
from math import prod


def get_top_path_heights(height_map: dict, coord: tuple[int, int]) -> list[int]:
    x, y = coord
    heights = []
    for y_d in range(y - 1, -1, -1):
        heights.append(height_map[(x, y_d)])
    return heights


def get_bottom_path_heights(height_map: dict, coord: tuple[int, int]) -> list[int]:
    x, y = coord
    heights = []
    _, max_y = get_max_coords(height_map)
    for y_d in range(y + 1, max_y + 1):
        heights.append(height_map[(x, y_d)])
    return heights


def get_right_path_heights(height_map: dict, coord: tuple[int, int]) -> list[int]:
    x, y = coord
    heights = []
    max_x, _ = get_max_coords(height_map)
    for x_d in range(x + 1, max_x + 1):
        heights.append(height_map[(x_d, y)])
    return heights


def get_left_path_heights(height_map: dict, coord: tuple[int, int]) -> list[int]:
    x, y = coord
    heights = []
    for x_d in range(x - 1, -1, -1):
        heights.append(height_map[(x_d, y)])
    return heights


def compute_scenic_score(tree_height: int, path_heights: list[int]) -> int:
    if not path_heights:
        return False

    score = 0
    for path_height in path_heights:
        score += 1
        if path_height >= tree_height:
            return score
    return score


def get_max_coords(height_map: dict) -> tuple[int, int]:
    max_x, max_y = max([k for k in height_map.keys()])
    return max_x, max_y


def is_edge(height_map: dict, coord: tuple[int, int]) -> bool:
    x, y = coord
    max_x, max_y = get_max_coords(height_map)
    return x == 0 or y == 0 or x == max_x or y == max_y


@timeit
def solve_p2():
    height_map = {}
    with open("./input.txt") as file:
        for y, line in enumerate(file):
            for x, c in enumerate(line.strip()):
                height_map[x, y] = int(c)

    scenic_scores = []
    for coord, height in height_map.items():
        if is_edge(height_map, coord):
            continue

        top_scenic_score = compute_scenic_score(
            height, get_top_path_heights(height_map, coord)
        )

        left_scenic_score = compute_scenic_score(
            height, get_left_path_heights(height_map, coord)
        )

        right_scenic_score = compute_scenic_score(
            height, get_right_path_heights(height_map, coord)
        )

        bottom_scenic_score = compute_scenic_score(
            height, get_bottom_path_heights(height_map, coord)
        )

        scenic_score = prod(
            [
                top_scenic_score,
                bottom_scenic_score,
                left_scenic_score,
                right_scenic_score,
            ]
        )
        print(
            f"{coord=} {height=} {(top_scenic_score, left_scenic_score, right_scenic_score, bottom_scenic_score)} {scenic_score=}"
        )
        scenic_scores.append(scenic_score)

    return max(scenic_scores)


if __name__ == "__main__":
    p2 = solve_p2()
    print(p2)
