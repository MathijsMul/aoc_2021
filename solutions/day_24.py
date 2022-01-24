from __future__ import annotations

from collections import Counter
from typing import List, Union, Callable

from utils import read_file


def parse_input(input_path: str):
    data = []
    for line in read_file(input_path):
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
    def __init__(self, init_counts: dict = None, offset: int = 0):
        self.counter = Counter(init_counts)
        self.set_offset(offset)
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

    @property
    def main_var(self):
        return next(
            key for key, count in self.counter.items() if key != -1 and count != 0
        )

    def set_offset(self, offset: int):
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
            self.equations.append((self.main_var, other.main_var, self.offset))
            new_val = 1
        self.counter.clear()
        self.set_offset(new_val)


def get_equations(commands: List[List[Union[str, int]]]):
    values = {var: Variable() for var in ["w", "x", "y", "z"]}

    digit_idx = 0
    for command_idx, command in enumerate(commands):
        instr, var_1 = command[0], command[1]
        if instr == "inp":
            var_2 = Variable({digit_idx: 1})
            digit_idx += 1
        elif isinstance(command[2], str):
            var_2 = values[command[2]]
        elif isinstance(command[2], int):
            var_2 = Variable(offset=command[2])
        else:
            raise ValueError
        getattr(values[var_1], instr)(var_2)

    return values["x"].equations


def solve(commands: List[List[Union[str, int]]], init_val: int, method: Callable):
    mode = method(-1, 1)
    system = get_equations(commands)
    model_nr = 14 * [0]
    for equation in system:
        left_var, right_var, constant = equation
        model_nr[left_var] = init_val - (mode * constant > 0) * constant
        model_nr[right_var] = init_val + (mode * constant < 0) * constant

    return int("".join(map(str, model_nr)))


def solve_1(commands):
    """Get maximum model nr."""
    return solve(commands, 9, max)


def solve_2(commands):
    """Get minimum model nr."""
    return solve(commands, 1, min)


if __name__ == "__main__":
    real_input = parse_input("data/day_24/input.txt")
    assert solve_1(real_input) == 92915979999498
    assert solve_2(real_input) == 21611513911181
