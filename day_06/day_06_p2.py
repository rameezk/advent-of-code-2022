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

    for char_count, i in enumerate(range(len(line) - WIN_SIZE + 1)):
        thing = line[i : i + WIN_SIZE]
        if is_unique(thing):
            return char_count + WIN_SIZE


if __name__ == "__main__":
    p2 = solve_p2()
    print(p2)
