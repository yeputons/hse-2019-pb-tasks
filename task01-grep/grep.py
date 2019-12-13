#!/usr/bin/env python3
import argparse
import re
import sys
from typing import List, IO


def parse_args(args_str: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('string', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    return parser.parse_args(args_str)


def print_file(print_filenames: bool, count: bool, prefix: str, lines: List[str]) -> None:
    if not print_filenames:
        prefix = ''
    if count:
        print(f'{prefix}{len(lines)}')
    else:
        for line in lines:
            print(f'{prefix}{line}')


def print_stdio(count: int, lines: List[str]) -> None:
    if count:
        print(len(lines))
    else:
        for lin in lines:
            print(lin)


def search_append(string: str, line: str, lines: List[str]) -> None:
    line = line.rstrip('\n')
    if re.search(string, line):
        lines.append(line)


def search_right_string_file(string: str, file: IO[str], lines: List[str]) -> None:
    for line in file:
        search_append(string, line, lines)


def search_right_string_stdin(string: str, lines: List[str]) -> None:
    for line in sys.stdin:
        search_append(string, line, lines)


def main(args_str: List[str]) -> None:
    args = parse_args(args_str)
    string = args.string if args.regex else re.escape(args.string)
    lines: List[str] = []

    if args.files:
        print_filenames: bool = len(args.files) > 1
        for file in args.files:
            with open(file, 'r') as in_file:
                search_right_string_file(string, in_file, lines)
                print_file(print_filenames, args.count, file + ':', lines)
                lines = []

    else:
        search_right_string_stdin(string, lines)
        print_stdio(args.count, lines)


if __name__ == '__main__':
    main(sys.argv[1:])
