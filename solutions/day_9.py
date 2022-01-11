from functools import reduce
from itertools import product

import numpy as np

from utils import read_file


def parse_input(input_path: str):
    all_input = []
    for line_idx, line in enumerate(read_file(input_path)):
        all_input.append(list(map(int, list(line.strip().split()[0]))))
    return np.array(all_input).reshape((line_idx + 1, -1))


def solve_1(input_array: np.ndarray):
    shape = input_array.shape
    min_bools = np.zeros(shape)
    for x in range(shape[0]):
        for y in range(shape[1]):
            adjacent_nrs = get_adjacent_nrs(input_array, x, y)
            if min(adjacent_nrs) > input_array[x, y]:
                min_bools[x, y] = 1
    return sum((min_bools * (input_array + 1)).flatten())


def get_adjacent_nrs(input_array, x, y):
    adjacent_indices = get_adjacent_indices(input_array, x, y)
    return [input_array[loc[0], loc[1]] for loc in adjacent_indices]


def get_adjacent_indices(input_array, x, y):
    shape = input_array.shape
    adjacent_indices = []
    if x != 0:
        adjacent_indices.append((x - 1, y))
    if x != shape[0] - 1:
        adjacent_indices.append((x + 1, y))
    if y != 0:
        adjacent_indices.append((x, y - 1))
    if y != shape[1] - 1:
        adjacent_indices.append((x, y + 1))
    return adjacent_indices


def get_basin_neighbors(input_array, x, y):
    neighbour_indices = get_adjacent_indices(input_array, x, y) + [(x, y)]
    return {n for n in neighbour_indices if input_array[n[0], n[1]] != 9}


def solve_2(input_array: np.ndarray):
    shape = input_array.shape
    basins = []
    for x, y in product(range(shape[0]), range(shape[1])):
        if input_array[x, y] == 9:
            continue

        basin_neighbor_indices = get_basin_neighbors(input_array, x, y)
        existing_basin = False
        for basin in basins:
            if any(loc in basin for loc in basin_neighbor_indices):
                basin.update(basin_neighbor_indices)
                existing_basin = True
        if not existing_basin:
            basins.append(basin_neighbor_indices)

    while (
        not sum([len(b) for b in basins]) + len(np.argwhere(input_array == 9))
        == input_array.size
    ):
        for idx_left, basin_left in enumerate(basins):
            for idx_right, basin_right in enumerate(basins[idx_left + 1 :]):
                if len(basin_left.intersection(basin_right)) > 0:
                    basin_left.update(basin_right)
                    basin_right.clear()

    return reduce(lambda a, b: a * b, sorted([len(b) for b in basins])[-3:])


if __name__ == "__main__":
    sample_input = parse_input("data/day_9/sample.txt")
    sample2_input = parse_input("data/day_9/sample2.txt")
    real_input = parse_input("data/day_9/input.txt")

    assert solve_1(sample_input) == 15
    assert solve_1(real_input) == 580

    # Part 2
    assert solve_2(sample_input) == 1134
    assert solve_2(sample2_input) == 1260
    assert solve_2(real_input) == 856716
