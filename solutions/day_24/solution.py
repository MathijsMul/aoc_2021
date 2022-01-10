from __future__ import annotations

import os
from collections import Counter


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    data = []
    with open(input_path) as file:
        for line in file.readlines():
            command = []
            for segment in line.strip().split():
                try:
                    segment = int(segment)
                except ValueError:
                    pass
                command.append(segment)
            data.append(command)
    return data


class Variable:
    def __init__(self, init_counts: dict = None):
        self.counter = Counter(init_counts)
        self.equations = []

    @property
    def max_sum(self):
        return 9 * self.min_sum - 8 * self.offset

    @property
    def min_sum(self):
        return sum(self.counter.values())

    @property
    def offset(self):
        return self.counter[-1]

    @property
    def no_vars(self):
        return list(self.counter.keys()) == [-1]

    def set_offset(self, offset):
        self.counter[-1] = offset

    def inp(self, other: Variable):
        self.counter = other.counter

    def add(self, other: Variable):
        self.counter.update(other.counter)

    def mul(self, other: Variable):
        new_counter = Counter()
        for key in self.counter:
            for key_other in other.counter:
                new_counter[key] += other.counter[key_other] * self.counter[key]
        self.counter = new_counter

    def div(self, other: Variable):
        for key_idx, key in enumerate(
            sorted(
                [k for k, v in self.counter.items() if v != 0],
                reverse=True,
            )[:-1]
        ):
            if key_idx > 0 and self.counter[key] % other.offset == 0:
                self.counter[key] //= other.offset
            elif key_idx == 0:
                max_remainder = self.offset % other.offset + 9 * self.counter[key]
                if max_remainder < other.offset:
                    self.set_offset(self.offset // other.offset)
                    self.counter[key] = 0

    def mod(self, other: Variable):
        for key in self.counter:
            self.counter[key] %= other.offset

    def eql(self, other: Variable):
        if self.no_vars and other.no_vars:
            new_val = int(self.offset == other.offset)
        elif self.max_sum < other.min_sum or other.max_sum < self.min_sum:
            new_val = 0
        else:
            # Assume we always want the case where values are equal, in order to minimize z.
            self.equations.append([Counter(self.counter), Counter(other.counter)])
            new_val = 1
        self.counter.clear()
        self.set_offset(new_val)


def get_equations(commands):
    values = {var: Variable() for var in ["w", "x", "y", "z"]}

    digit_idx = 0
    for command_idx, command in enumerate(commands):
        instr, var_1 = command[0], command[1]
        if instr == "inp":
            var_2 = Variable({digit_idx: 1})
            digit_idx += 1
        else:
            if isinstance(command[2], str):
                var_2 = values[command[2]]
            elif isinstance(command[2], int):
                var_2 = Variable({-1: command[2]})
            else:
                raise ValueError
        getattr(values[var_1], instr)(var_2)

    return values["x"].equations


def get_var(equation_side):
    vars = [key for key, count in equation_side.items() if key != -1 and count != 0]
    assert len(vars) == 1, vars
    return vars[0]


def solve(commands, init_val, mode):
    ass = get_equations(commands)
    model_nr = 14 * [0]
    for equation in ass:
        left, right = equation
        left_val, right_val = init_val, init_val
        constant = left.get(-1, 0)

        right_val += (mode * constant < 0) * constant
        left_val -= (mode * constant > 0) * constant

        model_nr[get_var(left)] = left_val
        model_nr[get_var(right)] = right_val

    return int("".join(list(map(str, model_nr))))


def solve_1(commands):
    return solve(commands, 9, 1)


def solve_2(commands):
    return solve(commands, 1, -1)


if __name__ == "__main__":
    real_input = read_file("data/day_24/input.txt")
    assert solve_1(real_input) == 92915979999498, solve_1(real_input)
    assert solve_2(real_input) == 21611513911181
