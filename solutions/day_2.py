from utils import read_file


def parse_input(input_path: str):
    return list(
        map(
            lambda command: (command[0], int(command[1])),
            (line.split() for line in read_file(input_path)),
        )
    )


def solve_1(itinerary):
    depth, horiz = 0, 0
    for direction, units in itinerary:
        depth += ((direction == "down") - (direction == "up")) * units
        horiz += (direction == "forward") * units
    return depth * horiz


def solve_2(itinerary):
    aim, depth, horiz = 0, 0, 0
    for direction, units in itinerary:
        horiz += (direction == "forward") * units
        depth += (direction == "forward") * aim * units
        aim += ((direction == "down") - (direction == "up")) * units
    return depth * horiz


if __name__ == "__main__":
    sample_input = parse_input("data/day_2/sample.txt")
    real_input = parse_input("data/day_2/input.txt")

    # Part 1
    assert solve_1(sample_input) == 150
    assert solve_1(real_input) == 1728414

    # Part 2
    assert solve_2(sample_input) == 900
    assert solve_2(real_input) == 1765720035
