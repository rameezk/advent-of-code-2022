from common.timing import timeit
import typing
from enum import StrEnum, auto


class Status(StrEnum):
    INCOMPLETE = auto()
    CORRUPTED = auto()
    VALID = auto()


VALID_CHUNKS = [("(", ")"), ("[", "]"), ("{", "}"), ("<", ">")]
OPENING_BRACES = [b[0] for b in VALID_CHUNKS]
CLOSING_BRACES = [b[1] for b in VALID_CHUNKS]
PAIR_LOOKUP = {c: o for o, c in zip(OPENING_BRACES, CLOSING_BRACES)}
SCORE_LOOKUP = {")": 3, "]": 57, "}": 1197, ">": 25137}


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


@timeit
def p1() -> int:
    illegal_characters = []
    with open("./input.txt", "r") as file:
        for line in file:
            chunks = list(line.strip())
            status, first_illegal_char = check(chunks)
            if status == Status.CORRUPTED:
                illegal_characters.append(first_illegal_char)
    score = sum([SCORE_LOOKUP[c] for c in illegal_characters])
    return score


@timeit
def p2():
    ...


if __name__ == "__main__":
    print("======p1=====")
    p1 = p1()
    print(p1)
    print("======p1=====")
    print("======p2=====")
    # p2()
    print("======p2=====")
