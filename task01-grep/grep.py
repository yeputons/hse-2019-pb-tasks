#!/usr/bin/env python3
from typing import List
from typing import Iterable
from typing import Pattern
from typing import Tuple

import sys
import re
import argparse


def parse_args(args_str: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    return parser.parse_args(args_str)


def strip_lines(file: Iterable) -> List[str]:
    return [line.rstrip('\n') for line in file]


def get_re_pattern(pattern: str, regex_flag: bool) -> Pattern[str]:
    if not regex_flag:
        pattern = re.escape(pattern)
    return re.compile(pattern)


def filter_lines_by_re(lines: List[str], re_pattern: Pattern[str]) -> List[str]:
    return [line for line in lines if re.search(re_pattern, line)]


def filter_blocks(blocks: List[List[str]], re_pattern: Pattern[str]) -> List[List[str]]:
    return [filter_lines_by_re(lines, re_pattern) for lines in blocks]


def map_blocks(blocks: List[List[str]]) -> List[List[str]]:
    return [[str(len(lines))] for lines in blocks]


def add_filename_prefix_to_lines(lines_source_tuple: Tuple[List[str], str]) -> List[str]:
    lines, source = lines_source_tuple
    return [f'{source}:{line}' for line in lines]


def print_blocks(blocks: list):
    for lines in blocks:
        for line in lines:
            print(line)


def main(args_str: List[str]):
    args = parse_args(args_str)

    blocks = []
    for file_name in args.files:
        with open(file_name, 'r') as file:
            blocks.append(strip_lines(file))
    if not args.files:
        blocks.append(strip_lines(sys.stdin))

    sources = args.files
    if not sources:
        sources = ['_stdin_']

    re_pattern = get_re_pattern(args.pattern, args.regex)
    blocks = filter_blocks(blocks, re_pattern)

    if args.count:
        blocks = map_blocks(blocks)

    if len(sources) > 1:
        blocks = list(map(add_filename_prefix_to_lines, zip(blocks, sources)))

    print_blocks(blocks)


if __name__ == '__main__':
    main(sys.argv[1:])
