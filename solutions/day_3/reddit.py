from functools import reduce
import os

input_path = "data/day_1/input.txt"
input_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "..", "..", input_path
)
N = [[map(int, l.strip())] for l in open(input_path)]

a, b, c, d = [
    reduce(
        lambda x, y: 2 * x + y,
        reduce(
            lambda x, y: x + [t([l[y] for l in N if x == l[: len(x)] or m])],
            range(len(N[0])),
            [],
        ),
    )
    for t in (
        lambda x: sum(x) >= (len(x) / 2),
        lambda x: (0 < (2 * sum(x)) < len(x)) or all(x),
    )
    for m in [0,1]
]

print(b * d, a * c)
