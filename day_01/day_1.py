from common.timing import timeit


def compute_totals(data: str) -> list:
    totals = []
    for group in data.split("\n\n"):
        group_total = sum([int(x) for x in group.splitlines()])
        totals.append(group_total)
    return totals


@timeit
def p1():
    with open("./input.txt") as f:
        data = f.read()
    totals = compute_totals(data)
    highest = max(totals)
    return highest


@timeit
def p2():
    with open("./input.txt") as f:
        data = f.read()
    totals = compute_totals(data)
    sum_top_3 = sum(sorted(totals, reverse=True)[:3])
    return sum_top_3


if __name__ == "__main__":
    print("======p1=====")
    p1 = p1()
    print(p1)
    print("======p1=====")
    print("======p2=====")
    p2 = p2()
    print(p2)
    print("======p2=====")
