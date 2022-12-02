from enum import StrEnum, auto

import pytest


class Hand(StrEnum):
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()


class Strategy(StrEnum):
    LOSE = auto()
    DRAW = auto()
    WIN = auto()


lookup_hand = {
    "A": Hand.ROCK,
    "B": Hand.PAPER,
    "C": Hand.SCISSORS,
    "X": Hand.ROCK,
    "Y": Hand.PAPER,
    "Z": Hand.SCISSORS,
}
lookup_strategy = {
    "X": Strategy.LOSE,
    "Y": Strategy.DRAW,
    "Z": Strategy.WIN,
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


def strategise_hand(strategy: Strategy, opponent_hand: Hand) -> Hand:
    match strategy:
        case Strategy.LOSE:
            return beats[opponent_hand]
        case Strategy.DRAW:
            return opponent_hand
        case Strategy.WIN:
            return [k for k, v in beats.items() if v == opponent_hand][0]


def solve_p2(filename: str):
    total = 0
    with open(filename) as file:
        for line in file:
            opponent, me = line.strip().split(" ")
            opponent_hand = lookup_hand[opponent]
            strategy = lookup_strategy[me]
            my_new_hand = strategise_hand(strategy, opponent_hand)
            score = check_score(opponent_hand, my_new_hand)
            total += score
    return total


if __name__ == "__main__":
    p2 = solve_p2("./input.txt")
    print(p2)


@pytest.mark.parametrize(
    "filename, expected_total_score",
    [
        ("./sample.txt", 12),
        ("./input.txt", 12989),
    ],
)
def test_p2(filename, expected_total_score):
    assert solve_p2(filename) == expected_total_score
