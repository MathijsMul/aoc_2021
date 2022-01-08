import os

import numpy as np


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    with open(input_path) as file:
        lines = file.readlines()
        array = np.zeros((len(lines), len(lines[0]) - 1))
        for line_idx, line in enumerate(lines):
            for char_idx, char in enumerate(line.strip()):
                if char == ">":
                    array[line_idx, char_idx] = 1
                elif char == "v":
                    array[line_idx, char_idx] = -1
    return array


def step_dir(in_array, out_array, dir):
    length, width = in_array.shape
    for length_idx in range(length):
        for width_idx in range(width):
            value = in_array[length_idx, width_idx]
            if value == dir and dir == 1:
                adj_pos = (length_idx, (width_idx + 1) % width)
                can_move = in_array[adj_pos] == 0
            elif value == dir and dir == -1:
                adj_pos = ((length_idx + 1) % length, width_idx)
                can_move = in_array[adj_pos] != -1 and out_array[adj_pos] == 0
            else:
                continue

            if can_move:
                out_array[adj_pos] = dir
            else:
                out_array[length_idx, width_idx] = dir

    return out_array


def step(in_array):
    out_array = np.zeros(in_array.shape)
    for cucumber_direction in [1, -1]:
        out_array = step_dir(in_array, out_array, cucumber_direction)
    return out_array


def solve(cucumber_array):
    out_array = step(cucumber_array)
    num_steps = 1

    while not np.array_equal(out_array, cucumber_array):
        cucumber_array = out_array
        out_array = step(cucumber_array)
        num_steps += 1

    return num_steps


if __name__ == "__main__":
    sample_input = read_file("data/day_25/sample.txt")
    real_input = read_file("data/day_25/input.txt")

    assert solve(sample_input) == 58
    assert solve(real_input) == 549
