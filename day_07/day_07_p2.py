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


def solve_p2():
    lines = parse_data("./input.txt")
    dir_sizes = compute_dir_sizes(lines)
    need_at_least = 30000000
    max_available = 70000000
    need_to_delete = need_at_least - (max_available - dir_sizes[("/",)])
    possible_deletions = []
    for s in dir_sizes.values():
        if s >= need_to_delete:
            possible_deletions.append(s)
    return min(possible_deletions)


if __name__ == "__main__":
    p2 = solve_p2()
    print(p2)
