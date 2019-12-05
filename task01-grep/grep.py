#!/usr/bin/env python3
from typing import List, Pattern, Iterable, Any
import sys
import argparse
import re


def filter_matching_lines(pattern: Pattern, lines: Iterable[str]) -> List[str]:
    return [line for line in lines if re.search(pattern, line)]


def print_lines(lines: Iterable[str]) -> None:
    for line in lines:
        print(line)


def build_pattern(string: str, is_regex=False, is_ignore_case=False, is_full_match=False) \
                                                                                        -> Pattern:
    ignore_case = re.IGNORECASE if is_ignore_case else 0
    if not is_regex:
        string = re.escape(string)
    if is_full_match:
        string = '^{}$'.format(string)
    return re.compile(string, flags=ignore_case)


def rstrip_lines(lines: Iterable[str], chars='\n') -> List[str]:
    return [line.rstrip(chars) for line in lines]


def count_lines(line_sets: Iterable[List[Any]]) -> List[int]:
    return [len(lines) for lines in line_sets]


def add_prefix(prefix: str, lines: Iterable, chars_between='') -> List[str]:
    return ['{}{}{}'.format(prefix, chars_between, line) for line in lines]


def get_difference(set_a: List[Any], set_b: List[Any]) -> List[Any]:
    # A\B
    for item in set_b:
        if item in set_a:
            set_a.remove(item)
    return set_a


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument('-l', dest='files_with_matches', action='store_true')
    format_group.add_argument('-L', dest='files_without_match', action='store_true')
    format_group.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-i', dest='ignore_case', action='store_true')
    parser.add_argument('-x', dest='line_regex', action='store_true')
    parser.add_argument('-v', dest='invert_match', action='store_true')
    args = parser.parse_args(args_str)

    pattern = build_pattern(args.needle, args.regex, args.ignore_case, args.line_regex)

    result = []

    for file_name in args.files:
        with open(file_name, 'r') as file:
            result.append(rstrip_lines(file.readlines()))

    if not args.files:
        result.append(rstrip_lines(sys.stdin.readlines()))

    temp_result = [filter_matching_lines(pattern, lines) for lines in result]

    # Flag: -v

    if args.invert_match:
        for i, matches in enumerate(temp_result):
            result[i] = get_difference(result[i], matches)
    else:
        result = temp_result

    # Flag: -c

    if args.count:
        result = [[str(x)] for x in count_lines(result)]

    # Flag: -l and -L

    output_only_files = args.files_with_matches or args.files_without_match

    if output_only_files:
        for i, file_name in enumerate(args.files):
            result[i] = [file_name] if result[i] else []

    if args.files_without_match:
        for i, file_name in enumerate(args.files):
            result[i] = get_difference([file_name], result[i])

    if len(args.files) > 1 and not output_only_files:
        for i, file_name in enumerate(args.files):
            result[i] = add_prefix(file_name, result[i], chars_between=':')

    for lines in result:
        print_lines(lines)


if __name__ == '__main__':
    main(sys.argv[1:])
