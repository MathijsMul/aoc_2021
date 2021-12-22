import os
from itertools import product
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
    def __init__(self, boundaries: Tuple[Tuple[int]]):
        self.boundaries = boundaries
        self.x_min, self.x_max = self.boundaries[0]
        self.y_min, self.y_max = self.boundaries[1]
        self.z_min, self.z_max = self.boundaries[2]

    def size(self):
        return (
            (self.x_max - self.x_min)
            * (self.y_max - self.y_min)
            * (self.z_max - self.z_min)
        )

    def overlap(self, other: "Cuboid"):
        return (
            (self.x_min <= other.x_max - 1 and self.x_max - 1 >= other.x_min)
            and (self.y_min <= other.y_max - 1 and self.y_max - 1 >= other.y_min)
            and (self.z_min <= other.z_max - 1 and self.z_max - 1 >= other.z_min)
        )


def get_non_overlapping(cuboid1: Cuboid, cuboid2: Cuboid):
    """Subtract cuboid2 from cuboid1"""

    if cuboid2.x_min >= cuboid1.x_min and cuboid2.x_max <= cuboid1.x_max:
        xpoints = [cuboid1.x_min, cuboid2.x_min, cuboid2.x_max, cuboid1.x_max]
    elif cuboid2.x_min >= cuboid1.x_min:
        xpoints = [cuboid1.x_min, cuboid2.x_min, cuboid1.x_max]
    elif cuboid2.x_max <= cuboid1.x_max:
        xpoints = [cuboid1.x_min, cuboid2.x_max, cuboid1.x_max]
    else:
        xpoints = [cuboid1.x_min, cuboid1.x_max]

    if cuboid2.y_min >= cuboid1.y_min and cuboid2.y_max <= cuboid1.y_max:
        ypoints = [cuboid1.y_min, cuboid2.y_min, cuboid2.y_max, cuboid1.y_max]
    elif cuboid2.y_min >= cuboid1.y_min:
        ypoints = [cuboid1.y_min, cuboid2.y_min, cuboid1.y_max]
    elif cuboid2.y_max <= cuboid1.y_max:
        ypoints = [cuboid1.y_min, cuboid2.y_max, cuboid1.y_max]
    else:
        ypoints = [cuboid1.y_min, cuboid1.y_max]

    if cuboid2.z_min >= cuboid1.z_min and cuboid2.z_max <= cuboid1.z_max:
        zpoints = [cuboid1.z_min, cuboid2.z_min, cuboid2.z_max, cuboid1.z_max]
    elif cuboid2.z_min >= cuboid1.z_min:
        zpoints = [cuboid1.z_min, cuboid2.z_min, cuboid1.z_max]
    elif cuboid2.z_max <= cuboid1.z_max:
        zpoints = [cuboid1.z_min, cuboid2.z_max, cuboid1.z_max]
    else:
        zpoints = [cuboid1.z_min, cuboid1.z_max]

    xranges = [tuple(xpoints[idx : idx + 2]) for idx in range(len(xpoints) - 1)]
    yranges = [tuple(ypoints[idx : idx + 2]) for idx in range(len(ypoints) - 1)]
    zranges = [tuple(zpoints[idx : idx + 2]) for idx in range(len(zpoints) - 1)]

    subcuboids = list(product(xranges, yranges, zranges))

    # Take out overlapping ones
    non_overlapping_subcuboids = []
    for c in subcuboids:
        subcuboid = Cuboid(c)
        if not cuboid2.overlap(subcuboid):
            non_overlapping_subcuboids.append(subcuboid)

    return non_overlapping_subcuboids


def solve_2(steps):
    cuboids = []

    for idx, step in enumerate(steps):
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
