import typing
from enum import StrEnum, auto
from functools import reduce

from common.timing import timeit


class Status(StrEnum):
    INCOMPLETE = auto()
    CORRUPTED = auto()
    VALID = auto()


VALID_CHUNKS = [("(", ")"), ("[", "]"), ("{", "}"), ("<", ">")]
OPENING_BRACES = [b[0] for b in VALID_CHUNKS]
CLOSING_BRACES = [b[1] for b in VALID_CHUNKS]
PAIR_LOOKUP = {
    **{c: o for o, c in zip(OPENING_BRACES, CLOSING_BRACES)},
    **{o: c for o, c in zip(OPENING_BRACES, CLOSING_BRACES)},
}
CORRUPTED_CHAR_SCORE_LOOKUP = {")": 3, "]": 57, "}": 1197, ">": 25137}
CORRECT_CHAR_SCORE_LOOKUP = {")": 1, "]": 2, "}": 3, ">": 4}


def check(chunks: typing.List[str]) -> (Status, typing.Optional[str]):
    """Check for valid chunks. Will return first illegal char if found."""
    s = []
    for c in chunks:
        if c in OPENING_BRACES:
            s.append(c)
        else:
            b = s.pop()
            if PAIR_LOOKUP[c] != b:
                return Status.CORRUPTED, c
    if len(s) == 0:
        return Status.VALID, None
    else:
        return Status.INCOMPLETE, None


def check_and_correct(
    chunks: typing.List[str],
) -> (Status, typing.Optional[typing.List[str]]):
    """Check for valid chunks and suggests the correct completion."""
    s = []
    for c in chunks:
        if c in OPENING_BRACES:
            s.append(c)
        else:
            b = s.pop()
            if PAIR_LOOKUP[c] != b:
                return Status.CORRUPTED, None
    if len(s) == 0:
        return Status.VALID, None
    else:
        correct_characters = [PAIR_LOOKUP[c] for c in s[::-1]]
        return Status.INCOMPLETE, correct_characters


@timeit
def p1() -> int:
    illegal_characters = []
    with open("./input.txt", "r") as file:
        for line in file:
            chunks = list(line.strip())
            status, first_illegal_char = check(chunks)
            if status == Status.CORRUPTED:
                illegal_characters.append(first_illegal_char)
    score = sum([CORRUPTED_CHAR_SCORE_LOOKUP[c] for c in illegal_characters])
    return score


@timeit
def p2() -> int:
    scores = []
    with open("./input.txt", "r") as file:
        for line in file:
            chunks = list(line.strip())
            status, correct_characters = check_and_correct(chunks)
            if status == Status.INCOMPLETE:
                score = reduce(
                    lambda s, c: (s * 5) + CORRECT_CHAR_SCORE_LOOKUP[c],
                    correct_characters,
                    0,
                )
                scores.append(score)
    middle_score = sorted(scores)[(len(scores) - 1) // 2]
    return middle_score


if __name__ == "__main__":
    print("======p1=====")
    p1 = p1()
    assert p1 == 193275
    print(p1)
    print("======p1=====")
    print("======p2=====")
    p2 = p2()
    assert p2 == 2429644557
    print(p2)
    print("======p2=====")
