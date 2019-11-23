#!/usr/bin/env python3
from typing import List
import random

ITERS = 1000
FLIPS = 100


def get_max_run(flips: List[str]) -> int:
    max_run = 0
    cur_run = 0
    for flip in flips:
        if flip:
            cur_run += 1
        else:
            cur_run = 0
        max_run = max(max_run, cur_run)
    return max_run


def main():
    random.seed(123456)
    s = 0
    total = 0
    for _ in range(ITERS):
        total += 1
        flips = [random.choice([0, 1]) for _ in range(FLIPS)]
        s += get_max_run(flips)
    print(s, total, s / total)


if __name__ == '__main__':
    main()
