import fileinput
import os

import numpy as np


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )

    boards = []
    board = []
    for idx, line in enumerate(fileinput.input(input_path)):
        if idx == 0:
            order = [int(nr) for nr in line.split(",")]
        elif (idx - 1) % 6 == 0:
            if len(board) > 0:
                boards.append(board)
            board = []
        else:
            board.append([int(x) for x in line.split()])
    boards.append(board)

    for board in boards:
        assert len(board) == 5
        for row in board:
            assert len(row) == 5

    boards = [np.array(board) for board in boards]
    return order, boards


def compute_score(board, bool_board, last_nr):
    sum_remaining_nrs = np.sum(((1 - bool_board) * board).flatten())
    return sum_remaining_nrs * last_nr


def check_board(drawn_nrs, board):
    bingo_bools = np.zeros((5, 5))
    for nr in drawn_nrs:
        bingo_locations = np.argwhere(board == nr)
        for loc in bingo_locations:
            bingo_bools[loc[0]][loc[1]] = 1

        if any(x == 5 for x in bingo_bools.sum(0)) or any(
            x == 5 for x in bingo_bools.sum(1)
        ):
            return compute_score(board, bingo_bools, nr)


def solve(drawn_nrs, boards):
    winning_boards = []

    for idx, nr in enumerate(drawn_nrs):
        for board_idx, board in enumerate(boards):
            res = check_board(drawn_nrs[: idx + 1], board)
            if res is not None and board_idx not in winning_boards:
                winning_boards.append(board_idx)
                print(f"Board {board_idx} wins with score {res}")


if __name__ == "__main__":
    sample_order, sample_boards = read_file("data/day_4/sample.txt")
    order, boards = read_file("data/day_4/input.txt")

    # Part 1 & 2
    # solve(sample_order, sample_boards)
    solve(order, boards)
