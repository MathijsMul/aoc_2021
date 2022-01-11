from functools import reduce

import numpy as np

from utils import read_file


def parse_input(input_path: str):
    content = read_file(input_path)
    order = list(map(int, content[0].strip().split(",")))
    boards = np.array(
        list(map(int, reduce(lambda x, y: x + y, content[1:]).split()))
    ).reshape(-1, 5, 5)
    return order, boards


def compute_score(board, bool_board, last_nr):
    sum_remaining_nrs = np.sum(((1 - bool_board) * board).flatten())
    return sum_remaining_nrs * last_nr


def winner(board):
    return any(x == 5 for x in board.sum(0)) or any(x == 5 for x in board.sum(1))


def check_board(drawn_nrs, board):
    bingo_bools = np.zeros((5, 5))
    for nr in drawn_nrs:
        bingo_locations = np.argwhere(board == nr)
        for loc in bingo_locations:
            bingo_bools[loc[0], loc[1]] = 1
        if winner(bingo_bools):
            return compute_score(board, bingo_bools, nr)


def get_scores(drawn_nrs, boards):
    winning_boards, scores = [], []

    for idx, nr in enumerate(drawn_nrs):
        for board_idx, board in enumerate(boards):
            if board_idx not in winning_boards:
                score = check_board(drawn_nrs[: idx + 1], board)
                if score is not None:
                    winning_boards.append(board_idx)
                    scores.append(score)
    return scores


def solve_1(drawn_nrs, boards):
    return get_scores(drawn_nrs, boards)[0]


def solve_2(drawn_nrs, boards):
    return get_scores(drawn_nrs, boards)[-1]


if __name__ == "__main__":
    sample_order, sample_boards = parse_input("data/day_4/sample.txt")
    order, boards = parse_input("data/day_4/input.txt")

    # Part 1
    assert solve_1(sample_order, sample_boards) == 4512
    assert solve_1(order, boards) == 49686, solve_1(order, boards)

    # Part 2
    assert solve_2(sample_order, sample_boards) == 1924
    assert solve_2(order, boards) == 26878, solve_2(order, boards)
