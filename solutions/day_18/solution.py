import os
from collections import defaultdict, Counter
import numpy as np


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    return [line.strip().split("-") for line in open(input_path).readlines()]


def solve_1(input_list):
    return


def solve_2(input_list):
    return


if __name__ == "__main__":
    sample1_input = read_file("data/day_18/sample1.txt")
    sample2_input = read_file("data/day_18/sample2.txt")
    sample3_input = read_file("data/day_18/sample3.txt")
    real_input = read_file("data/day_18/input.txt")

    # Part 1
    assert solve_1(sample1_input) == ..., solve_1(sample1_input)
    # assert solve_1(sample2_input) == ..., solve_1(sample2_input)
    # assert solve_1(sample3_input) == ..., solve_1(sample3_input)
    # print(solve_1(real_input))
    # assert solve_1(real_input) == ...

    # Part 2
    # assert solve_2(sample1_input) == ..., solve_2(sample1_input)
    # assert solve_2(sample2_input) == ..., solve_2(sample2_input)
    # assert solve_2(sample3_input) == ..., solve_2(sample3_input)
    # print(solve_2(real_input))
    # assert solve_2(real_input) == ...
