from common.timing import timeit


def parse_program(filename: str) -> list[list[str, int | None]]:
    program = []
    with open(filename) as file:
        for line in file:
            line_data = line.strip().split()
            program.append(
                [
                    line_data[0],
                    int(line_data[1]) if len(line_data) == 2 else None,
                ]
            )
    return program


def compute_signal_strength(program: list[list[str, int | None]]) -> int:
    signal_strength = 0
    next_cycle_count = 20
    cycles_left = 0
    x_register = 1

    for instruction, by in program:
        if instruction == "noop":
            cycles_left += 1
        else:
            cycles_left += 2

        if cycles_left >= next_cycle_count:
            signal_strength += next_cycle_count * x_register
            next_cycle_count += 40

        if instruction != "noop":
            x_register += by

    return signal_strength


@timeit
def solve_p1():
    program = parse_program("./input.txt")
    signal_strength = compute_signal_strength(program)
    return signal_strength


if __name__ == "__main__":
    p1 = solve_p1()
    print(p1)
    assert p1 == 11720
