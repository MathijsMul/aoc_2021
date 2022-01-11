import os
from functools import reduce
from itertools import product
from operator import mul
from typing import Tuple

import numpy as np


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    steps = []
    for line in open(input_path).readlines():
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
        cuboid1_bounds = cuboid1.boundaries[axis_id]
        cuboid2_bounds = cuboid2.boundaries[axis_id]
        points = list(cuboid1_bounds)

        if cuboid2_bounds[0] >= cuboid1_bounds[0]:
            points.append(cuboid2_bounds[0])
        if cuboid2_bounds[1] <= cuboid1_bounds[1]:
            points.append(cuboid2_bounds[1])
        points = sorted(points)
        points = [tuple(points[idx : idx + 2]) for idx in range(len(points) - 1)]
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
        new_cuboids = []
        sign, boundaries = step
        new_cub = Cuboid(boundaries)

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

    num_on = 0
    for cuboid in cuboids:
        num_on += cuboid.size()

    return num_on


if __name__ == "__main__":
    sample1_input = read_file("data/day_22/sample1.txt")
    sample2_input = read_file("data/day_22/sample2.txt")
    sample3_input = read_file("data/day_22/sample3.txt")
    real_input = read_file("data/day_22/input.txt")

    # Part 1
    assert solve_1(sample1_input) == 39, solve_1(sample1_input)
    assert solve_1(sample2_input) == 590784, solve_1(sample2_input)
    assert solve_1(real_input) == 551693

    # Part 2
    assert solve_2(sample3_input) == 2758514936282235, solve_2(sample3_input)
    assert solve_2(real_input) == 1165737675582132
