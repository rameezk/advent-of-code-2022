from common.timing import timeit


@timeit
def p1():
    with open("./input.txt", "r") as f:
        report = f.read().splitlines()

    gamma = ""
    epsilon = ""
    for i in range(len(report[0])):
        bits = [x[i] for x in report]
        bit_0_count = bits.count("0")
        bit_1_count = bits.count("1")
        gamma += "1" if bit_1_count > bit_0_count else "0"
        epsilon += "0" if bit_1_count > bit_0_count else "1"
    print(int(gamma, 2) * int(epsilon, 2))


def solve(significant: bool) -> int:
    with open("./input.txt", "r") as f:
        report = f.read().splitlines()

    for i in range(len(report[0])):
        if len(report) <= 1:
            break
        bits = [r[i] for r in report]
        if significant:
            check_bit = "1" if bits.count("1") >= bits.count("0") else "0"
        else:
            check_bit = "0" if bits.count("1") >= bits.count("0") else "1"
        report = [r for r in report if r[i] == check_bit]

    return int(report[0], 2)


@timeit
def p2():
    o2 = solve(significant=True)
    co2 = solve(significant=False)
    print(o2 * co2)


if __name__ == "__main__":
    print("======p1=====")
    p1()
    print("======p1=====")
    print("======p2=====")
    p2()
    print("======p2=====")
