from utils import read_file


def parse_input(input_path: str):
    return [line.strip() for line in read_file(input_path)]


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
    sample1_input = parse_input("data/day_18/sample1.txt")
    sample2_input = parse_input("data/day_18/sample2.txt")
    sample3_input = parse_input("data/day_18/sample3.txt")
    real_input = parse_input("data/day_18/input.txt")

    full_sample_3 = parse_input("data/day_18/sample3.txt")
    assert compute_magnitude(add(full_sample_3)) == 4140

    real_input = parse_input("data/day_18/input.txt")
    assert compute_magnitude(add(real_input)) == 4137

    # Part 2
    assert get_max_magnitude(full_sample_3) == 3993
    assert get_max_magnitude(real_input) == 4573
