from random import randint, seed
from typing import Any


def shuffle_list(input: list[Any], steps: int = -1, rnd_seed: int = 1) -> list[Any]:
    if steps == -1:
        steps = len(input) * 3

    seed(rnd_seed)
    r = input.copy()
    for _ in range(steps):
        left = randint(0, len(input) - 1)
        right = randint(0, len(input) - 1)

        if left != right:
            r[left], r[right] = r[right], r[left]

    return r
