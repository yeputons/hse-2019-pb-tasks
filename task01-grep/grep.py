#!/usr/bin/env python3
import argparse
import re
import sys
from typing import List


def parse_args(args_str: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('string', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    args = parser.parse_args(args_str)
    return args


def print_file(print_filenames, flag_c, prefix, lines: List[str]) -> None:
    if not print_filenames:
        prefix = ''
    if flag_c:
        print(f'{prefix}{len(lines)}')
    else:
        for lin in lines:
            print(f'{prefix}{lin}')


def print_stdio(flag_c, lines: List[str]) -> None:
    if flag_c:
        print(len(lines))
    else:
        for lin in lines:
            print(lin)


def search_append(string, line, lines: List[str]) -> None:
    line = line.rstrip('\n')
    if re.search(string, line):
        lines.append(line)


def search_right_string(string: str, place_of_search, lines: List[str]) -> None:
    for line in place_of_search:
        search_append(string, line, lines)


def main(args_str: List[str]) -> None:
    args = parse_args(args_str)
    string = args.string if args.regex else args.string
    lines: List[str] = []

    if args.files:
        print_filenames: bool = len(args.files) > 1
        for file in args.files:
            with open(file, 'r') as in_file:
                search_right_string(string, in_file, lines)
                print_file(print_filenames, args.count, file + ':', lines)
                lines = []

    else:
        search_right_string(string, sys.stdin, lines)
        print_stdio(args.count, lines)


if __name__ == '__main__':
    main(sys.argv[1:])
