"""
TODO FIX THIS
"""

from queue import Queue


# def get_new_positions(positions, idx, new_value):
#     return (
#             (positions[:idx])
#             + (cave[:idx] + (-1,) + cave[idx + 1:],)
#             + positions[idx + 1:]
#     )
#     new_hallway = (
#             hallway[:hallway_idx]
#             + (amphi_type,)
#             + hallway[hallway_idx + 1:]
#     )


def get_next_states(state):
    # caves, hallway = state
    next_states = []
    hallway_allowed = [0, 1, 3, 5, 7, 9, 10]
    cave_len = len(state) // 4

    for amphi_idx, (amphi_type, (cave_idx, cave_pos), num_moves) in enumerate(state):
        if num_moves >= 2:
            break
        elif cave_idx == -1:
            # Amphi in hallway
            cave_address = 2 + (amphi_type * 2)

            # todo rename to sth generic because we are now in hallway
            if cave_address < cave_pos:
                if any(
                    t[1][0] == -1 and cave_address <= t[1][1] < cave_pos for t in state
                ):
                    continue
            elif cave_address > cave_idx:
                if any(
                    t[1][0] == -1 and cave_pos < t[1][1] <= cave_address for t in state
                ):
                    continue
            if any(
                t[0] != amphi_type
                for t in filter(lambda amphi: amphi[1][0] == amphi_type, state)
            ):
                continue

            for pos_idx in range(cave_len)[::-1]:
                if any(t[1][0] == amphi_type and t[1][1] == pos_idx for t in state):
                    break

                new_state = (
                    state[:amphi_idx]
                    + ((
                        amphi_type,
                        (amphi_type, pos_idx),
                        num_moves + 1,),
                    )
                    + state[amphi_idx + 1 :]
                )

                num_steps = (
                    cave_len - pos_idx + abs(cave_address - cave_pos)
                )
                cost = num_steps * (10 ** amphi_type)

                next_states.append((new_state, cost))
        else:
            # Amphi in cave
            cave_address = 2 + (cave_idx * 2)
            if all(
                t[0] == -1
                for t in filter(
                    lambda amphi: amphi[1][0] == cave_idx and amphi[1][1] > cave_pos,
                    state
                )
            ):
                for hallway_idx in hallway_allowed:
                    bounds = [cave_address, hallway_idx]
                    if any(
                        t[0] != -1
                        for t in filter(
                            lambda amphi: amphi[1][0] == -1
                            and min(bounds) <= amphi[1][1] <= max(bounds),
                            state,
                        )
                    ):
                        continue
                    new_state = (
                        state[:amphi_idx]
                        + ((
                            amphi_type,
                            (-1, hallway_idx),
                            num_moves + 1,),
                        )
                        + state[amphi_idx + 1 :]
                    )

                    num_steps = cave_len - cave_pos + abs(cave_address - hallway_idx)
                    cost = num_steps * (10 ** amphi_type)

                    next_states.append((new_state, cost))

    # From cave to hallway
    # for cave_idx, cave in enumerate(caves):
    #     cave_address = 2 + (cave_idx * 2)
    #
    #     for pos_idx, amphi_type in enumerate(cave):
    #         if amphi_type != -1 and all(t == -1 for t in cave[pos_idx + 1 :]):
    #             for hallway_idx in hallway_allowed:
    #                 bounds = [cave_address, hallway_idx]
    #                 if any(
    #                     hallway[i] != -1 for i in range(min(bounds), max(bounds) + 1)
    #                 ):
    #                     continue
    #
    #                 new_caves = (
    #                     (caves[:cave_idx])
    #                     + (cave[:pos_idx] + (-1,) + cave[pos_idx + 1 :],)
    #                     + caves[cave_idx + 1 :]
    #                 )
    #                 new_hallway = (
    #                     hallway[:hallway_idx]
    #                     + (amphi_type,)
    #                     + hallway[hallway_idx + 1 :]
    #                 )
    #
    #                 num_steps = len(cave) - pos_idx + abs(cave_address - hallway_idx)
    #                 cost = num_steps * (10 ** amphi_type)
    #
    #                 next_states.append(((new_caves, new_hallway), cost))
    #
    # # From hallway to cave
    # for hallway_idx, amphi_type in enumerate(hallway):
    #     cave_address = 2 + (amphi_type * 2)
    #     if amphi_type != -1:
    #         if cave_address < hallway_idx:
    #             if any(hallway[i] != -1 for i in range(cave_address, hallway_idx)):
    #                 continue
    #         elif cave_address > hallway_idx:
    #             if any(
    #                 hallway[i] != -1 for i in range(hallway_idx + 1, cave_address + 1)
    #             ):
    #                 continue
    #
    #         dest_cave = caves[amphi_type]
    #         if any(t not in [-1, amphi_type] for t in dest_cave):
    #             continue
    #         for pos_idx, dest_type in enumerate(dest_cave):
    #             if dest_type == -1:
    #                 new_caves = (
    #                     (caves[:amphi_type])
    #                     + (
    #                         dest_cave[:pos_idx]
    #                         + (amphi_type,)
    #                         + dest_cave[pos_idx + 1 :],
    #                     )
    #                     + caves[amphi_type + 1 :]
    #                 )
    #                 new_hallway = (
    #                     hallway[:hallway_idx] + (-1,) + hallway[hallway_idx + 1 :]
    #                 )
    #
    #                 num_steps = (
    #                     len(dest_cave) - pos_idx + abs(cave_address - hallway_idx)
    #                 )
    #                 cost = num_steps * (10 ** amphi_type)
    #
    #                 next_states.append(((new_caves, new_hallway), cost))
    #                 break

    return next_states


