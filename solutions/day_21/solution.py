import os
from collections import defaultdict, Counter
import numpy as np
from itertools import product


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    return [line.strip().split("-") for line in open(input_path).readlines()]


def solve_1(init_pos):
    scores = [0, 0]
    locations = init_pos
    turn = 0
    rolls = 0
    die_side = 0

    while all(score < 1000 for score in scores):
        player = turn % 2
        print(f"Player {player} rolls ")

        total_turn = -1
        for die_roll in range(3):
            die_score = (die_side % 100) + 1
            die_side += 1
            print(f"Die rolls {die_score}")
            total_turn += die_score
            rolls += 1

        locations[player] = (locations[player] + total_turn) % 10 + 1

        print(f"Moves to {locations[player]}")
        scores[player] += locations[player]
        print(f"Total score: {scores[player]}")
        turn += 1

    return min(scores) * rolls


def get_turn_counts(init_pos_player):
    pos_score_turn_counter = Counter([(init_pos_player, 0, 0)])

    while any(score < 21 for _, score, _ in pos_score_turn_counter):
        new_counter = Counter()
        for (pos, score, turn), count in pos_score_turn_counter.items():
            if score >= 21:
                new_counter[(pos, score, turn)] += count
            else:
                move_counts = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
                for move, freq in move_counts.items():
                    new_pos = (pos + move - 1) % 10 + 1
                    new_counter[(new_pos, score + new_pos, turn + 1)] += freq
        pos_score_turn_counter = new_counter

    turn_counts = Counter()
    for (pos, score, turn), count in pos_score_turn_counter.items():
        turn_counts[turn] += count
    return turn_counts


def solve_2(init_pos):
    init_state = ((0,0),(init_pos[0], init_pos[1]),1)
    queue = [init_state]

    turn = 0
    move_counts = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
    wins1, wins2 = 0, 0

    while len(queue) > 0:
        # Play one turn
        print(f"Turn {turn}; queue size: {len(queue)}")

        player = turn % 2
        new_queue = []
        for state in queue:
            state_count = state[2]
            for move, count in move_counts.items():
                if player == 0:
                    new_pos = (state[1][0] + move - 1) % 10 + 1
                    new_score = state[0][0] + new_pos
                    new_state = ((new_score, state[0][1]), (new_pos, state[1][1]), state_count * count)
                elif player == 1:
                    new_pos = (state[1][1] + move - 1) % 10 + 1
                    new_score = state[0][1] + new_pos
                    new_state = ((state[0][0], new_score), (state[1][0], new_pos), state_count * count)

                new_queue.append(new_state)

        # Check for winners
        queue = []
        for state in new_queue:
            score1, score2 = state[0]
            state_count = state[2]
            if score1 >= 21:
                wins1 += state_count
            elif score2 >= 21:
                wins2 += state_count
            else:
                queue.append(state)
        turn += 1

    return wins1, wins2

# def solve_2(init_pos):
#     roll_options = list(product([1, 2, 3], repeat=3))
#     move_options = Counter([sum(r) for r in roll_options])
#
#     counts_player_1 = get_turn_counts(init_pos_player=init_pos[0])
#     counts_player_2 = get_turn_counts(init_pos_player=init_pos[1])
#
#     wins_1, wins_2 = 0, 0
#     for num_turns_1, count_1 in counts_player_1.items():
#         for num_turns_2, count_2 in counts_player_2.items():
#             if num_turns_1 < num_turns_2:
#                 wins_1 += count_1 * count_2
#             elif num_turns_2 < num_turns_1:
#                 wins_2 += count_1 * count_2
#             elif num_turns_1 == num_turns_2:
#                 wins_1 += count_1 * count_2
#
#     return wins_1, wins_2
#     # Player 0
#
#     # return turn_counts
#     # return pos_score_turn_counter


if __name__ == "__main__":
    sample_pos = [4, 8]
    real_pos = [10, 2]

    # Part 1
    # assert solve_1(sample_pos) == 739785
    # assert solve_1(real_pos) == 916083

    # Part 2
    c = solve_2(sample_pos)
    print(c)

    # player 1
    # 444356092776315
    # player 2
    # 341960390180808
