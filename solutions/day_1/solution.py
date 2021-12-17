import os
import pandas as pd


def solve_day_1(data: pd.DataFrame, window_size: int = 1):
    data = data.rolling(window_size).sum()
    return data.shift(-1).gt(data).sum().loc[0]


if __name__ == "__main__":
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", "data/day_1/input.txt"
    )
    input_data = pd.read_csv(input_path, header=None)

    assert solve_day_1(input_data) == 1167
    assert solve_day_1(input_data, 3) == 1130
