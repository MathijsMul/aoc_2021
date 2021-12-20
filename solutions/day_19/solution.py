import os
from collections import defaultdict, Counter
import numpy as np
import itertools


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    scanners = []
    scanner = []
    for idx, line in enumerate(open(input_path).readlines()):
        if "scanner" in line and len(scanner) > 0:
            scanners.append(scanner)
            scanner = []
        elif line != "\n" and "scanner" not in line:
            coords = list(map(int, line.split(",")))
            scanner.append(coords)
    scanners.append(scanner)
    # return scanners
    # print(scanners)
    scanner_array = []
    for s in scanners:
        s_array = np.array(s).reshape(len(s), 3)
        scanner_array.append(s_array)
    # scanner_array = np.array(scanners).reshape(len(scanners), -1, 3)
    return scanner_array


def rotate(positions, dir1, dir2):
    """Rotate positions in given directions."""
    dims = list(zip(*positions))

    pos1 = dims[dir1[0]]


def get_relative_distances(observations):
    rel_dists = defaultdict(set)
    for idx1, obs1 in enumerate(observations):
        for idx2, obs2 in enumerate(observations):
            if idx1 != idx2:
                dist = obs2 - obs1
                # print(obs1, obs2)
                # print(dist)
                dist = str(sorted(list(np.abs(dist))))
                rel_dists[idx1].add(dist)
    return rel_dists


def get_exact_distances(observations):
    dists = defaultdict(list)
    for idx1, obs1 in enumerate(observations):
        for idx2, obs2 in enumerate(observations):
            if idx1 != idx2:
                dist = obs2 - obs1
                # print(obs1, obs2)
                # print(dist)
                # dist = str(sorted(list(np.abs(dist))))
                # dist = str(dist)
                dists[idx1].append(dist)

    array_dists = dict()
    for loc_idx, dist_list in dists.items():
        array_dists[loc_idx] = np.stack(dist_list)

    return array_dists


def neutralize_positions():
    """Make absolute and orderless"""
    pass


def compare_2_scanners(scanner_distances, scanner_distances2, min_overlapping):
    # Account for point itself
    min_overlapping -= 1

    num_points = len(scanner_distances)
    num_points2 = len(scanner_distances2)

    for dist_idx, distances in scanner_distances.items():
        for dist_idx2, distances2 in scanner_distances2.items():
            overlap = distances.intersection(distances2)
            overlap_size = len(overlap)
            if overlap_size >= min_overlapping:
                # match
                print(f"Found enough overlapping beacons.")
                # get_rel_position()
                return (dist_idx, dist_idx2)
        #     if num_points2 - dist_idx2 < min_overlapping:
        #         # no match
        #         break
        # if num_points - dist_idx < min_overlapping:
        #     # no match
        #     break
    return False


def compare_all_scanners(scanner_dists, min_overlapping):
    overlap_pairs = []

    for idx, scanner_distances in scanner_dists.items():
        for idx2, scanner_distances2 in scanner_dists.items():
            if idx2 > idx:
                print(f"Comparing scanner {idx} and {idx2}")
                overlap = compare_2_scanners(
                    scanner_distances, scanner_distances2, min_overlapping
                )
                if overlap:
                    overlap_pairs.append([idx, idx2])
    return overlap_pairs


def get_all_rel_distances(scanners):
    dists = {}
    for idx, s in enumerate(scanners):
        dists[idx] = get_relative_distances(s)
    return dists


def apply_rotation(dist_dict, option_idx):
    options = list(
        itertools.product(
            itertools.permutations([0, 1, 2], 3), itertools.product([1, -1], repeat=3)
        )
    )
    rot = options[option_idx]

    out_dict = dict()

    for loc_idx, dists in dist_dict.items():
        # for dist in dists:
        out_dict[loc_idx] = dists[:, rot[0]] * rot[1]

    return out_dict


def stringify_arrays(dist_dict):
    out_dict = dict()
    for k, v in dist_dict.items():
        out_dict[k] = set([str(i) for i in v])
    return out_dict


