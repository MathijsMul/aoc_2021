from collections import defaultdict, Counter

from utils import read_file


def parse_input(input_path: str):
    return [line.strip().split("-") for line in read_file(input_path)]


def get_map(connections):
    cave_map = defaultdict(list)
    for cave1, cave2 in connections:
        if cave1 != "end" and cave2 != "start":
            cave_map[cave1].append(cave2)
        if cave1 != "start" and cave2 != "end":
            cave_map[cave2].append(cave1)
    return cave_map


def get_small_cave_count(path):
    return Counter(
        list(filter(lambda loc: loc.islower() and loc not in ["start", "end"], path))
    ).values()


def small_cave_check_1(path):
    return all(count <= 1 for count in get_small_cave_count(path))


def small_cave_check_2(path):
    sorted_counts = sorted(get_small_cave_count(path))
    return (
        not sorted_counts
        or all(count <= 1 for count in sorted_counts[:-1])
        and sorted_counts[-1] <= 2
    )


def compute_valid_paths(cave_map, criterion):
    path_stack = [["start"]]
    valid_paths = []

    while len(path_stack) > 0:
        current_path = path_stack.pop()
        for dest in cave_map[current_path[-1]]:
            path = current_path + [dest]
            if dest == "end":
                valid_paths.append(path)
            elif criterion(path):
                path_stack.append(path)
    return len(valid_paths)


def solve_1(input_list):
    map = get_map(input_list)
    return compute_valid_paths(map, small_cave_check_1)


def solve_2(input_list):
    map = get_map(input_list)
    return compute_valid_paths(map, small_cave_check_2)


if __name__ == "__main__":
    sample1_input = parse_input("data/day_12/sample1.txt")
    sample2_input = parse_input("data/day_12/sample2.txt")
    sample3_input = parse_input("data/day_12/sample3.txt")
    real_input = parse_input("data/day_12/input.txt")

    # Part 1
    assert solve_1(sample1_input) == 10, solve_1(sample1_input)
    assert solve_1(sample2_input) == 19, solve_1(sample2_input)
    assert solve_1(sample3_input) == 226, solve_1(sample3_input)
    assert solve_1(real_input) == 4241

    # Part 2
    assert solve_2(sample1_input) == 36, solve_2(sample1_input)
    assert solve_2(sample2_input) == 103, solve_2(sample2_input)
    assert solve_2(sample3_input) == 3509, solve_2(sample3_input)
    assert solve_2(real_input) == 122134
