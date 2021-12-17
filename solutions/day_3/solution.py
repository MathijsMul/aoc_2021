import fileinput
import os
from typing import List, Tuple, Callable, Iterable


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    return [list(map(int, line.strip())) for line in fileinput.input(input_path)]


def gamma(column: Tuple[int]) -> int:
    return max([1, 0], key=lambda x: column.count(x))


def epsilon(column: Tuple[int]) -> int:
    return min([0, 1], key=lambda x: column.count(x))


def filter_by_rate(
    input_rows: List[List[int]], criterion: Callable, col_idx: int = 0
) -> List[int]:
    if len(input_rows) == 1:
        return input_rows[0]
    return filter_by_rate(
        [
            row
            for row in input_rows
            if row[col_idx] == criterion([row[col_idx] for row in input_rows])
        ],
        criterion,
        col_idx + 1,
    )


def bin2int(input: Iterable[int]) -> int:
    return int("".join(map(str, input)), 2)


def solve_1(input_list: List[List[int]]):
    g, e = (bin2int(rate(col) for col in zip(*input_list)) for rate in (gamma, epsilon))
    return g * e


def solve_2(input_list: List[List[int]]):
    oxy, co2 = (bin2int(filter_by_rate(input_list, rate)) for rate in (gamma, epsilon))
    return oxy * co2


if __name__ == "__main__":
    sample_input = read_file("data/day_3/sample.txt")
    real_input = read_file("data/day_3/input.txt")

    # Part 1
    assert solve_1(sample_input) == 198, solve_1(sample_input)
    assert solve_1(real_input) == 3895776

    # Part 2
    assert solve_2(sample_input) == 230
    assert solve_2(real_input) == 7928162
