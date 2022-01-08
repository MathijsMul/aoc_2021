import os
from collections import Counter


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    data = []
    for line in open(input_path).readlines():
        l = []
        for segment in line.strip().split():
            try:
                segment = int(segment)
            except ValueError:
                pass
            l.append(segment)
        data.append(l)
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
                        self.counter.keys(),
                        key=lambda x: int(x.split("_")[1]) if "_" in x else -1,
                    )[::-1]
                ):
                    if key == "ones":
                        continue
                    elif key_idx > 0:
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
                    # Two options. Assume we always want the case where values are equal.
                    c1 = {k: v for k, v in Counter(self.counter).items() if v != 0}
                    c2 = {k: v for k, v in Counter(other.counter).items() if v != 0}

                    self.assumptions.append([c1, c2])
                    self.counter.clear()
                    self.counter["ones"] = 1


def get_equations(commands):
    values = {"w": Variable(), "x": Variable(), "y": Variable(), "z": Variable()}

    digit_idx = 0
    for command_idx, command in enumerate(commands):
        instr, var_1 = command[0], command[1]
        if instr == "inp":
            values[var_1].inp("d_" + str(digit_idx))
            digit_idx += 1
        else:
            var_2 = command[2]

            if isinstance(var_2, str):
                var_2 = values[var_2]

            if instr == "add":
                values[var_1].add(var_2)
            elif instr == "mul":
                values[var_1].mul(var_2)
            elif instr == "div":
                values[var_1].div(var_2)
            elif instr == "mod":
                values[var_1].mod(var_2)
            elif instr == "eql":
                values[var_1].eql(var_2)

    return values["x"].assumptions


def solve_1(commands):
    ass = get_equations(commands)
    model_nr = 14 * [0]
    for equation in ass:
        left, right = equation
        left_vars = [k for k in left.keys() if k != "ones"]
        right_vars = [k for k in right.keys() if k != "ones"]

        assert len(left_vars) == 1
        assert len(right_vars) == 1

        left_var = left_vars[0]
        right_var = right_vars[0]

        if left.get("ones", 0) > 0:
            left_val = 9 - left["ones"]
            right_val = 9
        elif right.get("ones", 0) > 0:
            right_val = 9 - right["ones"]
            left_val = 9
        elif left.get("ones", 0) < 0:
            left_val = 9
            right_val = 9 + left["ones"]
        elif right.get("ones", 0) < 0:
            right_val = 9
            left_val = 9 + right["ones"]
        else:
            left_val, right_val = 9, 9

        model_nr[int(left_var.split("_")[1])] = left_val
        model_nr[int(right_var.split("_")[1])] = right_val

    return int("".join(list(map(str, model_nr))))


def solve_2(commands):
    ass = get_equations(commands)
    model_nr = 14 * [0]
    for equation in ass:
        left, right = equation
        left_vars = [k for k in left.keys() if k != "ones"]
        right_vars = [k for k in right.keys() if k != "ones"]

        assert len(left_vars) == 1
        assert len(right_vars) == 1

        left_var = left_vars[0]
        right_var = right_vars[0]

        if left.get("ones", 0) > 0:
            left_val = 1
            right_val = 1 + left["ones"]
        elif right.get("ones", 0) > 0:
            right_val = 1
            left_val = 1 + right["ones"]
        elif left.get("ones", 0) < 0:
            left_val = 1 - left["ones"]
            right_val = 1
        elif right.get("ones", 0) < 0:
            right_val = 1 - right["ones"]
            left_val = 1
        else:
            left_val, right_val = 1, 1

        model_nr[int(left_var.split("_")[1])] = left_val
        model_nr[int(right_var.split("_")[1])] = right_val

    return int("".join(list(map(str, model_nr))))


if __name__ == "__main__":
    real_input = read_file("data/day_24/input.txt")
    assert solve_1(real_input) == 92915979999498
    assert solve_2(real_input) == 21611513911181
