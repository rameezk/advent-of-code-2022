from common.timing import timeit

from collections import Counter

KNOWN_DIGITS_LENGTHS = [2, 4, 3, 7]

DIGITS = [
    {"a", "b", "c", "e", "f", "g"},  # 0
    {"c", "f"},  # 1
    {"a", "c", "d", "e", "g"},  # 2
    {"a", "c", "d", "f", "g"},  # 3
    {"b", "c", "d", "f"},  # 4
    {"a", "b", "d", "f", "g"},  # 5
    {"a", "b", "d", "e", "f", "g"},  # 6
    {"a", "c", "f"},  # 7
    {"a", "b", "c", "d", "e", "f", "g"},  # 8
    {"a", "b", "c", "d", "f", "g"},  # 9
]


@timeit
def p1():
    count_known_digits = 0
    with open("./input.txt", "r") as file:
        for line in file:
            _, output_notes = line.split("|")
            outputs = output_notes.split()
            for output in outputs:
                if len(output) in KNOWN_DIGITS_LENGTHS:
                    count_known_digits += 1
    print(count_known_digits)


def parse_lines(payload):
    for line in payload:
        signal, output = line.split(" | ")
        yield signal, output


def get_key(digit):
    return "".join(sorted(digit))


def encode(counter, digit):
    return sum(counter[segment] for segment in digit)


@timeit
def p2():
    # segment lights up x times
    segment_counter = {
        "a": 8,
        "b": 6,
        "c": 8,
        "d": 7,
        "e": 4,
        "f": 9,
        "g": 7,
    }

    fingerprints = [encode(segment_counter, digit) for digit in DIGITS]

    outputs = []
    with open("./input.txt", "r") as file:
        for line in file:
            signal, output = line.strip().split(" | ")
            signal_counter = Counter(signal)

            digits = {}
            for digit in signal.split():
                fingerprint = encode(signal_counter, digit)
                digits[get_key(digit)] = fingerprints.index(fingerprint)

            outputs.append(
                int("".join(str(digits[get_key(digit)]) for digit in output.split()))
            )

        print(sum(outputs))


if __name__ == "__main__":
    print("======p1=====")
    p1()
    print("======p1=====")
    print("======p2=====")
    p2()
    print("======p2=====")
