import typing
from collections import defaultdict

from common.timing import timeit


def get_edges(filename: str) -> typing.Dict[str, typing.Set]:
    edges = defaultdict(set)
    with open(filename) as file:
        for line in file:
            start, end = line.strip().split("-")
            edges[start].add(end)
            edges[end].add(start)
    return edges


@timeit
def p1():
    edges = get_edges("./input.txt")

    paths = set()
    journey = [("start",)]
    while journey:
        path = journey.pop()

        if path[-1] == "end":
            paths.add(path)
            continue

        candidate: str
        for candidate in edges[path[-1]]:
            if candidate.isupper() or candidate not in path:
                journey.append((*path, candidate))

    print(len(paths))


@timeit
def p2():
    edges = get_edges("./input.txt")

    paths = set()
    journey = [(("start",), False)]
    while journey:
        path, small_cave_visited = journey.pop()

        if path[-1] == "end":
            paths.add(path)
            continue

        candidate: str
        for candidate in edges[path[-1]]:
            if candidate == "start":
                continue
            elif candidate.isupper() or candidate not in path:
                journey.append(((*path, candidate), small_cave_visited))
            elif not small_cave_visited and path.count(candidate) == 1:
                journey.append(((*path, candidate), True))

    print(len(paths))


if __name__ == "__main__":
    print("======p1=====")
    p1()
    print("======p1=====")
    print("======p2=====")
    p2()
    print("======p2=====")
