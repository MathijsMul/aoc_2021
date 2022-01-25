import re

import numpy as np

from utils import read_file


def parse_input(input_path: str):
    return np.array(
        [
            list(map(int, re.split("\\->|,", line.strip())))
            for line in read_file(input_path)
        ]
    ).reshape(-1, 2, 2)


def get_grid(lines):
    max_x = max(lines[:, :, 0].flatten())
    max_y = max(lines[:, :, 1].flatten())
    return np.zeros((max_x + 1, max_y + 1))


def get_score(grid):
    return len(np.argwhere(grid >= 2))


def get_straight_path(loc1, loc2, axis):
    [start, end] = sorted([loc1, loc2], key=lambda coords: coords[axis])
    order = axis - (axis == 0)
    return [
        [start[1 - axis], other][::order] for other in range(start[axis], end[axis] + 1)
    ]


def get_diagonal_path(loc1, loc2):
    xx, xy = zip(*get_straight_path(loc1, loc2, 0))
    yx, yy = zip(*get_straight_path(loc1, loc2, 1))

    if [xx[0], xy[0]] != [yx[0], yy[0]]:
        yy = list(yy)[::-1]

    return list(zip(xx, yy))


def get_path(vent, diagonals):
    for axis in [0, 1]:
        if vent[0, axis] == vent[1, axis]:
            return get_straight_path(vent[0], vent[1], 1 - axis)
    if diagonals:
        return get_diagonal_path(vent[0], vent[1])


def fill_grid(grid, input, diagonals=False):
    for vent in input:
        path = get_path(vent, diagonals)
        if path:
            for loc in path:
                grid[loc[0], loc[1]] += 1
    return get_score(grid)


def solve_1(input_list):
    grid = get_grid(input_list)
    return fill_grid(grid, input_list)


def solve_2(input_list):
    grid = get_grid(input_list)
    return fill_grid(grid, input_list, diagonals=True)


if __name__ == "__main__":
    sample_input = parse_input("data/day_5/sample.txt")
    real_input = parse_input("data/day_5/input.txt")

    # Part 1
    assert solve_1(sample_input) == 5
    assert solve_1(real_input) == 6283

    # Part 2
    assert solve_2(sample_input) == 12, solve_2(sample_input)
    assert solve_2(real_input) == 18864
