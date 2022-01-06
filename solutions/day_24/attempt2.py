import os
from collections import defaultdict, Counter
import numpy as np
from itertools import product

from copy import deepcopy


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
                for key_idx, key in enumerate(sorted(self.counter.keys(), key=lambda x: int(x.split("_")[1]) if "_" in x else -1)[::-1]):
                    if key == "ones":
                        continue
                    elif key_idx > 0:
                        if self.counter[key] % other == 0:
                            self.counter[key] //= other
                        else:
                            raise NotImplementedError
                    elif key_idx == 0:
                        max_remainder = self.counter["ones"] % other + 9 * self.counter[key]
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
                    # Two options
                    raise ArithmeticError
                    # self.counter.clear()




def solve_1(commands):
    init_values = {"w": Variable(), "x": Variable(), "y": Variable(), "z": Variable()}
    worlds = [init_values]

    digit_idx = 0
    for command_idx, command in enumerate(commands):
        print(command)
        instr, var_1 = command[0], command[1]
        new_worlds = []
        if instr == "inp":
            for values in worlds:
                values[var_1].inp("d_" + str(digit_idx))
            digit_idx += 1
        else:
            var_2 = command[2]

            for values in worlds:
                print(values)
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
                    try:
                        values[var_1].eql(var_2)
                    except ArithmeticError:
                        # Two options; create new worlds
                        values[var_1].counter.clear()

                        # option_1 = dict(values)
                        option_2 = deepcopy(values)
                        option_2[var_1].counter["ones"] = 1
                        new_worlds.append(option_2)
                print(values)
        worlds.extend(new_worlds)

        # print(values)

        # if command_idx == 35:
        #     break
    return worlds


def solve_2(input_list):
    return


if __name__ == "__main__":
    # sample1_input = read_file("data/day_24/sample1.txt")
    # sample2_input = read_file("data/day_24/sample2.txt")
    # sample3_input = read_file("data/day_24/sample3.txt")
    real_input = read_file("data/day_24/input.txt")
    print(real_input)
    solve_1(real_input)

    # Part 1
    # assert solve_1(sample1_input) == ..., solve_1(sample1_input)
    # assert solve_1(sample2_input) == ..., solve_1(sample2_input)
    # assert solve_1(sample3_input) == ..., solve_1(sample3_input)
    # print(solve_1(real_input))
    # assert solve_1(real_input) == ...

    # Part 2
    # assert solve_2(sample1_input) == ..., solve_2(sample1_input)
    # assert solve_2(sample2_input) == ..., solve_2(sample2_input)
    # assert solve_2(sample3_input) == ..., solve_2(sample3_input)
    # print(solve_2(real_input))
    # assert solve_2(real_input) == ...
