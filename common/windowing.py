import typing


def window(lst: typing.List, size: int = 2) -> typing.List:
    return [lst[i : i + size] for i in range(len(lst))]


def sliding_window(
    seq: typing.Sequence, size: int
) -> typing.Generator[typing.Sequence, None, None]:
    for i in range(len(seq) - size + 1):
        yield seq[i : i + size]
