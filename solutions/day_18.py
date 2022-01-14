from utils import read_file


def parse_input(input_path: str):
    return [line.strip() for line in read_file(input_path)]


def explode(
    snailfish_str,
    last_reg_idx=None,
    last_reg_value=None,
    next_reg_idx=None,
    next_reg_value=None,
    nesting=0
):
    """Apply single explode action."""
    snailfish_list = snailfish_str_to_list(snailfish_str)

    for idx, char in enumerate(snailfish_list):
        if char == "[":
            nesting += 1
        elif char == "]":
            nesting -= 1
        elif isinstance(char, int):
            last_reg_value, last_reg_idx = char, idx

        if nesting == 5:
            try:
                left = int(snailfish_list[idx + 1])
                right = int(snailfish_list[idx + 3])

                if last_reg_value is not None:
                    last_reg_value += left

                # Find next reg
                for idx2, char2 in enumerate(snailfish_list[idx + 4 :]):
                    try:
                        next_reg_value = int(char2)
                        next_reg_idx = idx2 + idx
                        break
                    except ValueError:
                        continue

                if next_reg_value is not None:
                    next_reg_value += right

                result = snailfish_list[:idx] + ["0"] + snailfish_list[idx + 5 :]

                if last_reg_idx:
                    result[last_reg_idx] = last_reg_value
                if next_reg_idx:
                    result[next_reg_idx] = next_reg_value

                return "".join(map(str, result))
            except ValueError:
                continue
    return snailfish_str


def snailfish_str_to_list(snailfish_str):
    snailfish_list = list(snailfish_str)
    new_list, int_stack = [], []

    for char in snailfish_list:
        if char in ["[", "]", ","]:
            if int_stack:
                new_int = int("".join(int_stack))
                new_list.append(new_int)
                int_stack = []
            new_list.append(char)
        elif char in [str(i) for i in range(10)]:
            int_stack.append(char)

    return new_list


def split(snailfish_str):
    """Apply single split action."""
    snailfish_list = snailfish_str_to_list(snailfish_str)
    for idx, char in enumerate(snailfish_list):
        try:
            reg_value = int(char)
            if reg_value >= 10:
                left = reg_value // 2
                right = left if reg_value % 2 == 0 else left + 1
                new_pair = [left, right]
                snailfish_list[idx] = new_pair
                return "".join(map(str, snailfish_list)).replace(" ", "")
        except ValueError:
            continue
    return snailfish_str


def reduce(snailfish_str, change=True):
    while change:
        snailfish_start = snailfish_str
        snailfish_str = explode(snailfish_str)
        if snailfish_start != snailfish_str:
            continue

        snailfish_str = split(snailfish_str)
        change = snailfish_start != snailfish_str

    return snailfish_str


def add_single(snailfish_str1, snailfish_str2):
    snailfish_str = f"[{snailfish_str1},{snailfish_str2}]"
    return reduce(snailfish_str)


def add(nrs):
    snailfish_nr1 = nrs[0]
    for idx, snailfish_nr2 in enumerate(nrs):
        if idx > 0:
            snailfish_nr1 = add_single(snailfish_nr1, snailfish_nr2)
    return reduce(snailfish_nr1)


def compute_magnitude(snailfish):
    if isinstance(snailfish, str):
        snailfish = eval(snailfish)
    if isinstance(snailfish, int):
        return snailfish
    else:
        return 3 * compute_magnitude(snailfish[0]) + 2 * compute_magnitude(snailfish[1])


def solve_1(input_list):
    return compute_magnitude(add(input_list))


def solve_2(snailfishnrs):
    """Compute max magnitude"""
    sums = []
    for idx, snailfishnr in enumerate(snailfishnrs):
        for idx2, snailfishnr2 in enumerate(snailfishnrs):
            if idx != idx2:
                sum = add_single(snailfishnr, snailfishnr2)
                sums.append(compute_magnitude(sum))
    return max(sums)


if __name__ == "__main__":
    sample1_input = parse_input("data/day_18/sample1.txt")
    sample2_input = parse_input("data/day_18/sample2.txt")
    sample3_input = parse_input("data/day_18/sample3.txt")
    real_input = parse_input("data/day_18/input.txt")

    # Part 1
    assert solve_1(sample3_input) == 4140
    assert solve_1(real_input) == 4137

    # Part 2
    assert solve_2(sample3_input) == 3993
    assert solve_2(real_input) == 4573
