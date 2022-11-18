import typing


def read_file_as_int_list(file_name: str) -> typing.List:
    with open(file_name, "r") as f:
        data = [int(line) for line in f]
        return data
