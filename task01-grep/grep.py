#!/usr/bin/env python3
from typing import List
from collections.abc import Iterable
import sys
import re
import argparse as ap


def parse_args(args_str: List[str]) -> ap.Namespace:
    parser = ap.ArgumentParser()
    parser.add_argument('-c', dest='count', action='store_true', help='count matches')
    parser.add_argument('-E', dest='regex', action='store_true',
                        help='given string is understood as regex')
    parser.add_argument('pattern', type=str, help='first string after flags')
    parser.add_argument('files', nargs='*', type=ap.FileType('r'),
                        help='arguments after pattern are files names')
    return parser.parse_args(args_str)


def find_matches(pattern: str, data: List[str], is_regex: bool) -> List[str]:
    return [line for line in data if (is_regex and re.search(pattern, line))
            or (not is_regex and pattern in line)]


def strip_lines(file: Iterable) -> List[str]:
    return [line.rstrip('\n') for line in file]


def format_data(data: List[str], is_count: bool, multiple_files: bool, filename: str) -> List[str]:
    if is_count:
        data = [str(len(data))]
    return [filename + ': ' + line for line in data] if multiple_files else data


def find_in_file(file: Iterable, name: str, pattern: str, is_regex: bool,
                 is_count: bool, multiple_files: bool) -> List[str]:
    result: List[str] = find_matches(pattern, strip_lines(file), is_regex)
    return format_data(result, is_count, multiple_files, name)


def main(args_str: List[str]):
    args = parse_args(args_str)
    result: List[str] = []
    if args.files:
        for file in args.files:
            result += find_in_file(file, file.name, args.pattern,
                                   args.regex, args.count, len(args.files) > 1)
    else:
        result = find_in_file(sys.stdin, '', args.pattern, args.regex, args.count, False)
    print(*result, sep='\n')


if __name__ == '__main__':
    main(sys.argv[1:])
