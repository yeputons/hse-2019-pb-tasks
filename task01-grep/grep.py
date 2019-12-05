#!/usr/bin/env python3
from typing import List, Pattern, Iterable, Any
import sys
import argparse
import re


def filter_matching_lines(pattern: Pattern, lines: List[str]) -> List[str]:
    return [line for line in lines if re.search(pattern, line)]


def print_lines(lines: Iterable) -> None:
    for line in lines:
        print(line)


def build_pattern(string: str, is_regex: bool) -> Pattern:
    if not is_regex:
        string = re.escape(string)
    return re.compile(string)


def rstrip_lines(lines: List[str], chars='\n') -> List[str]:
    return [line.rstrip(chars) for line in lines]


def count_lines(line_sets: List[List[Any]]) -> List[int]:
    return [len(lines) for lines in line_sets]


def add_prefix(prefix: str, lines: Iterable, chars_between='') -> List[str]:
    return list(map(lambda x: '{}{}{}'.format(prefix, chars_between, x), lines))


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    args = parser.parse_args(args_str)

    pattern = build_pattern(args.needle, args.regex)

    result = []

    for file_name in args.files:
        with open(file_name, 'r') as file:
            result.append(file.readlines())

    if not args.files:
        result.append(sys.stdin.readlines())

    result = list(map(
        lambda lines: filter_matching_lines(pattern, rstrip_lines(lines)),
        result
    ))

    if args.count:
        result = [[str(x)] for x in count_lines(result)]

    if len(args.files) > 1:
        for i, file_name in enumerate(args.files):
            result[i] = add_prefix(file_name, result[i], chars_between=':')

    for lines in result:
        print_lines(lines)


if __name__ == '__main__':
    main(sys.argv[1:])
