import pytest


def solve_p1(filename: str):
    with open(filename) as file:
        sum_priorities = 0
        for line in file:
            rucksack = list(line.strip())
            middle_idx = len(rucksack) // 2
            compartment_1, compartment_2 = rucksack[:middle_idx], rucksack[middle_idx:]
            common_item: str = list(set(compartment_1) & set(compartment_2))[0]
            sum_priorities += (
                (ord(common_item) - 96)
                if common_item.islower()
                else (ord(common_item) - 38)
            )
    return sum_priorities


if __name__ == "__main__":
    p1 = solve_p1("./input.txt")
    print(p1)


@pytest.mark.parametrize(
    "filename, expected_sum",
    [
        ("./input.txt", 7785),
    ],
)
def test_p1(filename, expected_sum):
    assert solve_p1(filename) == expected_sum
