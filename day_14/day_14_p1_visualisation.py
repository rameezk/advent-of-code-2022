import pygame
from collections import defaultdict
from enum import StrEnum, auto
from itertools import pairwise


class CaveItem(StrEnum):
    ROCK = auto()
    AIR = auto()
    SAND = auto()
    HOLE = auto()


CAVE = dict[tuple[int, int], CaveItem]
HOLE = (500, 0)


def parse_cave(filename: str) -> CAVE:
    cave = defaultdict(lambda: CaveItem.AIR)

    with open(filename) as file:
        for line in file:
            path = list(
                map(
                    lambda p: list(map(int, p.strip().split(","))),
                    line.strip().split("->"),
                )
            )
            path_pairs = pairwise(path)
            for (start_x, start_y), (end_x, end_y) in path_pairs:
                if start_x == end_x:
                    step = 1 if end_y > start_y else -1
                    for y in range(start_y, end_y + step, step):
                        cave[start_x, y] = CaveItem.ROCK
                elif start_y == end_y:
                    step = 1 if end_x > start_x else -1
                    for x in range(start_x, end_x + step, step):
                        cave[x, start_y] = CaveItem.ROCK
                else:
                    raise AssertionError(f"Cannot handle this path")

    cave[HOLE] = CaveItem.HOLE
    return cave


def paint_cave(
    p: pygame, screen, cave: CAVE, min_x: int, max_x: int, min_y: int, max_y: int
) -> None:

    for (x, y), item in cave.items():
        draw_x, draw_y = x - min_x, y - min_y
        match item:
            case CaveItem.ROCK:
                p.draw.rect(screen, (168, 147, 50), (draw_x, draw_y, 1, 1))
            case CaveItem.AIR:
                continue
            case CaveItem.SAND:
                p.draw.rect(screen, (47, 150, 81), (draw_x, draw_y, 1, 1))
            case CaveItem.HOLE:
                p.draw.rect(screen, (192, 40, 209), (draw_x, draw_y, 1, 1))
            case _:
                ...


def cave_bounds(cave: CAVE) -> tuple[int, int, int, int]:
    keys = cave.keys()
    x_s = [x for x, _ in keys]
    min_x, max_x = min(x_s), max(x_s)
    y_s = [y for _, y in keys]
    min_y, max_y = min(y_s), max(y_s)
    return min_x, max_x, min_y, max_y


def is_blocked(cave: CAVE, x, y) -> bool:
    return cave[x, y] in [CaveItem.ROCK, CaveItem.SAND]


def drop_sand(
    win, p, screen, cave: CAVE, min_x: int, max_x: int, min_y: int, max_y: int
) -> (CAVE, bool):
    x, y = HOLE

    while True:
        y += 1

        if y > max_y:
            return cave, False

        if not is_blocked(cave, x, y):
            was = cave[x, y]
            cave[x, y] = CaveItem.SAND
            screen.fill(black)
            paint_cave(p, screen, cave, min_x, max_x, min_y, max_y)
            win.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))
            pygame.display.update()
            pygame.time.wait(1)
            cave[x, y] = was
            continue
        else:
            if not is_blocked(cave, x - 1, y):
                x -= 1
                was = cave[x, y]
                cave[x, y] = CaveItem.SAND
                screen.fill(black)
                paint_cave(p, screen, cave, min_x, max_x, min_y, max_y)
                win.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))
                pygame.display.update()
                pygame.time.wait(1)
                cave[x, y] = was
                if x < min_x:
                    return cave, False
                continue

            if not is_blocked(cave, x + 1, y):
                x += 1
                was = cave[x, y]
                cave[x, y] = CaveItem.SAND
                screen.fill(black)
                paint_cave(p, screen, cave, min_x, max_x, min_y, max_y)
                win.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))
                pygame.display.update()
                pygame.time.wait(1)
                cave[x, y] = was
                if x > max_x:
                    return cave, False
                continue

            cave[x, y - 1] = CaveItem.SAND
            was = cave[x, y]
            cave[x, y] = CaveItem.SAND
            screen.fill(black)
            paint_cave(p, screen, cave, min_x, max_x, min_y, max_y)
            win.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))
            pygame.display.update()
            pygame.time.wait(1)
            cave[x, y] = was
            break

    return cave, True


run = True

if __name__ == "__main__":
    cave = parse_cave("./input.txt")
    min_x, max_x, min_y, max_y = cave_bounds(cave)

    screen_width, screen_height = (max_x - min_x + 10), (max_y - min_y + 10)

    print(screen_width, screen_height)

    scaling_factor = 10

    x, y = 10, 10
    rect_width, rect_height = 1, 1
    vel = 2
    black = (0, 0, 0)
    white = (255, 255, 255)
    pygame.init()
    win = pygame.display.set_mode(
        (screen_width * scaling_factor, screen_height * scaling_factor)
    )

    screen = pygame.Surface((screen_width, screen_height))
    font = pygame.font.Font("freesansbold.ttf", 32)

    pygame.display.set_caption("rameezk - AOC 2022 Day 14 Part 1")

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        can_continue = True
        sand_dropped = -1
        while can_continue:
            pygame.display.set_caption(f"{sand_dropped}")
            sand_dropped += 1
            cave, can_continue = drop_sand(
                win, pygame, screen, cave, min_x, max_x, min_y, max_y
            )
        pygame.time.wait(2000)
        run = False

        pygame.quit()
