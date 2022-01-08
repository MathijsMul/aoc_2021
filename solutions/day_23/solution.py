from queue import Queue


def cave_to_hallway(caves, hallway):
    new_states = []
    hallway_allowed = [0, 1, 3, 5, 7, 9, 10]

    for cave_idx, cave in enumerate(caves):
        cave_address = 2 + (cave_idx * 2)

        for pos_idx, amphi_type in enumerate(cave):
            if amphi_type != -1 and all(t == -1 for t in cave[pos_idx + 1 :]):
                for hallway_idx in hallway_allowed:
                    bounds = [cave_address, hallway_idx]
                    if any(
                        hallway[i] != -1 for i in range(min(bounds), max(bounds) + 1)
                    ):
                        continue

                    new_caves = (
                        (caves[:cave_idx])
                        + (cave[:pos_idx] + (-1,) + cave[pos_idx + 1 :],)
                        + caves[cave_idx + 1 :]
                    )
                    new_hallway = (
                        hallway[:hallway_idx]
                        + (amphi_type,)
                        + hallway[hallway_idx + 1 :]
                    )

                    num_steps = len(cave) - pos_idx + abs(cave_address - hallway_idx)
                    cost = num_steps * (10 ** amphi_type)

                    new_states.append(((new_caves, new_hallway), cost))
    return new_states


def hallway_to_cave(caves, hallway):
    new_states = []

    # From hallway to cave
    for hallway_idx, amphi_type in enumerate(hallway):
        cave_address = 2 + (amphi_type * 2)
        if amphi_type != -1:
            if cave_address < hallway_idx:
                if any(hallway[i] != -1 for i in range(cave_address, hallway_idx)):
                    continue
            elif cave_address > hallway_idx:
                if any(
                    hallway[i] != -1 for i in range(hallway_idx + 1, cave_address + 1)
                ):
                    continue

            dest_cave = caves[amphi_type]
            if any(t not in [-1, amphi_type] for t in dest_cave):
                continue
            for pos_idx, dest_type in enumerate(dest_cave):
                if dest_type == -1:
                    new_caves = (
                        (caves[:amphi_type])
                        + (
                            dest_cave[:pos_idx]
                            + (amphi_type,)
                            + dest_cave[pos_idx + 1 :],
                        )
                        + caves[amphi_type + 1 :]
                    )
                    new_hallway = (
                        hallway[:hallway_idx] + (-1,) + hallway[hallway_idx + 1 :]
                    )

                    num_steps = (
                        len(dest_cave) - pos_idx + abs(cave_address - hallway_idx)
                    )
                    cost = num_steps * (10 ** amphi_type)

                    new_states.append(((new_caves, new_hallway), cost))
                    break
    return new_states


def get_next_states(state):
    caves, hallway = state
    next_states = cave_to_hallway(caves, hallway) + hallway_to_cave(caves, hallway)
    return next_states


def initialize(caves):
    type_dict = {"A": 0, "B": 1, "C": 2, "D": 3}
    caves = tuple(tuple(type_dict[t] for t in cave) for cave in caves)
    init_hallway = tuple(-1 for _ in range(11))
    return (caves, init_hallway)


def solve_1(init_state):
    init_state = initialize(init_state)

    frontier = Queue()
    frontier.put(init_state)
    came_from, cost_so_far = dict(), dict()
    came_from[init_state] = None
    cost_so_far[init_state] = 0

    goal = tuple(len(init_state[0][0]) * (i,) for i in range(4))

    while not frontier.empty():
        current_state = frontier.get()
        caves, hallway = current_state

        if caves == goal:
            return cost_so_far[current_state]

        next_states = get_next_states(current_state)
        for next_state, next_cost in next_states:
            if next_state == came_from[current_state]:
                continue

            new_cost = cost_so_far[current_state] + next_cost
            if next_state not in cost_so_far or cost_so_far[next_state] > new_cost:
                cost_so_far[next_state] = new_cost
                came_from[next_state] = current_state
                frontier.put(next_state)


if __name__ == "__main__":

    # Part 1
    sample_caves = (("A", "B"), ("D", "C"), ("C", "B"), ("A", "D"))
    assert solve_1(sample_caves) == 12521

    real_caves = (("D", "B"), ("C", "B"), ("A", "C"), ("A", "D"))
    assert solve_1(real_caves) == 15111

    # Part 2
    sample_caves2 = (
        ("A", "D", "D", "B"),
        ("D", "B", "C", "C"),
        ("C", "A", "B", "B"),
        ("A", "C", "A", "D"),
    )
    assert solve_1(sample_caves2) == 44169

    real_caves2 = (
        ("D", "D", "D", "B"),
        ("C", "B", "C", "B"),
        ("A", "A", "B", "C"),
        ("A", "C", "A", "D"),
    )
    assert solve_1(real_caves2) == 47625
