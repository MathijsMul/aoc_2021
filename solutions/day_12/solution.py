import os
import numpy as np
from itertools import product


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    return np.array(
        [list(map(int, list(line.strip()))) for line in open(input_path).readlines()]
    )


def solve_1(input_array):
    return


def solve_2(input_array):
    return


if __name__ == "__main__":
    sample_input = read_file("data/day_12/sample.txt")
    real_input = read_file("data/day_12/input.txt")

    # Part 1
    assert solve_1(sample_input) == ..., solve_1(sample_input)
    # print(solve_1(real_input))
    # assert solve_1(real_input) == ...

    # Part 2
    # assert solve_2(sample_input) == ..., solve_2(sample_input)
    # print(solve_2(real_input))
    # assert solve_2(real_input) == ..., solve_2(real_input)
