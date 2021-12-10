import os


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    return [line.strip() for line in open(input_path).readlines()]


def solve_1(input_list):
    return


def solve_2(input_list):
    return


if __name__ == "__main__":
    sample_input = read_file("data/day_11/sample.txt")
    real_input = read_file("data/day_11/input.txt")

    assert solve_1(sample_input) == ...
    print(solve_1(real_input))
    # assert solve_1(real_input) == ..., solve_1(real_input)

    # Part 2
    # assert solve_2(sample_input) == ...
    # assert solve_2(real_input) == ..., solve_2(real_input)
