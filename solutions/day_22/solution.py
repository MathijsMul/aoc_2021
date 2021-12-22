import os
from collections import defaultdict, Counter
import numpy as np
from scipy.sparse import lil_matrix


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    steps = []
    for line in open(input_path).readlines():
        # print(line)
        sign = None
        if line.startswith("on"):
            sign = 1
        elif line.startswith("off"):
            sign = 0

        ranges = []
        range_strs = line.split(" ")[1].split(",")
        for range_str in range_strs:
            range = tuple(map(int, range_str.split("=")[1].split("..")))
            ranges.append(range)
        steps.append((sign, ranges))
    return steps


def solve_1(steps):
    states = np.zeros((101, 101, 101))
    for step in steps:
        sign, [range_x, range_y, range_z] = step
        states[
            range_x[0] + 50: range_x[1] + 51,
            range_y[0] + 50: range_y[1] + 51,
            range_z[0] + 50: range_z[1] + 51,
        ] = sign

    return np.sum(states)


def solve_2(steps):
    # states = np.zeros((101, 101, 101))
    xmin, xmax, ymin, ymax, zmin, zmax = 0,0,0,0,0,0
    for step in steps:
        _, [(x0, x1), (y0,y1), (z0,z1)] = step
        if x0 < xmin:
            xmin = x0
        if x1 > xmax:
            xmax = x1
        if y0 < ymin:
            ymin = y0
        if y1 > ymax:
            ymax = y1
        if z0 < zmin:
            zmin = z0
        if z1 > zmax:
            zmax = z1
    xmax += 1
    ymax += 1
    zmax += 1
    # states = np.zeros((xmax - xmin, ymax - ymin, zmax - zmin), dtype="uint8")
    states = lil_matrix((xmax - xmin, ymax - ymin, zmax - zmin), dtype=np.int8)

    for step in steps:
        sign, [range_x, range_y, range_z] = step
        states[
            range_x[0] - xmin: range_x[1] - xmin + 1,
            range_y[0] - ymin: range_y[1] - ymin + 1,
            range_z[0] - zmin: range_z[1] - zmin + 1,
        ] = sign

    return np.sum(states)


if __name__ == "__main__":
    sample1_input = read_file("data/day_22/sample1.txt")
    sample2_input = read_file("data/day_22/sample2.txt")
    sample3_input = read_file("data/day_22/sample3.txt")
    real_input = read_file("data/day_22/input.txt")

    # Part 1
    assert solve_1(sample1_input) == 39, solve_1(sample1_input)
    assert solve_1(sample2_input) == 590784, solve_1(sample2_input)
    assert solve_1(real_input) == 551693

    # Part 2
    # assert solve_2(sample1_input) == ..., solve_2(sample1_input)
    # assert solve_2(sample2_input) == ..., solve_2(sample2_input)
    # assert solve_2(sample3_input) == 2758514936282235, solve_2(sample3_input)
    # print(solve_2(real_input))
    # assert solve_2(real_input) == ...
