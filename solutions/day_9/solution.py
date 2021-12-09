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
    shape = input_array.shape
    adjacent_nrs = []
    if x != 0:
        adjacent_nrs.append(input_array[x - 1, y])
    if x != shape[0] - 1:
        adjacent_nrs.append(input_array[x + 1, y])
    if y != 0:
        adjacent_nrs.append(input_array[x, y - 1])
    if y != shape[1] - 1:
        adjacent_nrs.append(input_array[x, y + 1])
    return adjacent_nrs


def get_adjacent_indices(input_array, x, y):
    shape = input_array.shape
    adjacent_indices = []
    if x != 0:
        adjacent_indices.append([x - 1, y])
    if x != shape[0] - 1:
        adjacent_indices.append([x + 1, y])
    if y != 0:
        adjacent_indices.append([x, y - 1])
    if y != shape[1] - 1:
        adjacent_indices.append([x, y + 1])
    return adjacent_indices


def get_basin_neighbors(input_array, x, y):
    neighbour_indices = get_adjacent_indices(input_array, x, y)
    return [n for n in neighbour_indices if input_array[n[0],n[1]] != 9]


def solve_2(input_array: np.ndarray):
    shape = input_array.shape
    basins = []
    # added = np.zeros(shape)
    added = []
    for x in range(shape[0]):
        for y in range(shape[1]):
            if input_array[x, y] == 9:
                continue
            # if added[x,y] == 1:
            #     continue
            else:
                # neighbors = get_basin_neighbors(input_array, x, y)
                current_locs = [[x,y]] + get_basin_neighbors(input_array, x, y)
                current_locs = [",".join(map(str, l)) for l in current_locs]
                found = False
                for basin in basins:
                    if any(loc in basin for loc in current_locs):
                        for location in current_locs:
                            basin.append(location)
                            # if added[location[0], location[1]] != 1 and location not in basin:
                            # if location not in basin and ",".join(map(str, location)) not in added:
                            #if ",".join(map(str, location)) not in added:
                            # if location not in added:
                            #     basin.append(location)
                            #     added.append(location)
                                # basin.append(",".join(map(str, location)))
                                # added[location[0], location[1]] = 1
                                # added.append(",".join(map(str, location)))
                        found = True
                if not found:
                    basins.append(current_locs)

    # print(basins)
    # for basin in basins:
    #     array = np.zeros(shape)
    #     for loc in basin:
    #         array[loc[0],loc[1]] = 1
    #     print(array)
    #     print("\n")
    basins = [list(set(b)) for b in basins]

    basin_sizes = sorted([len(basin) for basin in basins], reverse = True)
    print(basin_sizes)


    assert sum(basin_sizes) + len(np.argwhere(input_array == 9)) == input_array.size

    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


if __name__ == "__main__":
    sample_input = read_file("data/day_9/sample.txt")
    real_input = read_file("data/day_9/input.txt")

    assert solve_1(sample_input) == 15
    assert solve_1(real_input) == 580

    # Part 2
    # get_basins(sample_input)
    # print(solve_2(sample_input))
    assert solve_2(sample_input) == 1134
    print(solve_2(real_input))

    # 770224 too low
    # 557280
    # assert solve_2(real_input) == ..., solve_2(real_input)
