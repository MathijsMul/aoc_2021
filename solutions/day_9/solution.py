import os


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
    pass


def solve_2(input_list):
    pass


if __name__ == "__main__":
    sample_input = read_file("data/day_9/sample.txt")
    real_input = read_file("data/day_9/input.txt")

    assert solve_1(sample_input) == ...
    print(solve_1(real_input))
    # assert solve_1(real_input) == ...

    # Part 2
    # assert solve_2(sample_input) == ..., solve_2(sample_input)
    # print(solve_2(real_input))
    # assert solve_2(real_input) == ..., solve_2(real_input)
