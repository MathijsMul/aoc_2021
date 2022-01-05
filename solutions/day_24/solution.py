import os
from collections import defaultdict, Counter
import numpy as np
from typing import Iterable


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    return [line.strip().split(" ") for line in open(input_path).readlines()]


def solve_1x(program):
    var_dict = {"w": 0, "x": 0, "y": 0, "z": 0}
    max_code = ""
    z_out = 0

    for char_idx in range(14)[::-1]:
        print(f"Char idx: {char_idx}")
        subprogram = program[18 * char_idx : 18 * char_idx + 18]
        coef1 = int(subprogram[4][2])
        coef4 = int(subprogram[5][2])
        coef6 = int(subprogram[15][2])

        max_new = None
        var_in = dict(var_dict)

        for new_char in range(1, 10)[::-1]:

            # new_w = new_char
            # new_x = int(((var_in["z"] % 26) + coef4) != new_char)
            # new_z = ((new_char + coef6) * new_x) + (
            #     (var_in["z"] // coef1) * (1 + (25 * new_x))
            # )

            # Suppose x = 0
            z_in_range = [z_out * coef1 + i for i in range(coef1)]
            z_in_options = []
            added = False
            for option in z_in_range:
                if option % 26 + coef4 == new_char:
                    z_out = option
                    max_code = str(new_char) + max_code
                    print(f"Adding {new_char}")
                    added = True
                    break
            if added:
                break
            else:
                # Suppose x = 1
                unrounded = (-new_char - coef6) / 26
                rounded = (-new_char - coef6) // 26

                if rounded == unrounded:
                    # o = (-new_char - coef6) // 26
                    z_in_range = [rounded * coef1 + i for i in range(coef1)]

                    for option in z_in_range:
                        if option % 26 + coef4 != new_char:
                            z_out = option
                            max_code = str(new_char) + max_code
                            print(f"Adding {new_char}")
                            added = True
                            break
            if added:
                break

        # if max_new is None:
        #     return
        # max_code += str(max_new)
    return max_code


def solve_1(program):
    var_dict = {"w": 0, "x": 0, "y": 0, "z": 0}

    for char_idx in range(14):
        subprogram = program[18 * char_idx: 18 * char_idx + 18]

        for new_char in range(1,9)[::-1]:
            for instruction in subprogram:
                var_dict = apply_instruction(var_dict, instruction, new_char)
        

def solve_2(input_list):
    return


def apply_instruction(vars, line, new_char):
    instruction = line[0]
    if instruction == "inp":
        receiver = line[1]
        input = int(new_char)
        vars[receiver] = input
        # print(f"Assigning input {input} to {receiver}")
    else:
        arg1, arg2 = line[1], line[2]
        val1 = vars[arg1]
        if arg2 in vars:
            val2 = vars[arg2]
        else:
            val2 = int(arg2)

        if instruction == "add":
            vars[arg1] += val2
        elif instruction == "mul":
            vars[arg1] *= val2
        elif instruction == "div":
            vars[arg1] //= val2
        elif instruction == "mod":
            vars[arg1] %= val2
        elif instruction == "eql":
            vars[arg1] = int(val1 == val2)
    return vars


def apply_alu(inputs, program, vars):
    # vars = {"w": 0, "x": 0, "y": 0, "z": 0}
    inputs = iter(inputs)

    for idx, line in enumerate(program):
        instruction = line[0]
        if instruction == "inp":
            receiver = line[1]
            input = int(next(inputs))
            vars[receiver] = input
            # print(f"Assigning input {input} to {receiver}")
        else:
            arg1, arg2 = line[1], line[2]
            val1 = vars[arg1]
            if arg2 in vars:
                val2 = vars[arg2]
            else:
                val2 = int(arg2)

            if instruction == "add":
                vars[arg1] += val2
            elif instruction == "mul":
                vars[arg1] *= val2
            elif instruction == "div":
                vars[arg1] //= val2
            elif instruction == "mod":
                vars[arg1] %= val2
            elif instruction == "eql":
                vars[arg1] = int(val1 == val2)
    return vars


def get_final_z(model_nr, coefs):
    z_in = 0
    for idx, char in enumerate(str(model_nr)):
        if char == "0":
            return -1
        new_nr = int(char)

        # instructions = program[idx * 18: idx * 18 + 18]
        # assert instructions[0][0] == "inp"

        # coef2 = int(instructions[9][2])
        # assert coef2 == 25
        # coef3 = int(instructions[3][2])
        # assert coef3 == 26
        # coef5 = int(instructions[11][2])
        # assert coef5 == 1

        # coef1 = int(instructions[4][2])
        # coef4 = int(instructions[5][2])
        # coef6 = int(instructions[15][2])
        coef1, coef4, coef6 = coefs[idx]
        # print(coef1, coef4, coef6)

        x = int(((z_in % 26) + coef4) != new_nr)
        z_out = (z_in // coef1) * (25 * x + 1) + (x * (new_nr + coef6))
        z_in = z_out
        # TODO identify cases where z can never be 0

    return z_out


def get_coefs(program):
    idx = 0
    coefs = []
    while idx < len(program):
        p = program[idx : idx + 18]
        coefs.append(list(map(int, [p[4][2], p[5][2], p[15][2]])))
        idx += 18
    return coefs


def monad_check1(model_nr, monad):
    coefs = get_coefs(monad)
    final_z = get_final_z(model_nr, coefs)
    return final_z


def monad_check2(model_nr, monad):
    model_str = str(model_nr)
    if "0" in model_str:
        return -1
    model_str_iter = iter(model_str)
    out_vars = apply_alu(model_str_iter, monad)
    final_z = out_vars["z"]
    return final_z


if __name__ == "__main__":
    sample_prog1 = read_file("data/day_24/sample1.txt")
    sample_prog2 = read_file("data/day_24/sample2.txt")
    sample_prog3 = read_file("data/day_24/sample3.txt")
    program = read_file("data/day_24/input.txt")

    # assert apply_alu((999,), sample_prog1)["x"] == -999
    # assert apply_alu((-10,), sample_prog1)["x"] == 10
    # assert apply_alu((30, 90), sample_prog2)["z"] == 1
    # assert apply_alu((30, 91), sample_prog2)["z"] == 0
    # assert apply_alu((-10, 3), sample_prog2)["z"] == 0
    #
    # for i in range(15):
    #     assert int("".join(map(str, apply_alu((i,), sample_prog3).values())), 2) == i

    o = solve_1(program)
    print(o)

    # z_in = None
    # w_out = None

    # for w_out in range(1,9)[::-1]:
    # for w_out in [9]:
    #     for z_in in [14]:
    #         x_out = int(((z_in % 26) - 5) != w_out)
    #         z_out = ((w_out + 14) * x_out) + ((z_in // 26) * (1 + 25 * x_out))
    #         print(z_out)


    # sample_nr = 13579246899999
    # monad_check1(sample_nr, program)
    #
    # for nr in range(sample_nr, sample_nr + 100):
    #     assert monad_check1(nr, program) == monad_check2(nr, program)

    # out = monad_check(13579246899999, program)
    # print(out)

    # exit()
    # out = monad_check(99999999999999, program)
    # print(out)

    # for i in range(10 ** 14)[::-1]:
    #     if i % (10 ** 4) == 0:
    #         print(f"Tried {i} nrs")
    #
    #     check = monad_check(i, program)
    #     if check == 0:
    #         print(i)
    #         break
