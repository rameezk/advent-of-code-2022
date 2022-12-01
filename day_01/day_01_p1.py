def compute_totals(data: str) -> list:
    totals = []
    for group in data.split("\n\n"):
        group_total = sum([int(x) for x in group.splitlines()])
        totals.append(group_total)
    return totals


def p1():
    with open("./input.txt") as f:
        data = f.read()
    totals = compute_totals(data)
    highest = max(totals)
    return highest


if __name__ == "__main__":
    p1 = p1()
    print(p1)
