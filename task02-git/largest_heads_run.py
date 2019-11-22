#!/usr/bin/env python3
from typing import List
import random


def get_max_run(flips: List[int]) -> int:
    cur_run = 0
    max_run = 0
    for flip in flips:
        if flip:
            cur_run += 1
        else:
            cur_run = 0
        max_run = max(max_run, cur_run)
    return max_run


ITERS = 1000
FLIPS = 100


def main():
    random.seed(123456)
    s = 0
    total = 0
    for _ in range(ITERS):
        total += 1
        max_run = get_max_run([random.choice([0, 1]) for _ in range(FLIPS)])
        s += max_run
    print(s, total, s / total)


if __name__ == '__main__':
    main()
