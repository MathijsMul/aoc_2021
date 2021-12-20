import os
from itertools import product

import numpy as np


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    sections = []
    section = []

    for idx, line in enumerate(open(input_path).readlines()):
        if line == "\n":
            sections.append(section)
            section = []
        else:
            section.append(list(line.strip()))

    sections.append(section)
    algo = [l for m in sections[0] for l in m]
    algo = "".join(algo)
    image = np.array(sections[1]).reshape(len(sections[1]), len(sections[1][0]))
    return algo, image


def get_surrounding_indices(x, y):
    return list(product(range(x - 1, x + 2), range(y - 1, y + 2)))


def get_value_string(array, locs, pad_value):
    output_str = ""
    for loc in locs:
        try:
            value = array[loc]
        except IndexError:
            value = str(pad_value)

        if isinstance(value, float):
            value = int(value)
        output_str += str(value)
    return output_str


def str_to_int(value_str):
    value_str = value_str.replace(".", "0").replace("#", "1")
    return int(value_str, 2)


def solve(algo, input_image, n_iter=2):
    pad_value = 0

    for i in range(n_iter):
        if algo[0] == "#" and algo[-1] == ".":
            if i % 2 == 0:
                pad_value = 0
            else:
                pad_value = 1

        input_image = np.pad(input_image, 2, "constant", constant_values=(pad_value))
        out = np.zeros(input_image.shape)
        for x in range(input_image.shape[0]):
            for y in range(input_image.shape[1]):
                ids = get_surrounding_indices(x, y)
                value_str = get_value_string(input_image, ids, pad_value)
                value = str_to_int(value_str)
                new_value = algo[value]
                if new_value == "#":
                    new_value = 1
                elif new_value == ".":
                    new_value = 0
                out[x, y] = new_value
        input_image = out

    return int(np.sum(out))


if __name__ == "__main__":
    sample1_input = read_file("data/day_20/sample1.txt")
    real_input = read_file("data/day_20/input.txt")

    # Part 1
    algo1, image1 = sample1_input
    assert solve(algo1, image1) == 35

    algo, image = real_input
    assert solve(algo, image) == 5301

    # Part 2
    assert solve(algo1, image1, 50) == 3351
    assert solve(algo, image, 50) == 19492
