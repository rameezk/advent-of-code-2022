import pytest
from functools import reduce


def solve_p2(filename: str):
    with open(filename) as file:
        rucksacks = file.readlines()

    sum_priorities = 0
    for idx in range(0, len(rucksacks), 3):
        group = rucksacks[idx : idx + 3]
        common_item = list(
            reduce(
                lambda acc, g: acc & set(list(g.strip())), group, set(list(group[0]))
            )
        )[0]
        sum_priorities += (
            (ord(common_item) - 96)
            if common_item.islower()
            else (ord(common_item) - 38)
        )
    return sum_priorities


if __name__ == "__main__":
    p2 = solve_p2("./input.txt")
    print(p2)


@pytest.mark.parametrize(
    "filename, expected_sum",
    [
        ("./input.txt", 2633),
    ],
)
def test_p1(filename, expected_sum):
    assert solve_p2(filename) == expected_sum
