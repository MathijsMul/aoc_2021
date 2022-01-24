from itertools import product

import numpy as np

from utils import read_file


def parse_input(input_path: str):
    sections, section = [], []

    for idx, line in enumerate(read_file(input_path)):
        if line == "\n":
            sections.append(section)
            section = []
        else:
            section.append(list(line.strip()))

    sections.append(section)
    algo = "".join(l for m in sections[0] for l in m)
    image = np.array(sections[1]).reshape(len(sections[1]), len(sections[1][0]))
    return algo, image


def get_surrounding_indices(x, y):
    return list(product(range(x - 1, x + 2), range(y - 1, y + 2)))


def get_int_value(array, locs, pad_value):
    output_str = ""
    for loc in locs:
        try:
            value = array[loc]
        except IndexError:
            value = str(pad_value)

        if isinstance(value, float):
            value = int(value)
        output_str += str(value)
    return str_to_int(output_str)


def str_to_int(value_str):
    value_str = value_str.replace(".", "0").replace("#", "1")
    return int(value_str, 2)


def solve(algo, input_image, n_iter=2, pad_value=0, out=None):
    for iter_idx in range(n_iter):
        if algo[0] == "#" and algo[-1] == ".":
            pad_value = iter_idx % 2

        input_image = np.pad(input_image, 2, constant_values=pad_value)
        out = np.zeros(input_image.shape)
        for x in range(input_image.shape[0]):
            for y in range(input_image.shape[1]):
                ids = get_surrounding_indices(x, y)
                new_value = algo[get_int_value(input_image, ids, pad_value)]
                if new_value in ["#", "."]:
                    new_value = new_value == "#"
                out[x, y] = new_value
        input_image = out

    return int(np.sum(out))


if __name__ == "__main__":
    sample_algo, sample_image = parse_input("data/day_20/sample1.txt")
    algo, image = parse_input("data/day_20/input.txt")

    # Part 1
    assert solve(sample_algo, sample_image) == 35
    assert solve(algo, image) == 5301

    # Part 2
    assert solve(sample_algo, sample_image, 50) == 3351
    assert solve(algo, image, 50) == 19492
