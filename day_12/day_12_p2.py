from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Generator

from common.timing import timeit


@dataclass
class Node:
    x: int
    y: int
    height: int
    distance: int | None = None
    previous_node: Node | None = None


Heightmap = list[list[Node]]


def parse(filename: str) -> (Heightmap, list[Node], Node):
    with open(filename) as file:
        data = file.read().strip()
    heightmap = [list(line) for line in data.splitlines()]

    sources = list()
    destination = None

    max_x = len(heightmap[0])
    max_y = len(heightmap)
    for y in range(max_y):
        for x in range(max_x):
            node = Node(x, y, ord(heightmap[y][x]))
            heightmap[y][x] = node

            if node.height == ord("S") or node.height == ord("a"):
                source = node
                source.height = ord("a")
                source.distance = 0
                sources.append(source)

            if node.height == ord("E"):
                destination = node
                destination.height = ord("z")

    return heightmap, sources, destination


def neighbours(
    heightmap: Heightmap, node: Node, max_x: int, max_y: int
) -> Generator[Node, None, None]:
    for d_x, d_y in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        x = node.x + d_x
        y = node.y + d_y
        if x < 0 or x >= max_x or y < 0 or y >= max_y:
            continue
        yield heightmap[y][x]


@timeit
def solve_p2():
    initial_heightmap, sources, destination = parse("./input.txt")

    max_x = len(initial_heightmap[0])
    max_y = len(initial_heightmap)

    min_distance = None

    for source in sources:
        heightmap = initial_heightmap.copy()
        source.distance = 0

        queue = deque()
        queue.append(source)

        while len(queue) > 0:
            node: Node = queue.popleft()

            if node == destination:
                path = []
                while node is not None:
                    path.append(node)
                    node = node.previous_node

                distance = len(path) - 1

                if min_distance is None:
                    min_distance = distance

                if min_distance is not None and distance < min_distance:
                    min_distance = distance

                break

            for neighbour in neighbours(heightmap, node, max_x, max_y):
                if neighbour.height - node.height > 1:
                    continue

                distance = node.distance + 1
                if neighbour.distance is None or neighbour.distance > distance:
                    neighbour.distance = distance
                    neighbour.previous_node = node
                    queue.append(neighbour)

    return min_distance


if __name__ == "__main__":
    p2 = solve_p2()
    print(p2)
