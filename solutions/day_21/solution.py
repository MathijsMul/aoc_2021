import os
from collections import Counter


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    return [line.strip().split("-") for line in open(input_path).readlines()]


def solve_1(init_pos):
    scores = [0, 0]
    locations = [init_pos[0], init_pos[1]]
    turn = 0
    rolls = 0
    die_side = 0

    while all(score < 1000 for score in scores):
        player = turn % 2

        total_turn = -1
        for die_roll in range(3):
            die_score = (die_side % 100) + 1
            die_side += 1
            total_turn += die_score
            rolls += 1

        locations[player] = (locations[player] + total_turn) % 10 + 1

        scores[player] += locations[player]
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
    init_state = ((0,0),(init_pos[0], init_pos[1]))
    counter = Counter([init_state])

    turn = 0
    move_counts = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
    wins1, wins2 = 0, 0

    while sum(counter.values()) > 0:
        player = turn % 2
        new_counter = Counter()
        for state, state_count in counter.items():
            for move, count in move_counts.items():
                if player == 0:
                    new_pos = (state[1][0] + move - 1) % 10 + 1
                    new_score = state[0][0] + new_pos
                    new_state = ((new_score, state[0][1]), (new_pos, state[1][1]))

                elif player == 1:
                    new_pos = (state[1][1] + move - 1) % 10 + 1
                    new_score = state[0][1] + new_pos
                    new_state = ((state[0][0], new_score), (state[1][0], new_pos))

                new_counter[new_state] += state_count * count

        # Check for winners
        counter = Counter()
        for state, state_count in new_counter.items():
            score1, score2 = state[0]
            if score1 >= 21:
                wins1 += state_count
            elif score2 >= 21:
                wins2 += state_count
            else:
                counter[state] += state_count
        turn += 1

    return max([wins1, wins2])


if __name__ == "__main__":
    sample_pos = [4, 8]
    real_pos = [10, 2]

    # Part 1
    assert solve_1(sample_pos) == 739785
    assert solve_1(real_pos) == 916083

    # Part 2
    assert solve_2(sample_pos) == 444356092776315
    assert solve_2(real_pos) == 49982165861983
