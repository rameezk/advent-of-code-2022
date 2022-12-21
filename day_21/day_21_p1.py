from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from enum import StrEnum

from common.timing import timeit


class Operator(StrEnum):
    ADD = "+"
    MULTIPLY = "*"
    SUBTRACT = "-"
    DIVIDE = "/"


@dataclass
class Monkey:
    operator: Operator | None = None
    left: Monkey | str | None = None
    right: Monkey | str | None = None
    value: int | None = None


def ready_to_compute(monkeys: dict) -> bool:
    for name, monkey in monkeys.items():
        if monkey.value is None:
            return False
    return True


def expand(monkeys: dict[str, Monkey]) -> dict:
    for name, monkey in monkeys.items():
        if monkey.value is None:
            l = monkeys[monkey.left].value
            r = monkeys[monkey.right].value
            o = monkey.operator
            if l is not None and r is not None:
                monkey.value = int(eval(f"{l} {o} {r}"))
    return monkeys


@timeit
def solve_p1():
    monkeys = OrderedDict()
    with open("./input.txt") as file:
        for line in file:
            words = line.strip().split()
            name = words[0].split(":")[0]
            if len(words) == 2:
                monkeys[name] = Monkey(value=int(words[1]))
            else:
                monkeys[name] = Monkey(
                    left=words[1],
                    operator=Operator(words[2]),
                    right=words[3],
                )

    while not ready_to_compute(monkeys):
        monkeys = expand(monkeys)
    return monkeys["root"].value


if __name__ == "__main__":
    p1 = solve_p1()
    print(p1)
