import fileinput
import os

import numpy as np
from functools import reduce


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    content = fileinput.input(input_path)

    order = map(int, next(content).strip().split(","))
    boards = np.array(
        list(map(int, reduce(lambda x, y: x + y, content).split()))
    ).reshape(-1, 5, 5)

    return order, boards


def compute_score(boards, bool_board, board_idx, last_nr):
    return last_nr * np.sum(
        (bool_board[board_idx] * boards[board_idx]).flatten()
    )


def solve(drawn_nrs, boards):
    winning_boards = []
    hits = np.ones(boards.shape)

    while len(winning_boards) < boards.shape[0]:
        nr = next(drawn_nrs)
        hits[boards == nr] = 0
        winning_locs = np.argwhere(np.stack([hits.sum(dim) for dim in [1, 2]]) == 0)

        if len(winning_locs) > 0:
            winning_board_idx = winning_locs[0][1]
            if winning_board_idx not in winning_boards:
                res = compute_score(boards, hits, winning_board_idx, nr)
                winning_boards.append(winning_board_idx)
                print(f"Board {winning_board_idx} wins with score {res}")


if __name__ == "__main__":
    sample_order, sample_boards = read_file("data/day_4/sample.txt")
    order, boards = read_file("data/day_4/input.txt")
    # print(sample_order)
    # print(sample_boards)

    # Part 1 & 2
    # solve(sample_order, sample_boards)
    solve(order, boards)

    """
    part 1
    sample 4512
    real 49686
    
    part 2 
    sample 1924
    real 26878
    """
