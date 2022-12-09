from __future__ import annotations

from dataclasses import dataclass

from common.timing import timeit


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def is_adjacent_to(self, other: Point):
        d_x = self.x - other.x
        d_y = self.y - other.y
        is_adj = (abs(d_x), abs(d_y)) in [(0, 0), (1, 0), (0, 1), (1, 1)]
        return is_adj

    def move_right(self) -> Point:
        return Point(self.x + 1, self.y)

    def move_left(self) -> Point:
        return Point(self.x - 1, self.y)

    def move_down(self) -> Point:
        return Point(self.x, self.y + 1)

    def move_up(self) -> Point:
        return Point(self.x, self.y - 1)


def parse_motions(filename: str) -> list[(str, int)]:
    motions = []
    with open(filename) as file:
        for line in file:
            direction, by_s = line.strip().split()
            motions.append((direction, int(by_s)))
    return motions


def follow_head(head: Point, tail: Point) -> Point:
    if head.is_adjacent_to(tail):
        return tail

    if head.y == tail.y:
        # horizontal movement
        return tail.move_right() if head.x > tail.x else tail.move_left()

    if head.x == tail.x:
        # vertical movement
        return tail.move_down() if head.y > tail.y else tail.move_up()

    # diagonal movement
    if head.x > tail.x:
        tail = tail.move_right()
    else:
        tail = tail.move_left()

    if head.y > tail.y:
        tail = tail.move_down()
    else:
        tail = tail.move_up()

    return tail


@timeit
def solve_p1():
    motions = parse_motions("./input.txt")

    head = Point(0, 0)
    tail = Point(0, 0)

    visited = set()

    for direction, by in motions:
        for _ in range(by):
            match direction:
                case "R":
                    head = head.move_right()
                case "L":
                    head = head.move_left()
                case "U":
                    head = head.move_up()
                case "D":
                    head = head.move_down()
                case _:
                    raise AssertionError(f"Unknown direction {direction}")

            tail = follow_head(head, tail)
            visited.add(tail)

    return len(visited)


if __name__ == "__main__":
    p1 = solve_p1()
    print(p1)
