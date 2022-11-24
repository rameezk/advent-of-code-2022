import typing

from common.timing import timeit

from functools import reduce


def get_top_coord(x, y) -> (int, int):
    if y <= 0:
        return None, None
    return x, y - 1


def get_bottom_coord(x, y, max_y) -> (int, int):
    if y >= max_y:
        return None, None
    return x, y + 1


def get_right_coord(x, y, max_x) -> (int, int):
    if x >= max_x:
        return None, None
    return x + 1, y


def get_left_coord(x, y) -> (int, int):
    if x <= 0:
        return None, None
    return x - 1, y


def parse_heightmap(filename: str) -> typing.List[typing.List[int]]:
    heightmap = []
    with open(filename, "r") as file:
        for line in file:
            heightmap.append(list(map(int, list(line.strip()))))
    return heightmap


def height_at_point(heightmap, x, y) -> typing.Optional[int]:
    try:
        return heightmap[y][x]
    except IndexError:
        return None


def get_groups(heightmap, current_x, current_y) -> typing.List:
    groups = [(height_at_point(heightmap, current_x, current_y), current_x, current_y)]

    max_x = len(heightmap[0]) - 1
    max_y = len(heightmap) - 1

    top_x, top_y = get_top_coord(current_x, current_y)
    if top_x is not None and top_y is not None:
        groups.append((height_at_point(heightmap, top_x, top_y), top_x, top_y))

    bottom_x, bottom_y = get_bottom_coord(current_x, current_y, max_y)
    if bottom_x is not None and bottom_y is not None:
        groups.append(
            (height_at_point(heightmap, bottom_x, bottom_y), bottom_x, bottom_y)
        )

    left_x, left_y = get_left_coord(current_x, current_y)
    if left_x is not None and left_y is not None:
        groups.append((height_at_point(heightmap, left_x, left_y), left_x, left_y))

    right_x, right_y = get_right_coord(current_x, current_y, max_x)
    if right_x is not None and right_y is not None:
        groups.append((height_at_point(heightmap, right_x, right_y), right_x, right_y))

    return groups


def get_lowest_heights(heightmap):
    max_x = len(heightmap[0]) - 1
    max_y = len(heightmap) - 1

    lowest_heights = {}
    lowest_point_mapping = {}
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            groups = get_groups(heightmap, x, y)
            sorted_groups = sorted(groups, key=lambda g: g[0])

            lowest_height, lowest_x, lowest_y = sorted_groups[0]
            # check if already have a lowest
            if (lowest_x, lowest_y) not in lowest_point_mapping:
                lowest_heights[(lowest_x, lowest_y)] = lowest_height

            lowest_point_mapping[(x, y)] = sorted_groups[0]
            for group in sorted_groups[1::]:
                lowest_heights.pop((group[1], group[2]), None)
    return lowest_heights


def traverse(
    heightmap: typing.List[typing.List[int]],
    points_to_visit: typing.List[typing.Tuple[int, int]],
    number_of_points_visited: int,
    already_visited_points: typing.Dict[typing.Tuple, bool],
) -> int:
    max_x = len(heightmap[0]) - 1
    max_y = len(heightmap) - 1

    if len(points_to_visit) == 0:
        return number_of_points_visited

    next_points_to_visit = []
    for x, y in points_to_visit:
        if (x, y) in already_visited_points.keys():
            continue

        already_visited_points[(x, y)] = True
        height_at_this_point = height_at_point(heightmap, x, y)
        if height_at_this_point < 9:
            number_of_points_visited += 1
        else:
            continue

        # top
        top_x, top_y = get_top_coord(x, y)
        if None not in (top_x, top_y):
            next_points_to_visit.append((top_x, top_y))

        # left
        left_x, left_y = get_left_coord(x, y)
        if None not in (left_x, left_y):
            next_points_to_visit.append((left_x, left_y))

        # bottom
        bottom_x, bottom_y = get_bottom_coord(x, y, max_y)
        if None not in (bottom_x, bottom_y):
            next_points_to_visit.append((bottom_x, bottom_y))

        # right
        right_x, right_y = get_right_coord(x, y, max_x)
        if None not in (right_x, right_y):
            next_points_to_visit.append((right_x, right_y))

    return traverse(
        heightmap,
        next_points_to_visit,
        number_of_points_visited,
        already_visited_points,
    )


@timeit
def solve_p1():
    heightmap = parse_heightmap("./input.txt")
    lowest_heights = get_lowest_heights(heightmap)
    risk_level = 0
    for _, height in lowest_heights.items():
        risk_level += 1 + height
    return risk_level


@timeit
def solve_p2():
    heightmap = parse_heightmap("./input.txt")
    lowest_heights = get_lowest_heights(heightmap)
    basin_sizes = []
    for lowest_point in lowest_heights.keys():
        number_of_points_visited = traverse(
            heightmap,
            [lowest_point],
            0,
            {},
        )
        basin_sizes.append(number_of_points_visited)
    thing = reduce(lambda x, y: x * y, sorted(basin_sizes, reverse=True)[0:3])
    return thing


if __name__ == "__main__":
    print("======p1=====")
    risk_level = solve_p1()
    assert risk_level == 560
    print(risk_level)
    print("======p1=====")
    print("======p2=====")
    product = solve_p2()
    assert product == 959136
    print(product)
    print("======p2=====")
