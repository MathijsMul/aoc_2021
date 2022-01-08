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
    def __init__(self):
        self.counter = Counter()
        self.assumptions = []

    def __repr__(self):
        return str(self.counter)

    @property
    def max_sum(self):
        max_sum = 0
        for key in self.counter:
            if key == "ones":
                max_sum += self.counter[key]
            else:
                max_sum += 9 * self.counter[key]
        return max_sum

    @property
    def min_sum(self):
        min_sum = 0
        for key in self.counter:
            min_sum += self.counter[key]
        return min_sum

    def inp(self, other):
        self.counter.clear()
        self.counter[other] += 1

    def add(self, other):
        if isinstance(other, int):
            self.counter["ones"] += other
        elif isinstance(other, Variable):
            self.counter += other.counter

    def mul(self, other):
        if isinstance(other, int):
            for key in self.counter:
                self.counter[key] *= other
        elif isinstance(other, Variable):
            new_counter = Counter()
            for key in self.counter:
                for key_other in other.counter:
                    new_counter[key] += other.counter[key_other] * self.counter[key]
            self.counter = new_counter

    def div(self, other):
        if isinstance(other, int):
            if other == 1:
                pass
            else:
                for key_idx, key in enumerate(
                    sorted(
                        [k for k in self.counter.keys() if k != "ones"],
                    )[::-1]
                ):
                    if key_idx > 0:
                        if self.counter[key] % other == 0:
                            self.counter[key] //= other
                        else:
                            raise NotImplementedError
                    elif key_idx == 0:
                        max_remainder = (
                            self.counter["ones"] % other + 9 * self.counter[key]
                        )
                        if max_remainder < other:
                            self.counter["ones"] //= other
                            self.counter[key] = 0
                        else:
                            raise NotImplementedError
        else:
            raise NotImplementedError

    def mod(self, other):
        if isinstance(other, int):
            for key in self.counter:
                if key == "ones":
                    self.counter[key] %= other
                elif self.counter[key] % other == 0:
                    self.counter[key] = 0

        if isinstance(other, int) and other > self.max_sum:
            pass
        else:
            raise NotImplementedError

    def eql(self, other):
        if isinstance(other, int):
            if list(self.counter.keys()) == ["ones"]:
                new_val = int(self.counter["ones"] == other)
                self.counter.clear()
                self.counter["ones"] = new_val
            elif sum(self.counter) == 0 and other == 0:
                self.counter.clear()
                self.counter["ones"] = 1
            else:
                raise NotImplementedError(f"Trying to eql {self.counter} and {other}")
        if isinstance(other, Variable):
            if self.counter == other.counter:
                self.counter.clear()
                self.counter["ones"] = 1
            else:
                if self.max_sum < other.min_sum or other.max_sum < self.min_sum:
                    self.counter.clear()
                    self.counter["ones"] = 0
                else:
                    # Two options. Assume we always want the case where values are equal, in order
                    # to minimize z.
                    self.add_assumption(other)
                    self.counter.clear()
                    self.counter["ones"] = 1

    @property
    def non_zero_counts(self):
        return {k: v for k, v in Counter(self.counter).items() if v != 0}

    def add_assumption(self, other):
        self.assumptions.append([self.non_zero_counts, other.non_zero_counts])


def get_equations(commands):
    values = {var: Variable() for var in ["w", "x", "y", "z"]}

    digit_idx = 0
    for command_idx, command in enumerate(commands):
        instr, var_1 = command[0], command[1]
        if instr == "inp":
            var_2 = digit_idx
            digit_idx += 1
        else:
            var_2 = command[2]
            if isinstance(var_2, str):
                var_2 = values[var_2]
        getattr(values[var_1], instr)(var_2)

    return values["x"].assumptions


def get_var(equation_side):
    vars = [k for k in equation_side.keys() if k != "ones"]
    assert len(vars) == 1
    return vars[0]


def solve(commands, init_val, mode):
    ass = get_equations(commands)
    model_nr = 14 * [0]
    for equation in ass:
        left, right = equation
        left_val, right_val = init_val, init_val
        constant = left.get("ones", 0)

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
    assert solve_1(real_input) == 92915979999498
    assert solve_2(real_input) == 21611513911181
