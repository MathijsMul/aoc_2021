import fileinput
import os


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    return map(
        lambda command: (command[0], int(command[1])),
        (line.split() for line in fileinput.input(input_path)),
    )


def solve_1(path):
    itinerary = read_file(path)

    depth, horiz = 0, 0
    for direction, units in itinerary:
        depth += ((direction == "down") - (direction == "up")) * units
        horiz += (direction == "forward") * units
    return depth * horiz


def solve_2(path):
    itinerary = read_file(path)

    aim, depth, horiz = 0, 0, 0
    for direction, units in itinerary:
        horiz += (direction == "forward") * units
        depth += (direction == "forward") * aim * units
        aim += ((direction == "down") - (direction == "up")) * units
    return depth * horiz


if __name__ == "__main__":
    sample_path = "data/day_2/sample.txt"
    input_path = "data/day_2/input.txt"

    # Part 1
    assert solve_1(sample_path) == 150, solve_1(sample_path)
    assert solve_1(input_path) == 1728414

    # Part 2
    assert solve_2(sample_path) == 900
    assert solve_2(input_path) == 1765720035
