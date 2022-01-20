import itertools
from collections import defaultdict

import numpy as np

from utils import read_file


def parse_input(input_path: str):
    scanners, scanner = [], []

    for idx, line in enumerate(read_file(input_path)):
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


def find_overlap(scanner_distances, scanner_distances2, min_overlapping=12):
    """
    Determine if two scanners have enough overlapping points by comparing relative internal
    distances.
    """
    for dist_idx, distances in scanner_distances.items():
        for dist_idx2, distances2 in scanner_distances2.items():
            if dist_idx2 <= dist_idx:
                continue
            overlap_size = (
                distances.shape[0]
                + distances2.shape[0]
                - np.unique(np.concatenate([distances, distances2]), axis=0).shape[0]
            )
            # Account for point itself
            if overlap_size >= min_overlapping - 1:
                # Found enough overlapping beacons.
                return dist_idx, dist_idx2


def compare_all_scanners(input_array):
    """
    Compare all scanners, and if there is sufficient overlap compute the rotation and translation
    between them.
    """
    abs_dists, rel_dists = get_all_distances(input_array)
    mappings = defaultdict(dict)
    rotation_options = get_rotation_options()

    for idx1, distances1 in rel_dists.items():
        for idx2, distances2 in rel_dists.items():
            if idx2 <= idx1 or not find_overlap(distances1, distances2):
                continue

            mappings[idx2][idx1] = get_transform(
                rotation_options, abs_dists, input_array, idx1, idx2
            )
            mappings[idx1][idx2] = get_transform(
                rotation_options, abs_dists, input_array, idx2, idx1
            )
    return mappings


def get_transform(rotation_options, abs_dists, input_array, idx1, idx2):
    """Compute rotation and translation between two scanners."""
    for rotation in rotation_options:
        exact_dists2 = rotate_all(abs_dists[idx2], rotation)
        success = find_overlap(abs_dists[idx1], exact_dists2)

        if success:
            s2_rotated = apply_rotation(input_array[idx2], rotation)
            translation = input_array[idx1][success[0]] - s2_rotated[success[1]]
            print(f"Rotation, translation for {idx1, idx2}: {rotation}, {translation}")
            return rotation, translation


def get_all_distances(scanners):
    rel_dists, abs_dists = defaultdict(dict), defaultdict(dict)
    for scanner_idx, observations in enumerate(scanners):
        for obs_idx, observation in enumerate(observations):
            abs_dist = observations - observation
            abs_dists[scanner_idx][obs_idx] = abs_dist
            rel_dists[scanner_idx][obs_idx] = np.sort(np.abs(abs_dist))
    return abs_dists, rel_dists


def rotate_all(dist_dict, rotation):
    out_dict = dict()
    for loc_idx, dists in dist_dict.items():
        out_dict[loc_idx] = apply_rotation(dists, rotation)
    return out_dict


def apply_rotation(array, rotation):
    return array[:, rotation[0]] * rotation[1]


def get_rotation_options(num_dimensions=3):
    """
    Compute all possible rotations, represented as tuples of permutations of axes and inversions
    of axis directions.
    """
    return list(
        itertools.product(
            itertools.permutations(range(num_dimensions), num_dimensions),
            itertools.product([1, -1], repeat=num_dimensions),
        )
    )


def get_max_manhattan_dist(coordinates, max_mdist=-1):
    """Compute maximum Manhattan distance between any pair of positions."""
    scanner_positions = [c[1][-1] for c in coordinates]
    for idx1, s1 in enumerate(scanner_positions):
        for s2 in scanner_positions[idx1+1:]:
            manhattan_dist = sum(np.abs(s1 - s2))
            if manhattan_dist > max_mdist:
                max_mdist = manhattan_dist
    return max_mdist


def map_scanners(input_array, mappings, prio=0):
    """
    Map observations of scanners into each other's frame of reference in order to position all
    beacons in the same space, relative to the first scanner.
    """
    scanner_pairs = [(idx1, idx2) for idx1 in mappings for idx2 in mappings[idx1]]
    to_be_mapped = set([idx for pair in scanner_pairs for idx in pair])
    coords = [(idx, np.vstack([input_array[idx], [0, 0, 0]])) for idx in to_be_mapped]
    mapped_to_zero = {0: prio}

    while any(base_idx != 0 for base_idx, _ in coords):
        prio += 1
        for scanner_idx, (base_idx, observations) in enumerate(coords):
            if base_idx == 0:
                continue
            for idx1, idx2 in sorted(
                scanner_pairs, key=lambda i: mapped_to_zero.get(i[0], prio + 1)
            ):
                if idx2 != base_idx or idx2 == idx1:
                    continue
                rotation, translation = mappings[idx2][idx1]
                beacons_mapped = apply_rotation(observations, rotation) + translation
                coords[scanner_idx] = (idx1, beacons_mapped)
                mapped_to_zero[idx2] = prio
                break
    return coords


def get_unique_beacons(positions):
    """Compute nr of unique beacons."""
    return np.unique(
        np.concatenate([position[1][:-1] for position in positions]), axis=0
    ).shape[0]


def solve(input_array):
    mappings = compare_all_scanners(input_array)
    positions = map_scanners(input_array, mappings)
    return get_unique_beacons(positions), get_max_manhattan_dist(positions)


if __name__ == "__main__":
    sample1_input = parse_input("data/day_19/sample1.txt")
    real_input = parse_input("data/day_19/input.txt")

    assert solve(sample1_input) == (79, 3621)
    assert solve(real_input) == (396, 11828)
