from common.timing import timeit


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


def is_tallest_tree_in_path(tree_height: int, path_heights: list[int]) -> bool:
    if not path_heights:
        return False

    current_height = tree_height
    for path_height in path_heights:
        if current_height <= path_height:
            return False

    return True


def get_max_coords(height_map: dict) -> tuple[int, int]:
    max_x, max_y = max([k for k in height_map.keys()])
    return max_x, max_y


def is_edge(height_map: dict, coord: tuple[int, int]) -> bool:
    x, y = coord
    max_x, max_y = get_max_coords(height_map)
    return x == 0 or y == 0 or x == max_x or y == max_y


@timeit
def solve_p1():
    height_map = {}
    with open("./input.txt") as file:
        for y, line in enumerate(file):
            for x, c in enumerate(line.strip()):
                height_map[x, y] = int(c)

    visible_count = 0
    for coord, height in height_map.items():
        if is_edge(height_map, coord):
            visible_count += 1
            continue

        if any(
            [
                is_tallest_tree_in_path(
                    height, get_top_path_heights(height_map, coord)
                ),
                is_tallest_tree_in_path(
                    height, get_bottom_path_heights(height_map, coord)
                ),
                is_tallest_tree_in_path(
                    height, get_left_path_heights(height_map, coord)
                ),
                is_tallest_tree_in_path(
                    height, get_right_path_heights(height_map, coord)
                ),
            ]
        ):
            visible_count += 1
            continue

    return visible_count


if __name__ == "__main__":
    p1 = solve_p1()
    print(p1)
