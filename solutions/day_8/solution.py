import os
from collections import Counter, defaultdict


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


def solve_1(input_list):
    unique_counter = Counter()
    for _, output in input_list:
        for digit in output:
            unique_counter[len(digit)] += 1
    unique_lengths = [2, 4, 3, 7]
    return sum(unique_counter[i] for i in unique_lengths)


def get_mapping(*args):
    all_signals = args[0] + args[1]
    all_lengths = [len(s) for s in all_signals]

    int2set = defaultdict(set)

    for idx, (length, signal) in enumerate(zip(all_lengths, all_signals)):
        if length == 2:
            int2set[1] = signal
        if length == 3:
            int2set[7] = signal
        if length == 4:
            int2set[4] = signal
        if length == 7:
            int2set[8] = signal

    for idx, (length, signal) in enumerate(zip(all_lengths, all_signals)):
        if length == 6:
            if int2set[4].issubset(signal):
                int2set[9] = signal
            if (
                len(signal.intersection(int2set[1])) == 1
                or len(signal.intersection(int2set[4])) == 2
            ):
                int2set[6] = signal
            elif len(signal.intersection(int2set[4])) == 3:
                int2set[0] = signal
        if length == 5:
            if int2set[1].issubset(signal) or len(signal.intersection(int2set[1])) == 2:
                int2set[3] = signal
            elif signal.issubset(int2set[9]):
                int2set[5] = signal
            elif signal not in int2set.values():
                int2set[2] = signal

    return {"".join(sorted(int2set[i])): str(i) for i in int2set}


def solve_2(input):
    sum = 0
    for item in input:
        mapping = get_mapping(*item)
        signals = item[1]
        digit = ""
        for signal in signals:
            ordered_signal = "".join(sorted(signal))
            digit += str(mapping[ordered_signal])
        sum += int(digit)
    return sum


if __name__ == "__main__":
    sample_input = read_file("data/day_8/sample.txt")
    real_input = read_file("data/day_8/input.txt")

    assert solve_1(sample_input) == 26
    assert solve_1(real_input) == 495

    # Part 2
    assert solve_2(sample_input) == 61229, solve_2(sample_input)
    assert solve_2(real_input) == 1055164
