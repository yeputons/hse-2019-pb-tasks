#!/usr/bin/env python3
from functools import partial
from typing import List
from typing import Iterable
from typing import Pattern
from typing import Tuple
from typing import Callable

import sys
import re
import argparse


def parse_args(args_str: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-l', dest='name_file_only', action='store_true')
    parser.add_argument('-L', dest='invert_name_file_only', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-i', dest='ignore_case', action='store_true')
    parser.add_argument('-v', dest='invert', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    return parser.parse_args(args_str)


def strip_lines(file: Iterable) -> List[str]:
    return [line.rstrip('\n') for line in file]


def get_re_pattern(pattern: str, regex_flag: bool, ignore_case: bool) -> Pattern[str]:
    if not regex_flag:
        pattern = re.escape(pattern)
    _flags = re.I if ignore_case else 0
    return re.compile(pattern, flags=_flags)


def get_find_function(re_pattern: Pattern[str], full_match: bool, invert: bool) -> Callable[[str], bool]:
    find = re.fullmatch if full_match else re.search
    find = partial(find, pattern=re_pattern)
    return lambda line: bool(find(string=line)) ^ invert


def filter_lines_by_re(lines: List[str], find: Callable[[str], bool]) -> List[str]:
    return [line for line in lines if find(line)]


def filter_blocks(blocks: List[List[str]], find: Callable[[str], bool]) -> List[List[str]]:
    return [filter_lines_by_re(lines, find) for lines in blocks]


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

    re_pattern = get_re_pattern(args.pattern, args.regex, args.ignore_case)
    find = get_find_function(re_pattern, args.full_match, args.invert)
    blocks = filter_blocks(blocks, find)

    if args.count:
        blocks = map_blocks(blocks)

    if len(sources) > 1:
        blocks = list(map(add_filename_prefix_to_lines, zip(blocks, sources)))

    print_blocks(blocks)


if __name__ == '__main__':
    main(sys.argv[1:])
