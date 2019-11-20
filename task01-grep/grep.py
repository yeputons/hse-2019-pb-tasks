#!/usr/bin/env python3
from typing import List, Iterable
import sys
import re
import argparse as ap


def parse_args(args_str: List[str]) -> ap.Namespace:
    parser = ap.ArgumentParser()
    parser.add_argument('-c', dest='count', action='store_true', help='count matches')
    parser.add_argument('-E', dest='regex', action='store_true',
                        help='given string is understood as regex')
    parser.add_argument('pattern', type=str, help='first string after flags')
    parser.add_argument('files', nargs='*',
                        help='arguments after pattern are files names')
    return parser.parse_args(args_str)


def pattern_in_line(pattern: str, line: str, is_regex: bool) -> bool:
    return (is_regex and re.search(pattern, line) is not None) or (not is_regex and pattern in line)


def find_matches(pattern: str, data: List[str], is_regex: bool) -> List[str]:
    return [line for line in data if pattern_in_line(pattern, line, is_regex)]


def strip_lines(file: Iterable) -> List[str]:
    return [line.rstrip('\n') for line in file]


def format_data(data: List[str], counting_mode: bool, sourcename: str = None) -> List[str]:
    if counting_mode:
        data = [str(len(data))]
    return ['{}:{}'.format(sourcename, line) for line in data] if sourcename else data


def find_in_file(source: Iterable, pattern: str, is_regex: bool,
                 counting_mode: bool, sourcename: str = None) -> List[str]:
    result: List[str] = find_matches(pattern, strip_lines(source), is_regex)
    return format_data(result, counting_mode, sourcename)


def main(args_str: List[str]):
    args = parse_args(args_str)
    result: List[str] = []
    if args.files:
        for file in args.files:
            try:
                with open(file) as f:
                    result += find_in_file(f, args.pattern, args.regex,
                                           args.count, file if len(args.files) > 1 else None)
                    f.close()
            except IOError as e:
                print(e)

    else:
        result = find_in_file(sys.stdin, args.pattern, args.regex, args.count)
    print(*result, sep='\n')


if __name__ == '__main__':
    main(sys.argv[1:])
