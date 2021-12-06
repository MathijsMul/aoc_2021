import os

import numpy as np


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    return np.array(list(map(int, open(input_path).readlines()[0].strip().split(","))))


def extend_birth_planning(birth_planning, num_days, day, num_births=1, interval=7):
    while day < num_days:
        birth_planning[day] += num_births
        day += interval
    return birth_planning


def simulate_population(init_population, num_days):
    birth_planning = np.zeros(num_days)

    for fish_day in init_population:
        birth_planning = extend_birth_planning(birth_planning, num_days, fish_day)

    for day in range(num_days):
        birth_planning = extend_birth_planning(
            birth_planning, num_days, day + 9, birth_planning[day]
        )

    return len(init_population) + sum(birth_planning)


if __name__ == "__main__":
    sample_input = read_file("data/day_6/sample.txt")
    real_input = read_file("data/day_6/input.txt")

    # Part 1
    assert simulate_population(sample_input, 18) == 26
    assert simulate_population(sample_input, 80) == 5934
    assert simulate_population(real_input, 80) == 383160

    # Part 2
    assert simulate_population(sample_input, 256) == 26984457539
    assert simulate_population(real_input, 256) == 1721148811504
