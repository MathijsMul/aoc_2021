import numpy as np

from utils import read_file


def parse_input(input_path: str):
    lines = read_file(input_path)
    array = np.zeros((len(lines), len(lines[0]) - 1))
    for line_idx, line in enumerate(lines):
        for char_idx, char in enumerate(line.strip()):
            if char == ">":
                array[line_idx, char_idx] = 1
            elif char == "v":
                array[line_idx, char_idx] = -1
    return array


def step_dir(in_array, out_array, dir):
    """Move in one direction."""
    length, width = in_array.shape
    for x in range(length):
        for y in range(width):
            if in_array[x, y] == dir:
                adj_pos = ((x + (dir == -1)) % length, (y + (dir == 1)) % width)
                can_move = (dir == 1 and in_array[adj_pos] == 0) or (
                    dir == -1 and in_array[adj_pos] != -1 and out_array[adj_pos] == 0
                )
            else:
                continue

            if can_move:
                out_array[adj_pos] = dir
            else:
                out_array[x, y] = dir

    return out_array


def step(in_array):
    """Simulate a step by moving in both directions in the right order."""
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
    sample_input = parse_input("data/day_25/sample.txt")
    real_input = parse_input("data/day_25/input.txt")

    assert solve(sample_input) == 58
    assert solve(real_input) == 549
