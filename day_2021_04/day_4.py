from common.timing import timeit
import typing

PLAY_MARKER = "x"
GRID_ROW_SIZE = 5

BOARD = typing.List[typing.List]


def parse(filename: str) -> (typing.List[int], typing.List[BOARD]):
    with open(filename, "r") as f:
        plays = [int(p) for p in f.readline().rstrip().split(",")]
        _ = f.readline()
        raw = [line.rstrip() for line in f.readlines()]
        boards = []
        board = []
        raw.append("")
        for r in raw:
            if r != "":
                board.append([int(n) for n in r.split()])
            else:
                boards.append(board)
                board = []
    return plays, boards


def is_winner(board: BOARD) -> bool:
    for row in board:
        if row.count(PLAY_MARKER) == GRID_ROW_SIZE:
            return True

    for i in range(GRID_ROW_SIZE):
        col = [row[i] for row in board]
        if col.count(PLAY_MARKER) == GRID_ROW_SIZE:
            return True

    return False


def play_board(number_to_play: int, board: BOARD) -> BOARD:
    for i, row in enumerate(board):
        for j, number in enumerate(row):
            if number == number_to_play:
                board[i][j] = PLAY_MARKER
                return board
    return board


def sum_board(board) -> int:
    sum_ = 0
    for row in board:
        for number in row:
            if number != PLAY_MARKER:
                sum_ += number
    return sum_


@timeit
def p1():
    plays, boards = parse("./input.txt")
    for play in plays:
        for board in boards:
            play_board(play, board)
            if is_winner(board):
                print(play * sum_board(board))
                return


@timeit
def p2():
    plays, boards = parse("./input.txt")
    for play in plays:
        boards = [board for board in boards if not is_winner(board)]
        for board in boards:
            play_board(play, board)
        if len(boards) <= 1 and is_winner(board):
            print(play * sum_board(boards[0]))
            break


if __name__ == "__main__":
    print("======p1=====")
    p1()
    print("======p1=====")
    print("======p2=====")
    p2()
    print("======p2=====")
