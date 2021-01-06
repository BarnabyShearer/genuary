#!/usr/bin/env python3
# https://genuary2021.github.io/prompts

import itertools


class Infix:
    def __init__(self, f):
        self.f = f

    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.f(other, x))

    def __or__(self, other):
        return self.f(other)


# // TRIPLE NESTED LOOP
for t, y, x in itertools.product(range(2, 64, 4), range(8), range(10)):
    # Rule 30 (elementary cellular automaton)
    if not x:
        p = (n if y else t) << 1
        n = 0
    if 30 & 1 << (p >> (10 - x) & 7):
        n |= 1 << (10 - x)
    print("#" if x and n & 1 << (10 - x) else " ", end="" if 9 - x else "\n")

# Make something human.
try:
    raise Exception("human")
except Exception as e:
    print(f"err is {e}")

# Small areas of symmetry.
p = Infix(lambda a, b: print(f"{a}p{b}"))

"aiboh" | p | "hobia"

# Do some code golf! How little code can you write to make something interesting? Share the sketch and its code together if you can.
def golf(x):
    return (
        {"s": "i", "o": "n", "m": "t", "e": "ere", "t": "s", "h": "t"}.get(l, l)
        for l in x
    )


print("".join(golf("something")))
