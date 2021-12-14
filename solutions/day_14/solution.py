import os
from collections import defaultdict, Counter
import numpy as np


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    rules = {}
    for idx, line in enumerate(open(input_path).readlines()):
        if idx == 0:
            template = line.strip()
        elif "->" in line:
            start, end = line.strip().split(" -> ")
            rules[start] = end
    return template, rules


def solve_1_naive(input_template, insertion_rules, steps = 10):
    for step in range(steps):
        print(step)
        polymer = ""
        for idx in range(len(input_template) - 1):
            pair = input_template[idx:idx + 2]
            if idx == 0:
                polymer += pair[0]
            polymer += insertion_rules[pair] + pair[1]
        input_template = polymer
    counts = Counter(list(polymer)).most_common()
    most_common_count = counts[0][1]
    least_common_count = counts[-1][1]
    return most_common_count - least_common_count


def solve_1(template, insertion_rules, steps = 10):
    extended_rules = {}
    for pair in insertion_rules:
        inserted = insertion_rules[pair]
        extended_rules[pair] = [pair[0] + inserted, inserted + pair[1]]

    stop = template[-1]
    pair_count = Counter([template[i:i+2] for i in range(len(template) - 1)])

    for step in range(steps):
        # print(step)
        new_pair_count = Counter()
        for pair, count in pair_count.items():
            out_pairs = extended_rules[pair]
            for out_pair in out_pairs:
                new_pair_count[out_pair] += count

        pair_count = new_pair_count

    char_count = Counter([stop])
    for pair, count in pair_count.items():
        char_count[pair[0]] += count

    # chars = [pair[0] for pair in pairs] + [stop]
    counts = char_count.most_common()
    most_common_count = counts[0][1]
    least_common_count = counts[-1][1]
    return most_common_count - least_common_count



def solve_2(input_list):
    return


if __name__ == "__main__":
    sample_input = read_file("data/day_14/sample.txt")
    real_input = read_file("data/day_14/input.txt")

    sample_template, sample_rules = sample_input

    # Part 1
    assert solve_1(*sample_input) == 1588, solve_1(*sample_input)
    assert solve_1(*real_input) == 2975

    # Part 2
    sample_answer = solve_1(*sample_input, 40)
    assert sample_answer == 2188189693529, sample_answer
    # assert solve_2(sample2_input) == ..., solve_2(sample2_input)
    # assert solve_2(sample3_input) == ..., solve_2(sample3_input)
    print(solve_1(*real_input, 40))
    # assert solve_2(real_input) == ...
