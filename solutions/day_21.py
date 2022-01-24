from collections import Counter
from itertools import product

from utils import read_file


def parse_input(input_path: str):
    return [line.strip().split("-") for line in read_file(input_path)]


def solve_1(init_pos):
    state = ((0, 0), init_pos)
    player, rolls, die_side = 0, 0, 0

    while all(score < 1000 for score in state[0]):
        total_turn = 0
        for die_roll in range(3):
            total_turn += (die_side % 100) + 1
            die_side += 1
            rolls += 1

        state = get_new_state(state, player, total_turn)
        player = 1 - player

    return min(state[0]) * rolls


def get_new_state(old_state, player, move):
    """State has structure ((score_1, score_2), (pos_1, pos_2))."""
    scores, positions = old_state
    new_positions, new_scores = list(positions), list(scores)

    new_positions[player] = (positions[player] + move - 1) % 10 + 1
    new_scores[player] += new_positions[player]

    return tuple(new_scores), tuple(new_positions)


def check_winners(wins, new_state_counter):
    """Check for winners."""
    state_counter = Counter()
    for state, state_count in new_state_counter.items():
        scores, _ = state
        if scores[0] >= 21:
            wins[0] += state_count
        elif scores[1] >= 21:
            wins[1] += state_count
        else:
            state_counter[state] += state_count
    return wins, state_counter


def solve_2(init_pos):
    init_state = ((0, 0), init_pos)
    state_counter = Counter([init_state])

    move_counter = Counter([sum(prod) for prod in product([1, 2, 3], repeat=3)])
    player, wins = 0, [0, 0]

    while sum(state_counter.values()):
        new_state_counter = Counter()
        for state, state_count in state_counter.items():
            for move, count in move_counter.items():
                new_state = get_new_state(state, player, move)
                new_state_counter[new_state] += state_count * count

        wins, state_counter = check_winners(wins, new_state_counter)
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
