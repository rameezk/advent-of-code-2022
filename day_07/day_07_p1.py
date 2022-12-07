from collections import defaultdict


def parse_data(filename: str) -> list[list]:
    with open(filename) as f:
        lines = map(lambda l: l.strip().split(), f.readlines())
        return list(lines)


def compute_dir_sizes(lines: list[list]) -> dict:
    path_stack = []
    dir_sizes = defaultdict(int)

    for line in lines:
        match line[0], line[1]:
            case "$", "cd":
                dir_name = line[2]
                if dir_name != "..":
                    path_stack.append(line[2])
                else:
                    path_stack.pop()
                continue
            case "$", "ls":
                continue
            case "dir", _:
                continue
            case _, _:
                for i in range(len(path_stack)):
                    key = tuple(path_stack[: i + 1])
                    dir_size = int(line[0])
                    dir_sizes[key] += dir_size
                    continue

    return dir_sizes


def compute_totals_under_threshold(threshold: int, dir_sizes: dict) -> int:
    total = 0
    for s in dir_sizes.values():
        if s <= threshold:
            total += s
    return total


def solve_p1():
    lines = parse_data("./input.txt")
    dir_sizes = compute_dir_sizes(lines)
    total = compute_totals_under_threshold(100000, dir_sizes)
    return total


if __name__ == "__main__":
    p1 = solve_p1()
    print(p1)
