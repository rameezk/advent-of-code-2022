import re
from collections import defaultdict


def solve_p1():
    with open("./input.txt") as file:
        data = file.read().split("\n\n")

    monkey_notes = [list(map(str.strip, d.splitlines())) for d in data]

    monkey_items = defaultdict(list)
    monkey_order = []
    monkey_operations = dict()
    monkey_divisors = dict()
    monkey_throws = dict()
    for notes in monkey_notes:
        id_ = re.search(r"(\d+)", notes[0]).groups()[0]

        monkey_order.append(id_)

        items = list(map(int, re.findall(r"(\d+)", notes[1])))
        monkey_items[id_].extend(items)

        operation = re.search(r"Operation: new = old (.) (.*)", notes[2]).groups()
        monkey_operations[id_] = operation

        divisor = re.search(r"(\d+)", notes[3]).groups()[0]
        monkey_divisors[id_] = int(divisor)

        throw_true = re.search(r"(\d+)", notes[4]).groups()[0]
        throw_false = re.search(r"(\d+)", notes[5]).groups()[0]
        monkey_throws[id_] = (throw_true, throw_false)

    inspections = defaultdict(lambda: 0)
    for _ in range(20):
        for id_ in monkey_order:
            while len(monkey_items[id_]) > 0:
                item = monkey_items[id_].pop(0)

                inspections[id_] += 1

                operation_operand, by = monkey_operations[id_]
                if by == "old":
                    by = item
                match operation_operand:
                    case "+":
                        worry_level = item + int(by)
                    case "-":
                        worry_level = item - int(by)
                    case "*":
                        worry_level = item * int(by)
                    case "/":
                        worry_level = item / int(by)
                    case _:
                        raise AssertionError(f"Unknown operand {operation_operand}")

                worry_level = worry_level // 3
                divisor = monkey_divisors[id_]

                if worry_level % divisor == 0:
                    throw_to = monkey_throws[id_][0]
                else:
                    throw_to = monkey_throws[id_][1]
                monkey_items[throw_to].append(worry_level)

    top_inspections = sorted(inspections.values(), reverse=True)
    monkey_business = top_inspections[0] * top_inspections[1]
    return monkey_business


if __name__ == "__main__":
    p1 = solve_p1()
    print(p1)
