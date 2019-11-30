#!/usr/bin/env python3
from typing import List, Iterable, Pattern
import sys
import re
import argparse as ap


def parse_args(args_str: List[str]) -> ap.Namespace:
    parser = ap.ArgumentParser()
    parser.add_argument('-c', dest='count', action='store_true', help='count matches')
    parser.add_argument('-E', dest='regex', action='store_true',
                        help='given string is understood as regex')
    parser.add_argument('pattern', type=str, help='first string after flags')
    parser.add_argument('file_names', nargs='*',
                        help='arguments after pattern are files names')
    return parser.parse_args(args_str)


def match_lines(pattern: Pattern[str], data: List[str]) -> List[str]:
    return [line for line in data if re.search(pattern, line)]


def strip_lines(lines: Iterable) -> List[str]:
    return [line.rstrip('\n') for line in lines]


def compile_pattern(pattern: str, is_regex: bool) -> Pattern:
    if not is_regex:
        pattern = re.escape(pattern)
    return re.compile(pattern)


def format_data(data: List[str], counting_mode: bool, source_name: str = None) -> List[str]:
    if counting_mode:
        data = [str(len(data))]
    if source_name:
        return ['{}:{}'.format(source_name, line) for line in data]
    else:
        return data


def find_in_source(source: Iterable, pattern: Pattern[str],
                   counting_mode: bool, source_name: str = None) -> List[str]:
    result: List[str] = match_lines(pattern, strip_lines(source))
    return format_data(result, counting_mode, source_name)


def main(args_str: List[str]):
    args: ap.Namespace = parse_args(args_str)
    result: List[str] = []
    pattern: Pattern[str] = compile_pattern(args.pattern, args.regex)
    if args.file_names:
        for file_name in args.file_names:
            with open(file_name, 'r') as file:
                result += find_in_source(file, pattern, args.count,
                                         file_name if len(args.file_names) > 1 else None)
    else:
        result = find_in_source(sys.stdin, pattern, args.count)
    print(*result, sep='\n')


if __name__ == '__main__':
    main(sys.argv[1:])
