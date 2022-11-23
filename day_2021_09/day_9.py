import typing

from common.timing import timeit


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


def count_most_left(heightmap, x, y) -> int:
    count = 0
    next_x, next_y = get_left_coord(x, y)
    if next_x is None or next_y is None:
        return count
    next_height = height_at_point(heightmap, next_x, next_y)
    while next_x is not None and next_height < 9:
        count += 1
        next_x, next_y = get_left_coord(next_x, next_y)
        if next_x is not None and next_y is not None:
            next_height = height_at_point(heightmap, next_x, next_y)
    return count


def count_most_right(heightmap, x, y) -> int:
    count = 0
    max_x = len(heightmap[0]) + 1
    next_x, next_y = get_right_coord(x, y, max_x)
    if next_x is None or next_y is None:
        return count
    next_height = height_at_point(heightmap, next_x, next_y)
    while next_x is not None and next_height < 9:
        count += 1
        next_x, next_y = get_right_coord(next_x, next_y)
        if next_x is not None and next_y is not None:
            next_height = height_at_point(heightmap, next_x, next_y)
    return count


def count_most_top(heightmap, x, y) -> int:
    count = 0
    next_x, next_y = get_top_coord(x, y)

    if next_x is None or next_y is None:
        return count

    next_height = height_at_point(heightmap, next_x, next_y)
    while next_y is not None and next_height < 9:
        count += 1
        next_x, next_y = get_top_coord(next_x, next_y)
        if next_x is not None and next_y is not None:
            next_height = height_at_point(heightmap, next_x, next_y)
    return count


def count_most_bottom(heightmap, x, y) -> int:
    count = 0
    max_y = len(heightmap) + 1
    next_x, next_y = get_bottom_coord(x, y, max_y)

    if next_x is None or next_y is None:
        return count

    next_height = height_at_point(heightmap, next_x, next_y)
    while next_y is not None and next_height < 9:
        count += 1
        next_x, next_y = get_bottom_coord(next_x, next_y, max_y)
        if next_x is not None and next_y is not None:
            next_height = height_at_point(heightmap, next_x, next_y)
    return count


@timeit
def p1():
    heightmap = parse_heightmap("./input.txt")

    lowest_heights = get_lowest_heights(heightmap)

    risk_level = 0
    for _, height in lowest_heights.items():
        risk_level += 1 + height
    print(risk_level)


@timeit
def p2():
    heightmap = parse_heightmap("./sample.txt")
    lowest_heights = get_lowest_heights(heightmap)
    print(lowest_heights)

    x = 1
    y = 0
    print(count_most_left(heightmap, x, y))
    print(count_most_right(heightmap, x, y))
    print(count_most_top(heightmap, x, y))
    print(count_most_bottom(heightmap, x, y))


if __name__ == "__main__":
    print("======p1=====")
    # p1()
    print("======p1=====")
    print("======p2=====")
    p2()
    print("======p2=====")
