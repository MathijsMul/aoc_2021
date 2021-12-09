import os
import numpy as np


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    all_input = []
    for line_idx, line in enumerate(open(input_path).readlines()):
        all_input.append(list(map(int, list(line.strip().split()[0]))))
    return np.array(all_input).reshape((line_idx + 1, -1))


def solve_1(input_array: np.ndarray):
    shape = input_array.shape
    min_bools = np.zeros(shape)
    for x in range(shape[0]):
        for y in range(shape[1]):
            # print(f"Current nr: {input_array[x,y]} at {x,y}")
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
    return [n for n in neighbour_indices if input_array[n[0], n[1]] != 9]


def solve_2(input_array: np.ndarray):
    shape = input_array.shape
    basins = []
    for x in range(shape[0]):
        for y in range(shape[1]):
            if input_array[x, y] != 9:
                basin_neighbor_indices = set(get_basin_neighbors(input_array, x, y))
                existing_basin = False
                for basin in basins:
                    for loc in basin_neighbor_indices:
                        if loc in basin:
                            basin.update(basin_neighbor_indices)
                            existing_basin = True

                if not existing_basin:
                    basins.append(basin_neighbor_indices)

    while (
        not sum([len(b) for b in basins]) + len(np.argwhere(input_array == 9))
        == input_array.size
    ):
        for idx1, basin1 in enumerate(basins):
            for idx2, basin2 in enumerate(basins):
                if idx2 > idx1 and len(basin1.intersection(basin2)) > 0:
                    basin1.update(basin2)
                    basin2.clear()

    sizes = sorted([len(b) for b in basins], reverse=True)
    return sizes[0] * sizes[1] * sizes[2]


if __name__ == "__main__":
    sample_input = read_file("data/day_9/sample.txt")
    sample2_input = read_file("data/day_9/sample2.txt")
    real_input = read_file("data/day_9/input.txt")

    assert solve_1(sample_input) == 15
    assert solve_1(real_input) == 580

    # Part 2
    assert solve_2(sample_input) == 1134
    assert solve_2(sample2_input) == 1260
    assert solve_2(real_input) == 856716
