import numpy as np

from utils import read_file


def parse_input(input_path: str):
    return np.array(list(map(int, read_file(input_path)[0].strip().split(","))))


def extend_birth_planning(
    birth_planning, num_days, start_day, num_births=1, interval=7
):
    days = [
        start_day + i * interval
        for i in range(1 + ((num_days - 1 - start_day) // interval))
    ]
    birth_planning[days] += num_births
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
    sample_input = parse_input("data/day_6/sample.txt")
    real_input = parse_input("data/day_6/input.txt")

    # Part 1
    assert simulate_population(sample_input, 18) == 26
    assert simulate_population(sample_input, 80) == 5934
    assert simulate_population(real_input, 80) == 383160

    # Part 2
    assert simulate_population(sample_input, 256) == 26984457539
    assert simulate_population(real_input, 256) == 1721148811504
