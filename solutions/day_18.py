from utils import read_file


def parse_input(input_path: str):
    return [line.strip() for line in read_file(input_path)]


def explode(
    snailfish_str,
    last_reg_idx=None,
    last_reg_value=None,
    next_reg_idx=None,
    next_reg_value=None,
    nesting=0,
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

        if nesting == 5 and all(
            isinstance(snailfish_list[char_idx], int) for char_idx in [idx + 1, idx + 3]
        ):
            if last_reg_value is not None:
                last_reg_value += snailfish_list[idx + 1]

            # Find next reg
            for idx2, char2 in enumerate(snailfish_list[idx + 4 :]):
                if isinstance(char2, int):
                    next_reg_value, next_reg_idx = char2, idx + idx2
                    break

            if next_reg_value is not None:
                next_reg_value += snailfish_list[idx + 3]

            result = snailfish_list[:idx] + ["0"] + snailfish_list[idx + 5 :]

            if last_reg_idx:
                result[last_reg_idx] = last_reg_value
            if next_reg_idx:
                result[next_reg_idx] = next_reg_value
            return "".join(map(str, result))

    return snailfish_str


def snailfish_str_to_list(snailfish_str):
    """Convert snailfish number string to list."""
    snailfish_list = list(snailfish_str)
    new_list, int_stack = [], []

    for char in snailfish_list:
        if char in ["[", "]", ","]:
            if int_stack:
                new_list.append(int("".join(int_stack)))
                int_stack = []
            new_list.append(char)
        elif char in [str(i) for i in range(10)]:
            int_stack.append(char)
    return new_list


def split(snailfish_str):
    """Apply single split action."""
    snailfish_list = snailfish_str_to_list(snailfish_str)
    for idx, char in enumerate(snailfish_list):
        if isinstance(char, int) and char >= 10:
            left = char // 2
            right = left if char % 2 == 0 else left + 1
            snailfish_list[idx] = [left, right]
            return "".join(map(str, snailfish_list)).replace(" ", "")
    return snailfish_str


def reduce(snailfish_str, change=True):
    """Reduce full snailfish string by iteratively applying explode and split actions."""
    while change:
        snailfish_start = snailfish_str
        snailfish_str = explode(snailfish_str)
        if snailfish_start != snailfish_str:
            continue
        snailfish_str = split(snailfish_str)
        change = snailfish_start != snailfish_str
    return snailfish_str


def add_single(snailfish_str1, snailfish_str2):
    """Add two single snailfish numbers."""
    snailfish_str = f"[{snailfish_str1},{snailfish_str2}]"
    return reduce(snailfish_str)


def add(nrs):
    """Compute the sum of a list of snailfish numbers."""
    snailfish_nr1 = nrs[0]
    for idx, snailfish_nr2 in enumerate(nrs[1:]):
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


def solve_2(snailfish_nrs, max_mag=0):
    """Compute max magnitude"""
    for idx, snailfishnr in enumerate(snailfish_nrs):
        for idx2, snailfishnr2 in enumerate(snailfish_nrs):
            if idx != idx2:
                mag = compute_magnitude(add_single(snailfishnr, snailfishnr2))
                if mag > max_mag:
                    max_mag = mag
    return max_mag


if __name__ == "__main__":
    sample1_input = parse_input("data/day_18/sample1.txt")
    sample2_input = parse_input("data/day_18/sample2.txt")
    sample3_input = parse_input("data/day_18/sample3.txt")
    real_input = parse_input("data/day_18/input.txt")

    # Samples
    assert explode("[[[[[9,8],1],2],3],4]") == "[[[[0,9],2],3],4]"
    assert explode("[7,[6,[5,[4,[3,2]]]]]") == "[7,[6,[5,[7,0]]]]"
    assert explode("[[6,[5,[4,[3,2]]]],1]") == "[[6,[5,[7,0]]],3]"
    assert (
        explode("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
        == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
    )
    assert (
        explode("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]") == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"
    )
    assert (
        explode("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]")
        == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    )

    assert (
        split("[[[[0,7],4],[15,[0,13]]],[1,1]]") == "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"
    )
    assert (
        split("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")
        == "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"
    )

    assert (
        reduce("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
        == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    )

    assert (
        add_single("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]")
        == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    )
    assert (
        add_single(
            "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
            "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
        )
        == "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]"
    )
    assert (
        add_single(
            "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]",
            "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
        )
        == "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]"
    )
    assert (
        add_single(
            "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]",
            "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
        )
        == "[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]"
    )

    assert add(sample1_input) == "[[[[5,0],[7,4]],[5,5]],[6,6]]"
    assert add(sample2_input) == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"

    assert compute_magnitude("[[1,2],[[3,4],5]]") == 143
    assert compute_magnitude("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]") == 1384
    assert compute_magnitude("[[[[1,1],[2,2]],[3,3]],[4,4]]") == 445
    assert compute_magnitude("[[[[3,0],[5,3]],[4,4]],[5,5]]") == 791
    assert compute_magnitude("[[[[5,0],[7,4]],[5,5]],[6,6]]") == 1137
    assert (
        compute_magnitude("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")
        == 3488
    )

    # Part 1
    assert solve_1(sample3_input) == 4140
    assert solve_1(real_input) == 4137

    # Part 2
    assert solve_2(sample3_input) == 3993
    assert solve_2(real_input) == 4573
