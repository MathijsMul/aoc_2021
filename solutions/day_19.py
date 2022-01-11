import itertools
import os
from collections import defaultdict

import numpy as np


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    scanners, scanner = [], []

    with open(input_path) as file:
        for idx, line in enumerate(file.readlines()):
            if "scanner" in line and len(scanner) > 0:
                scanners.append(scanner)
                scanner = []
            elif line != "\n" and "scanner" not in line:
                coords = list(map(int, line.split(",")))
                scanner.append(coords)
        scanners.append(scanner)
        scanner_array = []
        for s in scanners:
            s_array = np.array(s).reshape(len(s), 3)
            scanner_array.append(s_array)
    return scanner_array


def get_distances(observations, abs_sort=False):
    rel_dists = {}
    for idx, obs in enumerate(observations):
        dists = observations - obs
        if abs_sort:
            dists = np.sort(np.abs(dists))
        rel_dists[idx] = dists
    return rel_dists


def compare_2_scanners(scanner_distances, scanner_distances2, min_overlapping=12):
    # Account for point itself
    min_overlapping -= 1

    for dist_idx, distances in scanner_distances.items():
        for dist_idx2, distances2 in scanner_distances2.items():
            overlap_size = (
                distances.shape[0]
                + distances2.shape[0]
                - np.unique(np.concatenate([distances, distances2]), axis=0).shape[0]
            )
            if overlap_size >= min_overlapping:
                # Found enough overlapping beacons.
                return dist_idx, dist_idx2


def compare_all_scanners(scanner_dists, min_overlapping):
    overlap_pairs = []

    for idx, scanner_distances in scanner_dists.items():
        for idx2, scanner_distances2 in scanner_dists.items():
            if idx2 <= idx:
                continue
            overlap = compare_2_scanners(
                scanner_distances, scanner_distances2, min_overlapping
            )
            if overlap:
                overlap_pairs.append([idx, idx2])
    return overlap_pairs


def get_all_rel_distances(scanners):
    dists = {}
    for idx, s in enumerate(scanners):
        dists[idx] = get_distances(s, abs_sort=True)
    return dists


def apply_rotation(dist_dict, rotation):
    out_dict = dict()
    for loc_idx, dists in dist_dict.items():
        out_dict[loc_idx] = dists[:, rotation[0]] * rotation[1]
    return out_dict


def get_rotation_options(num_dimensions=3):
    return list(
        itertools.product(
            itertools.permutations(range(num_dimensions), num_dimensions),
            itertools.product([1, -1], repeat=num_dimensions),
        )
    )


def find_rotations(scanners, overlap_pairs):
    rel_positions = []
    mappings = defaultdict(dict)
    mirror = [[j, i] for [i, j] in overlap_pairs]
    rotation_options = get_rotation_options()

    for pair in overlap_pairs + mirror:
        if pair[1] == 0:
            continue

        s1, s2 = scanners[pair[0]], scanners[pair[1]]
        exact_dists1, exact_dists2_init = get_distances(s1), get_distances(s2)

        for idx, rotation_option in enumerate(rotation_options):
            exact_dists2 = apply_rotation(exact_dists2_init, rotation_option)
            success = compare_2_scanners(exact_dists1, exact_dists2)

            if success:
                print(f"Found right rotation for scanners {pair}")
                s2_rotated = apply_rotation({0: s2}, rotation_option)[0]
                diff = s1[success[0]] - s2_rotated[success[1]]
                mappings[pair[1]][pair[0]] = (rotation_option, diff)

                print(f"Scanner {pair[1]} relative to scanner {pair[0]}: {diff}")
                rel_positions.append([pair, diff])
                break

    return rel_positions, mappings


def get_max_manhattan_dist(coordinates):
    scanner_positions = [c[1][-1] for c in coordinates]
    max_mdist = -1000
    for s1 in scanner_positions:
        for s2 in scanner_positions:
            manhattan_dist = sum(np.abs(s1 - s2))
            if manhattan_dist > max_mdist:
                max_mdist = manhattan_dist
    return max_mdist


def map_scanners(input_array, to_be_mapped, rel_positions, mappings):
    coords = [(i, np.vstack([input_array[i], [0, 0, 0]])) for i in to_be_mapped]
    prio = 0
    mapped_to_zero = {0: prio}

    while any(i[0] != 0 for i in coords):
        prio += 1
        for idx, c in enumerate(coords):
            rot_idx = c[0]
            if rot_idx == 0:
                continue
            for pair, diff in sorted(
                rel_positions, key=lambda i: mapped_to_zero.get(i[0][0], 10000)
            ):
                if pair[1] == rot_idx:
                    print(f"Pair {pair} with diff {diff}")
                    print(f"Mapping {pair[1]} to {pair[0]}")
                    rotation_option, diff_ = mappings[pair[1]][pair[0]]

                    beacons_mapped = (
                        apply_rotation({0: c[1]}, rotation_option)[0] + diff
                    )
                    coords[idx] = (pair[0], beacons_mapped)
                    mapped_to_zero[pair[1]] = prio
                    break
    return coords


def solve(input_array, min_num_overlapping=12):
    all_rel_dists = get_all_rel_distances(input_array)
    overlap_pairs = compare_all_scanners(all_rel_dists, min_num_overlapping)

    rel_positions, mappings = find_rotations(input_array, overlap_pairs)
    to_be_mapped = list(set([i for j in rel_positions for i in j[0]]))
    coords = map_scanners(input_array, to_be_mapped, rel_positions, mappings)

    num_beacons = np.unique(np.concatenate([c[1][:-1] for c in coords]), axis=0).shape[
        0
    ]
    max_mdist = get_max_manhattan_dist(coords)
    return num_beacons, max_mdist


if __name__ == "__main__":
    sample1_input = read_file("data/day_19/sample1.txt")
    sample2_input = read_file("data/day_19/sample2.txt")
    real_input = read_file("data/day_19/input.txt")

    assert solve(sample2_input) == (79, 3621)
    assert solve(real_input) == (396, 11828)
