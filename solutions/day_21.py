import os
from collections import Counter
from itertools import product


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    return [line.strip().split("-") for line in open(input_path).readlines()]


def solve_1(init_pos):
    scores = [0, 0]
    locations = [init_pos[0], init_pos[1]]
    player, rolls, die_side = 0, 0, 0

    while all(score < 1000 for score in scores):
        total_turn = -1
        for die_roll in range(3):
            die_score = (die_side % 100) + 1
            die_side += 1
            total_turn += die_score
            rolls += 1

        locations[player] = (locations[player] + total_turn) % 10 + 1
        scores[player] += locations[player]
        player = 1 - player

    return min(scores) * rolls


def get_new_state(old_state, player, move):
    scores, positions = old_state

    new_positions = list(positions)
    new_positions[player] = (positions[player] + move - 1) % 10 + 1

    new_scores = list(scores)
    new_scores[player] += new_positions[player]

    return (tuple(new_scores), tuple(new_positions))


def solve_2(init_pos):
    # State has structure ((score_1, score_2), (pos_1, pos_2))
    init_state = ((0, 0), init_pos)
    state_counter = Counter([init_state])

    move_counter = Counter([sum(prod) for prod in product([1, 2, 3], repeat=3)])
    player = 0
    wins = [0,0]

    while sum(state_counter.values()) > 0:
        new_state_counter = Counter()
        for state, state_count in state_counter.items():
            for move, count in move_counter.items():
                new_state = get_new_state(state, player, move)
                new_state_counter[new_state] += state_count * count

        # Check for winners
        state_counter = Counter()
        for state, state_count in new_state_counter.items():
            scores = state[0]
            if scores[0] >= 21:
                wins[0] += state_count
            elif scores[1] >= 21:
                wins[1] += state_count
            else:
                state_counter[state] += state_count

        player = 1 - player

    return max(wins)


if __name__ == "__main__":
    sample_pos = (4, 8)
    real_pos = (10, 2)

    # Part 1
    assert solve_1(sample_pos) == 739785
    assert solve_1(real_pos) == 916083

    # Part 2
    assert solve_2(sample_pos) == 444356092776315
    assert solve_2(real_pos) == 49982165861983
