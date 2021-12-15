import os
from queue import PriorityQueue

import numpy as np


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    locs = []
    for idx, line in enumerate(open(input_path).readlines()):
        locs.append(list(map(int, list(line.strip()))))
    return np.array(locs).reshape(-1, idx + 1)


def get_adjacent_indices(input_array, x, y):
    shape = input_array.shape
    adjacent_indices = []
    if x != 0:
        adjacent_indices.append((x - 1, y))
    if x != shape[0] - 1:
        adjacent_indices.append((x + 1, y))
    if y != 0:
        adjacent_indices.append((x, y - 1))
    if y != shape[1] - 1:
        adjacent_indices.append((x, y + 1))
    return adjacent_indices


def get_min_costs(array):
    """https://www.redblobgames.com/pathfinding/a-star/introduction.html#dijkstra"""
    frontier = PriorityQueue()
    start = (0, 0)
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0
    goal = (array.shape[0] - 1, array.shape[1] - 1)

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            return cost_so_far[current]

        for next in get_adjacent_indices(array, *current):
            new_cost = cost_so_far[current] + array[next]
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current


def solve_1(input_array):
    return get_min_costs(input_array)


def tile_array(input_array):
    xin, yin = input_array.shape
    tiled = np.tile(input_array, (5, 5))
    xx, yy = np.meshgrid(np.arange(5 * yin), np.arange(5 * xin))
    increases = (xx // xin) + (yy // yin)
    tiled += increases
    tiled[tiled >= 10] %= 9
    return tiled


def solve_2(input_array):
    full_array = tile_array(input_array)
    return get_min_costs(full_array)


if __name__ == "__main__":
    sample1_input = read_file("data/day_15/sample1.txt")
    real_input = read_file("data/day_15/input.txt")

    # Part 1
    assert solve_1(sample1_input) == 40, solve_1(sample1_input)
    assert solve_1(real_input) == 685

    # Part 2
    assert solve_2(sample1_input) == 315, solve_2(sample1_input)
    assert solve_2(real_input) == 2995
