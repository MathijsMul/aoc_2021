import os
from typing import List


def read_file(input_path: str, line_type: type = int) -> list:
    current_path = os.path.abspath(os.path.dirname(__file__))
    input_path = os.path.join(current_path, "..", "..", input_path)
    return [line_type(line.strip()) for line in open(input_path).readlines()]


def get_increase_count(input_list: List[int]) -> int:
    increase_count = 0
    for idx, depth in enumerate(input_list):
        if idx > 0 and depth > input_list[idx - 1]:
            increase_count += 1
    return increase_count


def get_window_sums(input_list: List[int], window_size: int = 3) -> List[int]:
    window_sums = []
    for idx, _ in enumerate(input_list[: -window_size + 1]):
        window_depths = (input_list[i] for i in range(idx, idx + window_size))
        window_sums.append(sum(window_depths))
    return window_sums


if __name__ == "__main__":
    real_input = read_file("data/day_1/input.txt")
    sample_input = read_file("data/day_1/sample.txt")

    # Part 1
    # sample_solution_1 = get_increase_count(sample_input)
    # assert sample_solution_1 == 7

    solution_1 = get_increase_count(real_input)
    assert solution_1 == 1167

    # Part 2
    sample_solution_2 = get_increase_count(get_window_sums(sample_input))
    assert sample_solution_2 == 5

    solution_2 = get_increase_count(get_window_sums(real_input))
    assert solution_2 == 1130
