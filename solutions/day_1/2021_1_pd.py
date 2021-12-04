import pandas as pd


def solve_day_1(data: pd.DataFrame, window_size: int = 1):
    data = data.rolling(window_size).sum()
    return data.shift(-1).gt(data).sum().loc[0]


if __name__ == "__main__":
    input_data = pd.read_csv("../data/day_1/input.txt", header=None)
    print(solve_day_1(input_data))
    print(solve_day_1(input_data, 3))
