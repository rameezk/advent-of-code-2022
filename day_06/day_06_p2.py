from common.windowing import sliding_window


def is_unique(s):
    d = []
    for c in s:
        if c in d:
            return False
        else:
            d.append(c)
    return True


WIN_SIZE = 14


def solve_p2():
    with open("./input.txt") as file:
        line = file.read()

    for char_idx, window in enumerate(sliding_window(line, WIN_SIZE)):
        if is_unique(window):
            return char_idx + WIN_SIZE


if __name__ == "__main__":
    p2 = solve_p2()
    print(p2)
