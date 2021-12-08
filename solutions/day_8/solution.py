import os
from collections import Counter


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    all_input = []
    for line in open(input_path).readlines():
        parts = line.split("|")
        input = parts[0].strip().split()
        output = parts[1].strip().split()
        all_input.append([input, output])
    return all_input


def solve_1(input):
    unique_counter = Counter()
    for item in input:
        # print(item[1])
        for digit in item[1]:
            unique_counter[len(digit)] += 1
        # print(unique_counter)
    unique_items = [2, 4, 3, 7]
    return sum(unique_counter[i] for i in unique_items)


def get_mapping(*args):
    all_signals = args[0] + args[1]
    all_lengths = [len(s) for s in all_signals]

    mapping = {}

    if 2 in all_lengths:
        digit1 = all_signals[all_lengths.index(2)]
        mapping["".join(sorted(digit1))] = "1"
    if 3 in all_lengths:
        digit7 = all_signals[all_lengths.index(3)]
        mapping["".join(sorted(digit7))] = "7"
    if 4 in all_lengths:
        digit4 = all_signals[all_lengths.index(4)]
        mapping["".join(sorted(digit4))] = "4"
    if 7 in all_lengths:
        digit8 = all_signals[all_lengths.index(7)]
        mapping["".join(sorted(digit8))] = "8"

    for idx, (length, signal) in enumerate(zip(all_lengths, all_signals)):
        if length == 6:
            if set(digit4).issubset(set(signal)):
                digit9 = signal
                mapping["".join(sorted(digit9))] = "9"
        if length == 5:
            if set(digit1).issubset(set(signal)):
                digit3 = signal
                mapping["".join(sorted(digit3))] = "3"
            try:
                if set(signal).issubset(set(digit9)):
                    digit5 = signal
                    mapping["".join(sorted(digit5))] = "5"
            except UnboundLocalError:
                continue
        if length == 6:
            if len(set(signal).intersection(set(digit1))) == 1:
                digit6 = signal
                mapping["".join(sorted(digit6))] = "6"
            elif len(set(signal).intersection(set(digit4))) == 2:
                digit6 = signal
                mapping["".join(sorted(digit6))] = "6"
            elif len(set(signal).intersection(set(digit4))) == 3:
                digit0 = signal
                mapping["".join(sorted(digit0))] = "0"
        if length == 5:
            if len(set(signal).intersection(set(digit1))) == 2:
                digit3 = signal
                mapping["".join(sorted(digit3))] = "3"
            elif "".join(sorted(signal)) not in mapping:
                digit2 = signal
                mapping["".join(sorted(digit2))] = "2"

    return mapping


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
    assert solve_2(sample_input) == 61229
    assert solve_2(real_input) == 1055164
