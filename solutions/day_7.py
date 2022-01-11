import numpy as np

from utils import read_file


def parse_input(input_path: str):
    return np.array(list(map(int, read_file(input_path)[0].strip().split(","))))


def get_distances(input):
    costs = np.ones((input.size, max(input))) * np.arange(max(input))
    return np.abs(costs - input.reshape(input.size, -1))


def get_min_costs(matrix):
    return min(matrix.sum(0))


def solve_1(input):
    costs = get_distances(input)
    return get_min_costs(costs)


def solve_2(input):
    distances = get_distances(input)
    costs = (distances * (distances + 1)) // 2
    return get_min_costs(costs)


if __name__ == "__main__":
    sample_input = parse_input("data/day_7/sample.txt")
    real_input = parse_input("data/day_7/input.txt")

    # Part 1
    assert solve_1(sample_input) == 37
    assert solve_1(real_input) == 342730

    # Part 2
    assert solve_2(sample_input) == 168
    assert solve_2(real_input) == 92335207
