import re
from collections import defaultdict

import pytest


def parse_data(filename: str) -> (dict, list):
    stacks = defaultdict(list)
    instructions = []
    with open(filename) as file:
        for line in file:
            # parse stacks
            if "[" in line:
                letters = [line[i] for i in range(1, len(line), 4)]
                for stack_number, letter in enumerate(letters, start=1):
                    if letter != " ":
                        stacks[stack_number].insert(0, letter)
            elif "move" in line:
                instructions.append(map(int, re.findall(r"(\d+)", line.strip())))
            # Skip any other line
            else:
                ...

        return stacks, instructions


def top_crates(stacks: dict) -> str:
    crates = ""
    for i in range(1, len(stacks.keys()) + 1):
        crates += stacks[i][-1]
    return crates


def solve_p2(filename: str):
    stacks, instructions = parse_data(filename)

    for number_of_crates_to_move, from_stack, to_stack in instructions:
        crates_to_move = stacks[from_stack][-number_of_crates_to_move:]
        stacks[to_stack] += crates_to_move
        del stacks[from_stack][-number_of_crates_to_move:]

    return top_crates(stacks)


if __name__ == "__main__":
    p2 = solve_p2("./input.txt")
    print(p2)


@pytest.mark.parametrize(
    "filename, expected_top_crates",
    [
        ("./sample.txt", "MCD"),
        ("./input.txt", "HZFZCCWWV"),
    ],
)
def test_p2(filename, expected_top_crates):
    assert solve_p2(filename) == expected_top_crates
