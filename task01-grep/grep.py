#!/usr/bin/env python3
from typing import List, Pattern
import sys
import re
import argparse


def parse(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count_format', action='store_true')
    return parser.parse_args(args_str)


def read_from_file(filename: str):
    with open(filename, 'r') as file:
        return [line for line in file.readlines()]


def find_matching_lines(lines: List[str], pattern: str, regex: bool):
    def match(line: str, regular_expression: Pattern):
        return re.search(regular_expression, line)
    if not regex:
        pattern = re.escape(pattern)
    regular_expression = re.compile(pattern)
    matched = [line for line in lines if match(line, regular_expression)]
    return matched


def print_matched(matched: List[str], need_filenames: bool = False, filename: str = None):
    for line in matched:
        if need_filenames:
            print(filename, end=':')
        print(line)


def main(args_str: List[str]):
    args = parse(args_str)

    if args.files:
        for filename in args.files:
            input_lines = [line.strip('\n') for line in read_from_file(filename)]
            matched = find_matching_lines(input_lines, args.needle, args.regex)
            formatted = [str(len(matched))] if args.count_format else [line for line in matched]
            print_matched(formatted, len(args.files) > 1, filename)
    else:
        input_lines = [line.strip('\n') for line in sys.stdin.readlines()]
        matched = find_matching_lines(input_lines, args.needle, args.regex)
        formatted = [str(len(matched))] if args.count_format else [line for line in matched]
        print_matched(formatted)


if __name__ == '__main__':
    main(sys.argv[1:])
