import os


def read_file(input_path: str):
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
    )
    return [line.strip() for line in open(input_path).readlines()]


def solve_1(input_list):
    return


def solve_2(input_list):
    return


def explode(sf_str):
    # Apply single explode action
    sf_list = sf_str_to_list(sf_str)

    nesting = 0
    last_reg_idx, last_reg_value = None, None
    next_reg_idx, next_reg_value = None, None

    for idx, char in enumerate(sf_list):
        if char == "[":
            nesting += 1
        elif char == "]":
            nesting -= 1
        else:
            try:
                last_reg_value = int(char)
                last_reg_idx = idx
            except ValueError:
                continue

        if nesting == 5:
            try:
                left = int(sf_list[idx + 1])
                right = int(sf_list[idx + 3])

                if last_reg_value is not None:
                    last_reg_value += left

                # Find next reg
                for idx2, char2 in enumerate(sf_list[idx + 4 :]):
                    try:
                        next_reg_value = int(char2)
                        next_reg_idx = idx2 + idx
                        break
                    except ValueError:
                        continue

                if next_reg_value is not None:
                    next_reg_value += right

                result = sf_list[:idx] + ["0"] + sf_list[idx + 5 :]

                if last_reg_idx:
                    result[last_reg_idx] = last_reg_value
                if next_reg_idx:
                    result[next_reg_idx] = next_reg_value

                return "".join(map(str, result))
            except ValueError:
                continue
    return sf_str


def sf_str_to_list(sf_str):
    sf_list = list(sf_str)
    new_list = []

    int_stack = []
    for char in sf_list:
        if char in ["[", "]", ","]:
            if int_stack:
                new_int = int("".join(int_stack))
                new_list.append(new_int)
                int_stack = []
            new_list.append(char)
        elif char in [str(i) for i in range(10)]:
            int_stack.append(char)

    return new_list


def split(sf_str):
    # Apply single split action
    sf_list = sf_str_to_list(sf_str)
    for idx, char in enumerate(sf_list):
        try:
            reg_value = int(char)
            if reg_value >= 10:
                left = reg_value // 2
                right = left if reg_value % 2 == 0 else left + 1
                new_pair = [left, right]
                sf_list[idx] = new_pair
                return "".join(map(str, sf_list)).replace(" ", "")
        except ValueError:
            continue
    return sf_str


def reduce(sf_str):
    change = True

    while change:
        sf_start = sf_str

        sf_str = explode(sf_str)
        if sf_start != sf_str:
            continue

        sf_str = split(sf_str)
        change = sf_start != sf_str

    return sf_str


def add_single(sf_str1, sf_str2):
    sf_str = f"[{sf_str1},{sf_str2}]"
    return reduce(sf_str)


def add(nrs):
    sf_nr1 = nrs[0]
    for idx, sf_nr2 in enumerate(nrs):
        if idx > 0:
            sf_nr1 = add_single(sf_nr1, sf_nr2)
    return reduce(sf_nr1)


def compute_magnitude(sf):
    if isinstance(sf, str):
        sf = eval(sf)
    if isinstance(sf, int):
        return sf
    else:
        return 3 * compute_magnitude(sf[0]) + 2 * compute_magnitude(sf[1])


def get_max_magnitude(sfnrs):
    sums = []
    for idx, sfnr in enumerate(sfnrs):
        for idx2, sfnr2 in enumerate(sfnrs):
            if idx != idx2:
                sum = add_single(sfnr, sfnr2)
                sums.append(compute_magnitude(sum))
    return max(sums)


if __name__ == "__main__":
    sample1_input = read_file("data/day_18/sample1.txt")
    sample2_input = read_file("data/day_18/sample2.txt")
    sample3_input = read_file("data/day_18/sample3.txt")
    real_input = read_file("data/day_18/input.txt")

    # Part 1
    explode_sample_1 = "[[[[[9,8],1],2],3],4]"
    explode_sample_2 = "[7,[6,[5,[4,[3,2]]]]]"
    explode_sample_3 = "[[6,[5,[4,[3,2]]]],1]"
    explode_sample_4 = "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]"
    explode_sample_5 = "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
    explode_sample_6 = "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"

    assert explode(explode_sample_1) == "[[[[0,9],2],3],4]"
    assert explode(explode_sample_2) == "[7,[6,[5,[7,0]]]]"
    assert explode(explode_sample_3) == "[[6,[5,[7,0]]],3]"
    assert explode(explode_sample_4) == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
    assert explode(explode_sample_5) == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"
    assert explode(explode_sample_6) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"

    split_sample_1 = "[[[[0,7],4],[15,[0,13]]],[1,1]]"
    split_sample_2 = "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"
    assert split(split_sample_1) == "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"
    assert split(split_sample_2) == "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"

    reduce_sample_1 = "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"
    assert reduce(reduce_sample_1) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"

    add_sample1 = "[[[[4,3],4],4],[7,[[8,4],9]]]"
    add_sample2 = "[1,1]"
    assert add_single(add_sample1, add_sample2) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"

    # larger example
    add_sample1 = "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]"
    add_sample2 = "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]"
    assert (
        add_single(add_sample1, add_sample2)
        == "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]"
    )

    add_sample1 = "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]"
    add_sample2 = "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]"
    assert (
        add_single(add_sample1, add_sample2)
        == "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]"
    )

    add_sample1 = "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]"
    add_sample2 = "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]"
    assert (
        add_single(add_sample1, add_sample2)
        == "[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]"
    )

    full_sample_1 = read_file("data/day_18/sample1.txt")
    assert add(full_sample_1) == "[[[[5,0],[7,4]],[5,5]],[6,6]]"

    full_sample_2 = read_file("data/day_18/sample2.txt")
    assert add(full_sample_2) == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"

    assert compute_magnitude("[[1,2],[[3,4],5]]") == 143
    assert compute_magnitude("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]") == 1384
    assert compute_magnitude("[[[[1,1],[2,2]],[3,3]],[4,4]]") == 445
    assert compute_magnitude("[[[[3,0],[5,3]],[4,4]],[5,5]]") == 791
    assert compute_magnitude("[[[[5,0],[7,4]],[5,5]],[6,6]]") == 1137
    assert (
        compute_magnitude("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")
        == 3488
    )

    full_sample_3 = read_file("data/day_18/sample3.txt")
    assert compute_magnitude(add(full_sample_3)) == 4140

    real_input = read_file("data/day_18/input.txt")
    assert compute_magnitude(add(real_input)) == 4137

    # Part 2
    assert get_max_magnitude(full_sample_3) == 3993
    assert get_max_magnitude(real_input) == 4573
