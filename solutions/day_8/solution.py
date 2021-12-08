import os
from collections import Counter, defaultdict
import numpy as np


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    all_input = []
    for line in open(input_path).readlines():
        all_input.append(
            [
                [set(signal) for signal in part.strip().split()]
                for part in line.split("|")
            ]
        )
    return all_input


def get_digits(input_path: str = "../../data/day_8/digits.csv"):
    with open(input_path, encoding='utf-8-sig') as f:
        return np.genfromtxt(f, dtype=int, delimiter=',')


def get_digit_lengths(digit_matrix):
    return Counter(digit_matrix.sum(0))


def get_unique_lengths(digit_matrix):
    counts = get_digit_lengths(digit_matrix)
    return [length for length in counts if counts[length] == 1]


def solve_1(input_list):
    unique_counter = Counter()
    for _, output in input_list:
        for digit in output:
            unique_counter[len(digit)] += 1
    unique_lengths = get_unique_lengths(get_digits())
    return sum(unique_counter[i] for i in unique_lengths)


def construct_mapping(mapping, length, signal):
    if length == 2:
        mapping[1] = signal
    elif length == 3:
        mapping[7] = signal
    elif length == 4:
        mapping[4] = signal
    elif length == 5:
        if mapping[1].issubset(signal) or len(signal.intersection(mapping[1])) == 2:
            mapping[3] = signal
        elif signal.issubset(mapping[9]):
            mapping[5] = signal
        elif signal not in mapping.values():
            mapping[2] = signal
    elif length == 6:
        if mapping[4].issubset(signal):
            mapping[9] = signal
        if (
            len(signal.intersection(mapping[1])) == 1
            or len(signal.intersection(mapping[4])) == 2
        ):
            mapping[6] = signal
        elif len(signal.intersection(mapping[4])) == 3:
            mapping[0] = signal
    elif length == 7:
        mapping[8] = signal

    return mapping


def get_mapping(input_signals, output_signals):
    all_signals = input_signals + output_signals
    all_lengths = [len(s) for s in all_signals]
    int2set = defaultdict(set)

    while any(signal not in int2set.values() for signal in all_signals):
        for length, signal in zip(all_lengths, all_signals):
            int2set = construct_mapping(int2set, length, signal)

    return {"".join(sorted(int2set[i])): str(i) for i in int2set}


def solve_2(input_list):
    sum = 0
    for input_sig, output_sig in input_list:
        mapping = get_mapping(input_sig, output_sig)
        sum += int("".join(mapping["".join(sorted(signal))] for signal in output_sig))
    return sum


if __name__ == "__main__":
    sample_input = read_file("data/day_8/sample.txt")
    real_input = read_file("data/day_8/input.txt")

    print(get_digits())
    # exit()

    assert solve_1(sample_input) == 26
    assert solve_1(real_input) == 495

    # Part 2
    assert solve_2(sample_input) == 61229
    assert solve_2(real_input) == 1055164
