def solve_p1():
    with open("./input.txt") as file:
        count = 0

        for line in file:
            pair_1, pair_2 = line.strip().split(",")
            x1, y1 = map(int, pair_1.split("-"))
            x2, y2 = map(int, pair_2.split("-"))

            if (x2 >= x1 and y2 <= y1) or (x1 >= x2 and y1 <= y2):
                count += 1

    return count


if __name__ == "__main__":
    p1 = solve_p1()
    print(p1)
