from utils import read_file


def parse_input(input_path: str):
    return [line.strip().split("-") for line in read_file(input_path)]


def simulate_path(speed, target_area):
    speed_x, speed_y = speed
    (target_x0, target_x1), (target_y0, target_y1) = target_area

    path = [[0, 0]]
    while path[-1][0] <= target_x1 and path[-1][1] >= target_y0:
        pos = [path[-1][0] + speed_x, path[-1][1] + speed_y]

        if speed_x > 0:
            speed_x -= 1
        elif speed_x < 0:
            speed_x += 1

        speed_y -= 1
        path.append(pos)

    return path


def target_reached(path, target_area):
    (target_x0, target_x1), (target_y0, target_y1) = target_area
    for loc in path:
        if target_x0 <= loc[0] <= target_x1 and target_y0 <= loc[1] <= target_y1:
            return True
    return False


def get_max_y(speed, target_area):
    path = simulate_path(speed, target_area)
    success = target_reached(path, target_area)
    if success:
        x_locs, y_locs = zip(*path)
        return max(y_locs)


def solve_1(target_area):
    (target_x0, target_x1), (target_y0, target_y1) = target_area

    max_y_positions = []
    for x_speed in range(target_x1 + 1):
        for y_speed in range(target_y0, 500):
            max_y = get_max_y((x_speed, y_speed), target_area)
            if max_y is not None:
                max_y_positions.append(max_y)

    return max(max_y_positions), len(max_y_positions)


if __name__ == "__main__":
    sample_target = ((20, 30), (-10, -5))
    real_target = ((79, 137), (-176, -117))

    assert get_max_y((7, 2), sample_target) == 3
    assert get_max_y((6, 3), sample_target) == 6
    assert get_max_y((9, 0), sample_target) == 0
    assert get_max_y((17, -4), sample_target) is None

    sample_output_1, sample_output_2 = solve_1(sample_target)
    real_output_1, real_output_2 = solve_1(real_target)

    # Part 1
    assert sample_output_1 == 45
    assert real_output_1 == 15400

    # Part 2
    assert sample_output_2 == 112
    assert real_output_2 == 5844, real_output_2
