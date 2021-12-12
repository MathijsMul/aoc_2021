import os
import numpy as np
from itertools import product
from collections import defaultdict, Counter


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    return [
        line.strip().split("-")  for line in open(input_path).readlines()
    ]


def get_map(connections):
    map = defaultdict(list)
    for con in connections:
        if con[0] != "end" and con[1] != "start":
            map[con[0]].append(con[1])
        if con[0] != "start" and con[1] != "end":
            map[con[1]].append(con[0])
    return map


def small_cave_check(path):
    counter = Counter(list(filter(lambda loc: loc.islower() and loc not in ["start", "end"], path)))
    return all(counter[cave] <= 1 for cave in counter)


def solve_1(input_list):
    map = get_map(input_list)

    path_stack = [["start"]]
    valid_paths = []

    while len(path_stack) > 0:
        current_path = path_stack.pop()

        for dest in map[current_path[-1]]:
            path = current_path + [dest]

            if dest == "end":
                # print(f"Adding valid path {path}")
                valid_paths.append(path)
                # continue
            elif small_cave_check(path):
                path_stack.append(path)

    return len(valid_paths)


def small_cave_check2(path):
    counter = Counter(list(filter(lambda loc: loc.islower() and loc not in ["start", "end"], path)))
    sorted_counts = sorted(counter.values())
    if not sorted_counts:
        return True
    return all(count <= 1 for count in sorted_counts[:-1]) and sorted_counts[-1] <= 2


def solve_2(input_list):
    map = get_map(input_list)

    path_stack = [["start"]]
    valid_paths = []

    while len(path_stack) > 0:
        current_path = path_stack.pop()

        for dest in map[current_path[-1]]:
            path = current_path + [dest]

            if dest == "end":
                # print(f"Adding valid path {path}")
                valid_paths.append(path)
                # continue
            elif small_cave_check2(path):
                path_stack.append(path)

    return len(valid_paths)


if __name__ == "__main__":
    sample1_input = read_file("data/day_12/sample1.txt")
    sample2_input = read_file("data/day_12/sample2.txt")
    sample3_input = read_file("data/day_12/sample3.txt")
    real_input = read_file("data/day_12/input.txt")

    # Part 1
    assert solve_1(sample1_input) == 10, solve_1(sample1_input)
    assert solve_1(sample2_input) == 19, solve_1(sample2_input)
    # assert solve_1(sample3_input) == 226, solve_1(sample3_input)
    # assert solve_1(real_input) == 4241

    # Part 2
    assert solve_2(sample1_input) == 36, solve_2(sample1_input)
    assert solve_2(sample2_input) == 103, solve_2(sample2_input)
    # assert solve_2(sample3_input) == 3509, solve_2(sample3_input)
    # assert solve_2(real_input) == 122134