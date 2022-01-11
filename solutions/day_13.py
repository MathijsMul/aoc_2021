import os

import matplotlib.pyplot as plt
import numpy as np


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    dots, folds = [], []
    for line in open(input_path).readlines():
        if "," in line:
            dots.append(tuple(map(int, line.strip().split(","))))
        elif "fold" in line:
            folds.append((int("x" in line), int(line.strip().split("=")[-1])))
    xcoords, ycoords = zip(*dots)
    array = np.zeros((max(ycoords) + 1, max(xcoords) + 1))
    array[ycoords, xcoords] = 1
    return array, folds


def fold(dots, folds):
    for axis, idx in folds:
        dots = np.delete(dots, idx, axis)
        left, right = np.split(dots, [idx], axis)
        right_flipped = np.flip(right, axis)
        right_flipped = np.pad(
            right_flipped,
            (
                (left.shape[0] - right_flipped.shape[0], 0),
                (left.shape[1] - right_flipped.shape[1], 0),
            ),
        )
        dots = left + right_flipped
    dots[dots > 0] = 1
    return dots


def solve_1(input):
    dots, folds = input
    dots = fold(dots, folds[:1])
    return len(np.argwhere(dots > 0))


def visualize_dots(dot_array):
    plt.imshow(dot_array)
    plt.axis("off")
    plt.show()


def solve_2(input):
    dots = fold(*input)
    visualize_dots(dots)


if __name__ == "__main__":
    sample1_input = read_file("data/day_13/sample1.txt")
    real_input = read_file("data/day_13/input.txt")

    # Part 1
    assert solve_1(sample1_input) == 17, solve_1(sample1_input)
    assert solve_1(real_input) == 788

    # Part 2
    solve_2(real_input)
