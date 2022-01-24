from functools import reduce
from itertools import product
from operator import mul
from typing import Tuple

import numpy as np

from utils import read_file


def parse_input(input_path: str):
    steps = []
    for line in read_file(input_path):
        sign = int(line.startswith("on"))
        ranges = []
        range_strs = line.split(" ")[1].split(",")

        for range_str in range_strs:
            range = list(map(int, range_str.split("=")[1].split("..")))

            # Account for range boundaries to prevent one-off errors
            range[1] += 1
            ranges.append(tuple(range))
        steps.append((sign, tuple(ranges)))
    return steps


def solve_1(steps):
    states = np.zeros((101, 101, 101))
    for step in steps:
        sign, [range_x, range_y, range_z] = step
        states[
            range_x[0] + 50 : range_x[1] + 50,
            range_y[0] + 50 : range_y[1] + 50,
            range_z[0] + 50 : range_z[1] + 50,
        ] = sign

    return np.sum(states)


class Cuboid:
    axes = range(3)

    def __init__(self, boundaries: Tuple[Tuple[int]]):
        self.boundaries = boundaries

    def size(self):
        return reduce(mul, (boundary[1] - boundary[0] for boundary in self.boundaries))

    def overlap(self, other: "Cuboid"):
        return all(
            self.boundaries[idx][0] <= other.boundaries[idx][1] - 1
            and self.boundaries[idx][1] - 1 >= other.boundaries[idx][0]
            for idx in self.axes
        )


def get_non_overlapping(cuboid1: Cuboid, cuboid2: Cuboid):
    """Subtract cuboid2 from cuboid1"""

    boundaries = []
    for axis_id in range(3):
        c1_bounds, c2_bounds = cuboid1.boundaries[axis_id], cuboid2.boundaries[axis_id]
        points = list(c1_bounds)

        if c2_bounds[0] >= c1_bounds[0]:
            points.append(c2_bounds[0])
        if c2_bounds[1] <= c1_bounds[1]:
            points.append(c2_bounds[1])

        points = [
            tuple(sorted(points)[idx : idx + 2]) for idx in range(len(points) - 1)
        ]
        boundaries.append(points)

    subcuboids = product(*boundaries)

    # Take out overlapping ones
    non_overlapping_subcuboids = []
    for c in subcuboids:
        subcuboid = Cuboid(c)
        if not cuboid2.overlap(subcuboid):
            non_overlapping_subcuboids.append(subcuboid)

    return non_overlapping_subcuboids


def solve_2(steps):
    cuboids = []

    for step in steps:
        sign, boundaries = step
        new_cuboids, new_cub = [], Cuboid(boundaries)

        for old_cub in cuboids:
            # Detect and remove overlapping area
            if old_cub.overlap(new_cub):
                # Only keep non-overlapping areas of old cuboid
                non_overlapping_subcubs = get_non_overlapping(old_cub, new_cub)
                new_cuboids.extend(non_overlapping_subcubs)
            else:
                new_cuboids.append(old_cub)
        if sign == 1:
            new_cuboids.append(new_cub)
        cuboids = new_cuboids

    return sum(cuboid.size() for cuboid in cuboids)


if __name__ == "__main__":
    sample1_input = parse_input("data/day_22/sample1.txt")
    sample2_input = parse_input("data/day_22/sample2.txt")
    sample3_input = parse_input("data/day_22/sample3.txt")
    real_input = parse_input("data/day_22/input.txt")

    # Part 1
    assert solve_1(sample1_input) == 39
    assert solve_1(sample2_input) == 590784
    assert solve_1(real_input) == 551693

    # Part 2
    assert solve_2(sample3_input) == 2758514936282235
    assert solve_2(real_input) == 1165737675582132
