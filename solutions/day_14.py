import os
from collections import Counter


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    rules = {}
    for idx, line in enumerate(open(input_path).readlines()):
        if idx == 0:
            template = line.strip()
        elif "->" in line:
            pair, insertion = line.strip().split(" -> ")
            rules[pair] = [pair[0] + insertion, insertion + pair[1]]
    return template, rules


def solve(template, insertion_rules, steps):
    pair_count = Counter([template[i : i + 2] for i in range(len(template) - 1)])

    for step in range(steps):
        new_pair_count = Counter()
        for pair, count in pair_count.items():
            for out_pair in insertion_rules[pair]:
                new_pair_count[out_pair] += count

        pair_count = new_pair_count

    char_count = Counter([template[-1]])
    for pair, count in pair_count.items():
        char_count[pair[0]] += count

    chars, counts = zip(*char_count.most_common())
    return counts[0] - counts[-1]


def solve_1(template, insertion_rules):
    return solve(template, insertion_rules, 10)


def solve_2(template, insertion_rules):
    return solve(template, insertion_rules, 40)


if __name__ == "__main__":
    sample_input = read_file("data/day_14/sample.txt")
    real_input = read_file("data/day_14/input.txt")

    # Part 1
    assert solve_1(*sample_input) == 1588, solve_1(*sample_input)
    assert solve_1(*real_input) == 2975

    # Part 2
    assert solve_2(*sample_input) == 2188189693529
    assert solve_2(*real_input) == 3015383850689
