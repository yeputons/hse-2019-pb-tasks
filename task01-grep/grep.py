#!/usr/bin/env python3
from typing import List, Pattern, Union, Iterable, Any
import sys
import argparse
import re


def filter_matching_lines(pattern: Union[Pattern, str], lines: List[str]) -> List[str]:
    return [line for line in lines if re.search(pattern, line)]


def print_lines(lines: Iterable) -> None:
    for line in lines:
        print(line)


def build_pattern(string: str, is_regex: bool) -> Union[Pattern, str]:
    if is_regex:
        return re.compile(string)
    return re.escape(string)


def rstrip_lines(lines: List[str], chars: str) -> List[str]:
    return [line.rstrip(chars) for line in lines]


def count_lines(line_sets: List[List[Any]]) -> List[List[str]]:
    return [[str(len(lines))] for lines in line_sets]


def add_prefix(prefix: str, lines: List[str], chars_between='') -> List[str]:
    return list(map(lambda x: prefix + chars_between + x, lines))


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
            result.append(filter_matching_lines(pattern, rstrip_lines(file.readlines(), '\n')))

    if not args.files:
        result.append(filter_matching_lines(pattern, rstrip_lines(sys.stdin.readlines(), '\n')))

    if args.count:
        result = count_lines(result)

    if len(args.files) > 1:
        for i in range(len(args.files)):
            result[i] = add_prefix(args.files[i], result[i], chars_between=':')

    for lines in result:
        print_lines(lines)


if __name__ == '__main__':
    main(sys.argv[1:])
