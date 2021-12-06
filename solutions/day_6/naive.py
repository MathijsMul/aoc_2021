import fileinput
import os
from typing import List, Tuple, Callable, Iterable
import numpy as np
import re


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    return list(map(int, open(input_path).readlines()[0].strip().split(",")))


def simulate_population(population, num_days):
    for day in range(num_days):
        print(day)
        size = len(population)
        for idx, fish in enumerate(population[:size]):
            if fish > 0:
                population[idx] -= 1
            elif fish == 0:
                population[idx] = 6
                population.append(8)

        print(f"After {day+1} days: {len(population)}")
    return len(population)


def solve_1(input_list):
    return simulate_population(input_list, 80)


def solve_2(input_list):
    return simulate_population(input_list, 256)



if __name__ == "__main__":
    sample_input = read_file("data/day_6/sample.txt")
    real_input = read_file("data/day_6/input.txt")

    # Part 1
    assert solve_1(sample_input) == 5934
    assert solve_1(real_input) == 383160

    # Part 2
    # assert solve_2(sample_input) == 26984457539
    # assert solve_2(real_input) == ...
