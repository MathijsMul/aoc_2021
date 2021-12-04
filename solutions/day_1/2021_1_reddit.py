import fileinput
import os

current_path = os.path.abspath(os.path.dirname(__file__))
input_path = os.path.join(current_path, "..", "..", "data/day_1/input.txt")

nums = [int(x) for x in fileinput.input(files=(input_path))]


def solve(*arrs):
    zipped = list(zip(*arrs))
    return sum(map(lambda x: sum(x[1]) > sum(x[0]), zip(zipped, zipped[1:])))


p1 = solve(nums)
p2 = solve(nums, nums[1:], nums[2:])
print(p1, p2)

assert p1 == 1167
assert p2 == 1130
