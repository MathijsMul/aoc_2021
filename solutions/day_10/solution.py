import os


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    return [line.strip() for line in open(input_path).readlines()]


OPEN_TO_CLOSE = {"(": ")", "[": "]", "{": "}", "<": ">"}
CORRUPT_SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
INCOMPLETE_SCORES = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def score_2(points):
    return sum((5 ** idx) * point for idx, point in enumerate(points[::-1]))


def solve(input_list):
    corrupt_scores, incomplete_scores = [], []

    for line in input_list:
        close_chars = []
        for idx, char in enumerate(line):
            if char in OPEN_TO_CLOSE:
                close_chars.append(OPEN_TO_CLOSE[char])
            else:
                if char == close_chars[-1]:
                    close_chars.pop()
                else:
                    # Corrupt line
                    corrupt_scores.append(CORRUPT_SCORES[char])
                    break
            if idx == len(line) - 1:
                if len(close_chars) > 0:
                    # Incomplete line
                    completion = close_chars[::-1]
                    score = score_2([INCOMPLETE_SCORES[cc] for cc in completion])
                    incomplete_scores.append(score)

    corrupt_score = sum(corrupt_scores)
    incomplete_score = sorted(incomplete_scores)[int((len(incomplete_scores) - 1) / 2)]
    return corrupt_score, incomplete_score


if __name__ == "__main__":
    sample_input = read_file("data/day_10/sample.txt")
    real_input = read_file("data/day_10/input.txt")

    assert solve(sample_input)[0] == 26397
    assert solve(real_input)[0] == 166191

    # Part 2
    assert solve(sample_input)[1] == 288957
    assert solve(real_input)[1] == 1152088313
