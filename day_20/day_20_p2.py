from common.timing import timeit


def new_index(loc, by, s):
    return (loc + by) % (s - 1)


def rebuild_from_indices(indices, values):
    return list(map(lambda idx: values[idx], indices))


def shift(l, i_s, i, s):
    by = l[i]
    loc = i_s.index(i)
    i_s.pop(loc)
    insert_at = new_index(loc, by, s)
    i_s.insert(insert_at, i)
    return by


@timeit
def solve_p2():
    with open("./input.txt") as file:
        enc_file = list(map(lambda n: int(n) * 811589153, file.readlines()))

    s = len(enc_file)
    indices = list(range(s))

    for _ in range(10):
        for idx in range(s):
            shift(enc_file, indices, idx, s)

    nl = rebuild_from_indices(indices, enc_file)
    p_0 = nl.index(0)

    return nl[(1000 + p_0) % s] + nl[(2000 + p_0) % s] + nl[(3000 + p_0) % s]


if __name__ == "__main__":
    p2 = solve_p2()
    print(p2)