def initialize(caves):
    type_dict = {"A": 0, "B": 1, "C": 2, "D": 3}
    # caves = tuple(tuple(type_dict[t] for t in cave) for cave in state)
    # init_hallway = tuple(-1 for _ in range(11))
    # return (caves, init_hallway)
    state = tuple()
    for cave_idx, cave in enumerate(caves):
        for pos_idx, amphi in enumerate(cave):

            state += ((type_dict[amphi], (cave_idx, pos_idx), 0),)
    return state


def solve_1(init_state):
    init_state = initialize(init_state)

    frontier = Queue()
    frontier.put(init_state)
    came_from, cost_so_far = dict(), dict()
    came_from[init_state] = None
    cost_so_far[init_state] = 0

    # goal = tuple(len(init_state[0][0]) * (i,) for i in range(4))

    while not frontier.empty():
        current_state = frontier.get()
        print(current_state)
        # caves, hallway = current_state

        # if caves == goal:
        if all(
            amphi_type == cave_idx for amphi_type, (cave_idx, _), _ in current_state
        ):
            return cost_so_far[current_state]

        next_states = get_next_states(current_state)
        assert 1 == 1
        # print(next_states)
        for next_state, next_cost in next_states:
            if next_state == came_from[current_state]:
                continue

            new_cost = cost_so_far[current_state] + next_cost
            if next_state not in cost_so_far or cost_so_far[next_state] > new_cost:
                cost_so_far[next_state] = new_cost
                came_from[next_state] = current_state
                frontier.put(next_state)


if __name__ == "__main__":

    sample_caves = (("A", "B"), ("D", "C"), ("C", "B"), ("A", "D"))
    assert solve_1(sample_caves) == 12521

    # real_caves = (("D", "B"), ("C", "B"), ("A", "C"), ("A", "D"))
    # assert solve_1(real_caves) == 15111
    #
    # # Part 2
    # sample_caves2 = (
    #     ("A", "D", "D", "B"),
    #     ("D", "B", "C", "C"),
    #     ("C", "A", "B", "B"),
    #     ("A", "C", "A", "D"),
    # )
    # assert solve_1(sample_caves2) == 44169
    #
    # real_caves2 = (
    #     ("D", "D", "D", "B"),
    #     ("C", "B", "C", "B"),
    #     ("A", "A", "B", "C"),
    #     ("A", "C", "A", "D"),
    # )
    # assert solve_1(real_caves2) == 47625
