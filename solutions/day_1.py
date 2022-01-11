from utils import read_file


def parse_input(path):
    return list(map(int, read_file(path)))


def solve(data, window: int = 1):
    return sum(
        map(
            lambda idx: data[idx] > data[idx - window],
            range(window, len(data)),
        )
    )


if __name__ == "__main__":
    input_data = parse_input("data/day_1/input.txt")

    # Part 1
    assert solve(input_data) == 1167

    # Part 2
    assert solve(input_data, 3) == 1130
