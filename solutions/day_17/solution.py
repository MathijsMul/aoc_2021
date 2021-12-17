import os
from collections import defaultdict, Counter
import numpy as np


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    return [line.strip().split("-") for line in open(input_path).readlines()]


def simulate_path(speed, target_area):
    speed_x, speed_y = speed
    (target_x0, target_x1), (target_y0, target_y1) = target_area

    path = []
    pos = [0,0]

    while (
            (pos[0] <= target_x1) # and speed_x != 0)
            # TODO also stop if x speed constant and x before target
            # and speed_x != 0
            or pos[1] >= target_y1
    ):
        path.append(pos)
        pos = [pos[0] + speed_x, pos[1] + speed_y]

        if speed_x > 1: #0: #0:
            speed_x -= 1
        elif speed_x < 1: #0: #0:
            speed_x += 1

        speed_y -= 1
        print(speed_x, speed_y)
    return path


def target_reached(path, target_area):
    (target_x0, target_x1), (target_y0, target_y1) = target_area
    for loc in path:
        if target_x0 <= loc[0] <= target_x1 and target_y0 <= loc[1] <= target_y1:
            return True
    return False


def get_max_y(path):
    x_locs, y_locs = zip(*path)
    return max(y_locs)


def simulate_at_speed(speed, target_area):
    path = simulate_path(speed, target_area)
    success = target_reached(path, target_area)
    if success:
        max_y = get_max_y(path)
        return max_y


def solve_1(target_area):
    max_y_positions = []
    speeds = []
    for x_speed in range(50): # range(-100, 100):
        for y_speed in range(-20, 20): # range(0, 300):
            # print(x_speed, y_speed)
            max_y = simulate_at_speed((x_speed, y_speed), target_area)
            if max_y is not None:
                # print("true")
                # max_y_positions.append([max_y, (x_speed, y_speed)])
                max_y_positions.append(max_y)
                speeds.append((x_speed, y_speed))

    # return max(max_y_positions), len(max_y_positions)
    return speeds, max_y_positions


def solve_2(input_list):
    return


def load_speeds(path):
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", path
    )
    speeds = []
    for line in open(path).readlines():
        line_speeds = line.split()
        for speed in line_speeds:
            speed_x, speed_y = speed.split(",")
            speeds.append((int(speed_x), int(speed_y)))
    return speeds


if __name__ == "__main__":
    sample_input = "target area: x=20..30, y=-10..-5"
    real_input = "target area: x=79..137, y=-176..-117"

    sample_target = ((20,30),(-10,-5))
    real_target = ((79,137),(-176,-117))

    # Part 1
    # assert simulate_at_speed((7,2), sample_target) == 3
    # assert simulate_at_speed((6,3), sample_target) == 6
    # assert simulate_at_speed((9,0), sample_target) == 0
    # assert simulate_at_speed((17,-4), sample_target) is None
    # maxy = simulate_at_speed((23,-10), sample_target)
    # print(maxy)

    print(simulate_path((1,9), sample_target))

    gold_speeds = load_speeds("data/day_17/speeds")
    print(len(gold_speeds))

    comp_speeds, y_positions = solve_1(sample_target)
    print(len(comp_speeds))

    assert max(y_positions) == 45, max(y_positions)
    for cs in comp_speeds:
        if cs not in gold_speeds:
            print(cs)

    # assert solve_1(sample_target) == (45, 112), solve_1(sample_target)
    # assert solve_1(real_target) == 15400

    # Part 2
    # assert solve_2(sample1_input) == ..., solve_2(sample1_input)
    # assert solve_2(sample2_input) == ..., solve_2(sample2_input)
    # assert solve_2(sample3_input) == ..., solve_2(sample3_input)
    # print(solve_2(real_input))
    # assert solve_2(real_input) == ...
