import os

import matplotlib.pyplot as plt
import numpy as np


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    dots = []
    folds = []
    for line in open(input_path).readlines():
        if "," in line:
            dots.append(list(map(int, line.strip().split(","))))
        elif "fold along x" in line:
            folds.append((0, int(line.strip().split("=")[-1])))
        elif "fold along y" in line:
            folds.append((1, int(line.strip().split("=")[-1])))
    xcoords, ycoords = zip(*dots)
    array = np.zeros((max(xcoords)+1, max(ycoords)+1))
    for loc in dots:
        array[loc[0],loc[1]] = 1
    return array, folds


def solve_1(input):
    dots, folds = input
    for dim, axis in folds[:1]:
        if dim == 1:
            left = dots[:,:axis]
            right = dots[:,axis+1:]
            right_flipped = np.flip(right, 1)
        elif dim == 0:
            left = dots[:axis,:]
            right = dots[axis+1:,:]
            right_flipped = np.flip(right, 0)
        dots = left + right_flipped
    return len(np.argwhere(dots > 0))


def solve_2(input):
    dots, folds = input
    for dim, axis in folds:
        if dim == 1:
            left = dots[:,:axis]
            right = dots[:,axis+1:]
            right_flipped = np.flip(right, 1)
            if left.shape != right_flipped.shape:
                right_flipped = np.pad(right_flipped, ((0, 0), (1, 0)))
        elif dim == 0:
            left = dots[:axis,:]
            right = dots[axis+1:,:]
            right_flipped = np.flip(right, 0)
            assert left.shape == right_flipped.shape

        dots = left + right_flipped
    dots[dots > 0] = 1
    dots = dots.T
    return dots


if __name__ == "__main__":
    sample1_input = read_file("data/day_13/sample1.txt")
    real_input = read_file("data/day_13/input.txt")

    # Part 1
    assert solve_1(sample1_input) == 17, solve_1(sample1_input)
    assert solve_1(real_input) == 788

    # Part 2
    code = solve_2(real_input)
    plt.imshow(code)
    plt.show()
