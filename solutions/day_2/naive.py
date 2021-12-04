import os


def read_file(input_path: str) -> list:
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )

    input = []
    for line in open(input_path).readlines():
        dir, amount = line.split()
        amount = int(amount)
        input.append((dir, amount))
    return input


def solve_1(itinerary):
    depth, hor = 0, 0

    for dir, amount in itinerary:
        if dir == "forward":
            hor += amount
        elif dir == "up":
            depth -= amount
        elif dir == "down":
            depth += amount

    return hor * depth


def solve_2(itinerary):
    aim, depth, hor = 0, 0, 0

    for dir, amount in itinerary:
        if dir == "forward":
            hor += amount
            depth += aim * amount
        elif dir == "up":
            aim -= amount
        elif dir == "down":
            aim += amount

    return hor * depth


if __name__ == "__main__":
    input_sample = read_file("data/day_2/sample.txt")
    input_real = read_file("data/day_2/input.txt")

    # Part 1
    assert solve_1(input_sample) == 150
    assert solve_1(input_real) == 1728414

    # Part 2
    assert solve_2(input_sample) == 900
    assert solve_2(input_real) == 1765720035
