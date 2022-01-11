import fileinput
import os
import re

import numpy as np


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    return np.array(
        [
            list(map(int, re.split("\\->|,", line.strip())))
            for line in fileinput.input(input_path)
        ]
    ).reshape(-1, 2, 2)


def get_grid(lines):
    max_x = max(lines[:, :, 0].flatten())
    max_y = max(lines[:, :, 1].flatten())
    return np.zeros((max_x + 1, max_y + 1))


def get_score(grid):
    return len(np.argwhere(grid >= 2))


def fill_grid_straight(grid, input):
    for vent in input:
        # Select only straight lines
        compared = np.argwhere(vent[0] - vent[1] == 0)
        if len(compared) > 0:
            axis = compared[0][0]
            path1 = np.arange(min(vent[:, 1 - axis]), max(vent[:, 1 - axis]) + 1)
            vent_size = path1.size
            path2 = np.full(vent_size, vent[0, axis])
            paths = [path1, path2]

            for i in range(vent_size):
                grid[paths[1 - axis][i], paths[axis][i]] += 1

    return get_score(grid)


def fill_grid(grid, input):
    for vent in input:
        loc1, loc2 = vent[0], vent[1]

        if loc1[0] == loc2[0]:
            [start, end] = sorted([loc1, loc2], key=lambda coords: coords[1])
            path = [[start[0], y] for y in range(start[1], end[1] + 1)]
        elif loc1[1] == loc2[1]:
            [start, end] = sorted([loc1, loc2], key=lambda coords: coords[0])
            path = [[x, start[1]] for x in range(start[0], end[0] + 1)]
        else:
            xorder = sorted([loc1, loc2], key=lambda coords: coords[0])
            xpath = list(range(xorder[0][0], xorder[1][0] + 1))

            yorder = sorted([loc1, loc2], key=lambda coords: coords[1])
            ypath = list(range(yorder[0][1], yorder[1][1] + 1))
            if xorder[0].tolist() != yorder[0].tolist():
                ypathrev = list(ypath)[::-1]
                ypath = ypathrev

            path = list(zip(xpath, ypath))
        for loc in path:
            grid[loc[0]][loc[1]] += 1

    return get_score(grid)


def solve_1(input_list):
    grid = get_grid(input_list)
    return fill_grid_straight(grid, input_list)


def solve_2(input_list):
    grid = get_grid(input_list)
    return fill_grid(grid, input_list)


if __name__ == "__main__":
    sample_input = read_file("data/day_5/sample.txt")
    real_input = read_file("data/day_5/input.txt")

    # Part 1
    assert solve_1(sample_input) == 5
    assert solve_1(real_input) == 6283

    # # Part 2
    assert solve_2(sample_input) == 12, solve_2(sample_input)
    assert solve_2(real_input) == 18864
