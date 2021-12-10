import os


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    return [line.strip() for line in open(input_path).readlines()]


OPEN_TO_CLOSE = {"(": ")", "[": "]", "{": "}", "<": ">"}


def solve_1(input_list):
    scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    score = 0
    for line in input_list:
        close_chars = []
        for char in line:
            if char in OPEN_TO_CLOSE:
                close_chars.append(OPEN_TO_CLOSE[char])
            else:
                if char == close_chars[-1]:
                    close_chars.pop()
                else:
                    # Syntax error
                    # print(f"Found illegal char {char}")
                    score += scores[char]
                    break
    return score


def score_2(points):
    score = 0
    while len(points) > 0:
        score = (5 * score) + points[0]
        points = points[1:]
    return score


def solve_2(input_list):
    points = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }

    scores = []
    for line in input_list:
        close_chars = []
        num_chars = len(line)
        for idx, char in enumerate(line):
            if char in OPEN_TO_CLOSE:
                close_chars.append(OPEN_TO_CLOSE[char])
            else:
                if char == close_chars[-1]:
                    close_chars.pop()
                else:
                    # Syntax error: corrupted line
                    # print(f"Found illegal char {char}")
                    break

            if idx == num_chars - 1:
                if len(close_chars) > 0:
                    # Incomplete line
                    completion = close_chars[::-1]
                    print(
                        f"Found incomplete line with necessary completion: {completion}"
                    )

                    score = score_2([points[cc] for cc in completion])
                    print(f"Score: {score}")
                    scores.append(score)

    return sorted(scores)[int((len(scores) - 1) / 2)]


if __name__ == "__main__":
    sample_input = read_file("data/day_10/sample.txt")
    real_input = read_file("data/day_10/input.txt")

    assert solve_1(sample_input) == 26397, solve_1(sample_input)
    assert solve_1(real_input) == 166191

    # Part 2
    assert solve_2(sample_input) == 288957
    assert solve_2(real_input) == 1152088313