def get_rel_positions(scanners, overlap_pairs):
    rel_positions = []
    rotated = defaultdict(dict)
    rotated[0] = scanners[0]
    mappings = defaultdict(dict)

    mirror = [[j, i] for [i, j] in overlap_pairs]

    for pair in overlap_pairs + mirror:
        if pair[1] != 0:
            s1 = scanners[pair[0]]
            s2 = scanners[pair[1]]

            exact_dists1 = get_exact_distances(s1)
            exact_dists1_strs = stringify_arrays(exact_dists1)

            exact_dists2_init = get_exact_distances(s2)

            right_rotation = False
            rotation_option = 0
            while not right_rotation:
                # Rotate
                exact_dists2 = apply_rotation(exact_dists2_init, rotation_option)

                exact_dists2_strs = stringify_arrays(exact_dists2)

                comp = compare_2_scanners(exact_dists1_strs, exact_dists2_strs, 12)
                if comp:
                    # Get relative position

                    right_rotation = True
                    print(f"Found right rotation for scanners {pair}")
                    loc_idx1, loc_idx2 = comp
                    s2_rotated = apply_rotation({0: s2}, rotation_option)[0]
                    # rotated[pair[1]] = s2_rotated
                    rotated[pair[1]][pair[0]] = s2_rotated

                    diff = s1[loc_idx1] - s2_rotated[loc_idx2]
                    mappings[pair[1]][pair[0]] = (rotation_option, diff)

                    print(f"Scanner {pair[1]} relative to scanner {pair[0]}: {diff}")
                    rel_positions.append([pair, diff])

                else:
                    rotation_option += 1

    return rel_positions, rotated, mappings


# TODO set min num overlapping to 12
def solve_1(input_array, min_num_overlapping=12):
    # for part 2
    # input_array = [np.vstack([a, [0,0,0]]) for a in input_array]

    all_rel_dists = get_all_rel_distances(input_array)
    overlap_pairs = compare_all_scanners(all_rel_dists, min_num_overlapping)

    rel_positions, rotated_locs, mappings = get_rel_positions(input_array, overlap_pairs)
    to_be_mapped = list(set([i for j in rel_positions for i in j[0]]))
    # coords = [(i, input_array[i]) for i in to_be_mapped]
    # for part 2
    coords = [(i, np.vstack([input_array[i], [0,0,0]])) for i in to_be_mapped]

    prio = 0
    mapped_to_zero = {0: prio}

    while any(i[0] != 0 for i in coords):
        prio += 1
        for idx, c in enumerate(coords):
            rot_idx = c[0]
            if rot_idx != 0:
                for pair, diff in sorted(rel_positions, key=lambda i: mapped_to_zero.get(i[0][0], 10000)):
                    # if pair[0] in mapped_to_zero and pair[1] == rot_idx:
                    if pair[1] == rot_idx:
                        print(f"Pair {pair} with diff {diff}")
                        print(f"Mapping {pair[1]} to {pair[0]}")
                        # beacons_mapped = rotated_locs[pair[1]][pair[0]] + diff
                        rotation_option, diff_ = mappings[pair[1]][pair[0]]

                        beacons_mapped = apply_rotation({0: c[1]}, rotation_option)[0] + diff

                        # print(f"Mapped beacons:")
                        # print(beacons_mapped)
                        coords[idx] = (pair[0], beacons_mapped)
                        # mapped_to_zero.append(pair[1])
                        mapped_to_zero[pair[1]] = prio
                        break

    beacon_strs = []
    # beacons = [c[1] for c in coords]
    # print(beacons)

    for c in coords:
        beacons = c[1][:-1]
        for b_pos in beacons:
            beacon_strs.append(str(b_pos))

    scanner_positions = [c[1][-1] for c in coords]
    max_mdist = -1000
    for s1 in scanner_positions:
        for s2 in scanner_positions:
            manhattan_dist = sum(np.abs(s1 - s2))
            if manhattan_dist > max_mdist:
                max_mdist = manhattan_dist
    print(max_mdist)

    return len(set(beacon_strs)), max_mdist


def solve_2(input_list):
    return


if __name__ == "__main__":
    sample1_input = read_file("data/day_19/sample1.txt")
    sample2_input = read_file("data/day_19/sample2.txt")
    real_input = read_file("data/day_19/input.txt")

    assert solve_1(sample2_input) == (79, 3621)
    assert solve_1(real_input) == (396, 11828)

    # Part 1
    # assert solve_1(sample1_input) == ..., solve_1(sample1_input)
    # assert solve_1(sample2_input) == ..., solve_1(sample2_input)
    # assert solve_1(sample3_input) == ..., solve_1(sample3_input)
    # print(solve_1(real_input))
    # assert solve_1(real_input) == ...

    # Part 2
    # assert solve_2(sample1_input) == ..., solve_2(sample1_input)
    # assert solve_2(sample2_input) == ..., solve_2(sample2_input)
    # assert solve_2(sample3_input) == ..., solve_2(sample3_input)
    # print(solve_2(real_input))
    # assert solve_2(real_input) == ...
