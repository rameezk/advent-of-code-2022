def compute_totals(data: str) -> list:
    totals = []
    for group in data.split("\n\n"):
        group_total = sum([int(x) for x in group.splitlines()])
        totals.append(group_total)
    return totals


def solve_p2():
    with open("./input.txt") as f:
        data = f.read()
    totals = compute_totals(data)
    sum_top_3 = sum(sorted(totals, reverse=True)[:3])
    return sum_top_3


if __name__ == "__main__":
    p2 = solve_p2()
    print(p2)
