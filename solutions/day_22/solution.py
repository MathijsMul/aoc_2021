import os
from collections import defaultdict, Counter
import numpy as np
from scipy.sparse import lil_matrix
from itertools import product


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    steps = []
    for line in open(input_path).readlines():
        # print(line)
        sign = None
        if line.startswith("on"):
            sign = 1
        elif line.startswith("off"):
            sign = 0

        ranges = []
        range_strs = line.split(" ")[1].split(",")
        for range_str in range_strs:
            range = list(map(int, range_str.split("=")[1].split("..")))
            range[1] += 1
            range = tuple(range)
            ranges.append(range)
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


def overlap(cuboid1, cuboid2):
    ((xmin1, xmax1), (ymin1, ymax1), (zmin1, zmax1)) = cuboid1
    ((xmin2, xmax2), (ymin2, ymax2), (zmin2, zmax2)) = cuboid2

    return (
        set(range(xmin1, xmax1)).intersection(set(range(xmin2, xmax2)))
        and set(range(ymin1, ymax1)).intersection(set(range(ymin2, ymax2)))
        and set(range(zmin1, zmax1)).intersection(set(range(zmin2, zmax2)))
    )


def get_non_overlapping(cuboid1, cuboid2):
    # Compute cuboid1 - cuboid2 
    ((xmin1, xmax1), (ymin1, ymax1), (zmin1, zmax1)) = cuboid1
    ((xmin2, xmax2), (ymin2, ymax2), (zmin2, zmax2)) = cuboid2

    if xmin2 >= xmin1 and xmax2 <= xmax1:
        xpoints = [xmin1,xmin2,xmax2,xmax1]
    elif xmin2 >= xmin1:
        xpoints = [xmin1, xmin2, xmax1]
    elif xmax2 <= xmax1:
        xpoints = [xmin1, xmax2, xmax1]
    else:
        xpoints = [xmin1, xmax1]

    if ymin2 >= ymin1 and ymax2 <= ymax1:
        ypoints = [ymin1,ymin2,ymax2,ymax1]
    elif ymin2 >= ymin1:
        ypoints = [ymin1, ymin2, ymax1]
    elif ymax2 <= ymax1:
        ypoints = [ymin1, ymax2, ymax1]
    else:
        ypoints = [ymin1, ymax1]

    if zmin2 >= zmin1 and zmax2 <= zmax1:
        zpoints = [zmin1,zmin2,zmax2,zmax1]
    elif zmin2 >= zmin1:
        zpoints = [zmin1, zmin2, zmax1]
    elif zmax2 <= zmax1:
        zpoints = [zmin1, zmax2, zmax1]
    else:
        zpoints = [zmin1, zmax1]

    xranges = [tuple(xpoints[idx:idx+2]) for idx in range(len(xpoints)-1)]
    yranges = [tuple(ypoints[idx:idx+2]) for idx in range(len(ypoints)-1)]
    zranges = [tuple(zpoints[idx:idx+2]) for idx in range(len(zpoints)-1)]

    subcuboids = list(product(xranges, yranges, zranges))

    # Take out overlapping ones
    non_overlapping_subcuboids = []
    for c in subcuboids:
        if not overlap(c, cuboid2):
            non_overlapping_subcuboids.append(c)

    return non_overlapping_subcuboids


def compute_bounds(steps):
    xmin, xmax, ymin, ymax, zmin, zmax = 0,0,0,0,0,0
    for step in steps:
        _, [(x0, x1), (y0,y1), (z0,z1)] = step
        if x0 < xmin:
            xmin = x0
        if x1 > xmax:
            xmax = x1
        if y0 < ymin:
            ymin = y0
        if y1 > ymax:
            ymax = y1
        if z0 < zmin:
            zmin = z0
        if z1 > zmax:
            zmax = z1
    return ((xmin, xmax),(ymin, ymax),(zmin,zmax))
    # (-120100, 120875) (-124565, 118853) (-121762, 119054)


def solve_2(steps):
    # Represent cuboids as ((xmin, xmax),(ymin, ymax),(zmin,zmax))
    cuboids = []

    for idx, step in enumerate(steps):
        print(f"Step {idx}")
        print(f"Num cuboids: {len(cuboids)}")
        new_cuboids = []
        sign, new_cub = step
        # [(xmin, xmax), (ymin, ymax), (zmin, zmax)] = new_cub

        for old_cub in cuboids:
            # Detect and remove overlapping area
            if overlap(old_cub, new_cub):
                # Only keep non-overlapping areas of old cuboid
                non_overlapping_subcubs = get_non_overlapping(old_cub, new_cub)
                new_cuboids.extend(non_overlapping_subcubs)

                # TODO
                # don't cut pieces of existing cuboids, but take them off the NEW one
            else:
                new_cuboids.append(old_cub)
        if sign == 1:
            new_cuboids.append(new_cub)
        cuboids = new_cuboids

    num_on = 0
    for c in cuboids:
        (xmin, xmax), (ymin, ymax), (zmin, zmax) = c
        size = ((xmax - xmin)) * ((ymax - ymin)) * ((zmax - zmin))
        num_on += size

    return num_on


# def solve_2(steps):
#     range_dict = defaultdict(lambda: defaultdict(list))
#     for idx, step in enumerate(steps):
#         print(f"Step {idx}")
#         sign, cuboid = step
#         [(xmin, xmax), (ymin, ymax), (zmin, zmax)] = cuboid
#         for x in range(xmin, xmax+1):
#             for y in range(ymin, ymax+1):
#                 range_dict[x][y].append(range(zmin, zmax+1))
#
#     return


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
    # assert solve_2(sample1_input) == ..., solve_2(sample1_input)
    # assert solve_2(sample2_input) == ..., solve_2(sample2_input)


    # print(sample3_input)
    print(solve_2(sample3_input))
    # assert solve_2(sample3_input) == 2758514936282235, solve_2(sample3_input)

    # wrong: 2759022355482587

    # print(solve_2(real_input))
    # assert solve_2(real_input) == ...
