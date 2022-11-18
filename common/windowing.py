import typing


def window(lst: typing.List, size: int = 2) -> typing.List:
    return [lst[i : i + size] for i in range(len(lst))]
