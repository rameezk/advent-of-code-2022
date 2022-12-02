from enum import StrEnum, auto

import pytest


class Hand(StrEnum):
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()


lookup_hand = {
    "A": Hand.ROCK,
    "B": Hand.PAPER,
    "C": Hand.SCISSORS,
    "X": Hand.ROCK,
    "Y": Hand.PAPER,
    "Z": Hand.SCISSORS,
}
score_mapping = {
    Hand.ROCK: 1,
    Hand.PAPER: 2,
    Hand.SCISSORS: 3,
}
beats = {
    Hand.ROCK: Hand.SCISSORS,
    Hand.PAPER: Hand.ROCK,
    Hand.SCISSORS: Hand.PAPER,
}


def check_score(opponent_hand: Hand, my_hand: Hand) -> int:
    my_hand_score = score_mapping[my_hand]

    if opponent_hand == my_hand:
        return my_hand_score + 3

    i_won = beats[my_hand] == opponent_hand
    if i_won:
        my_hand_score += 6
    return my_hand_score


def solve_p1(filename: str):
    total = 0
    with open(filename) as file:
        for line in file:
            opponent_hand, my_hand = map(
                lambda h: lookup_hand[h], line.strip().split(" ")
            )
            score = check_score(opponent_hand, my_hand)
            total += score
    return total


if __name__ == "__main__":
    p1 = solve_p1("./input.txt")
    print(p1)


@pytest.mark.parametrize(
    "opponent, me, expected_score",
    [
        ("A", "Y", 8),
        ("B", "X", 1),
        ("C", "Z", 6),
    ],
)
def test_score(opponent, me, expected_score):
    assert check_score(lookup_hand[opponent], lookup_hand[me]) == expected_score


@pytest.mark.parametrize(
    "filename, expected_total_score",
    [
        ("./sample.txt", 15),
        ("./input.txt", 15691),
    ],
)
def test_p1(filename, expected_total_score):
    assert solve_p1(filename) == expected_total_score
