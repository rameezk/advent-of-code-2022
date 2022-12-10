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


def compute_pixels(program: list[list[str, int | None]]) -> list[int]:
    x_register = 1
    pixels = []

    for instruction, by in program:
        if instruction == "noop":
            pixels.append(x_register)
        else:
            pixels += [x_register] * 2
            x_register += by

    return pixels


def render_screen(pixels: list[int]) -> None:
    for i, pixel in enumerate(pixels):
        position = i % 40

        end_of_line = position == 39

        if position in [pixel - 1, pixel, pixel + 1]:
            print("█", end="")
        else:
            print(".", end="")

        if end_of_line:
            print()


@timeit
def solve_p2():
    program = parse_program("./input.txt")
    pixels = compute_pixels(program)
    render_screen(pixels)


if __name__ == "__main__":
    p2 = solve_p2()
