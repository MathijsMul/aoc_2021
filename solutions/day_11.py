from itertools import product

import numpy as np

from utils import read_file


def parse_input(input_path: str):
    return np.array(
        [list(map(int, list(line.strip()))) for line in read_file(input_path)]
    )


def get_adjacent_indices(input_array, x, y):
    shape = input_array.shape
    neighborhood = product(range(x - 1, x + 2), range(y - 1, y + 2))
    return filter(
        lambda loc: loc != (x, y) and loc in product(range(shape[0]), range(shape[1])),
        neighborhood,
    )


def flash(array, flash_idx=0):
    for flash_idx, (x, y) in enumerate(np.argwhere(array == 10)):
        for loc in get_adjacent_indices(array, x, y):
            if array[loc] not in [10, -1]:
                array[loc] += 1
        array[x, y] = -1
    return flash_idx + 1


def simulate_step(array: np.ndarray) -> (np.ndarray, int):
    num_flashes = 0
    array += 1
    while array[array == 10].size > 0:
        num_flashes += flash(array)
    array[array == -1] = 0
    return array, num_flashes


def solve_1(input_array: np.ndarray, num_steps: int = 100) -> int:
    return sum(simulate_step(input_array)[1] for _ in range(num_steps))


def solve_2(input_array: np.ndarray) -> int:
    step = 0
    while input_array[input_array == 0].size < input_array.size:
        input_array, _ = simulate_step(input_array)
        step += 1
    return step


if __name__ == "__main__":
    # Part 1
    sample_input = parse_input("data/day_11/sample.txt")
    real_input = parse_input("data/day_11/input.txt")
    assert solve_1(sample_input) == 1656, solve_1(sample_input)
    assert solve_1(real_input) == 1686

    # Part 2
    sample_input = parse_input("data/day_11/sample.txt")
    real_input = parse_input("data/day_11/input.txt")
    assert solve_2(sample_input) == 195, solve_2(sample_input)
    assert solve_2(real_input) == 360, solve_2(real_input)
