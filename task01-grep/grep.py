#!/usr/bin/env python3
from typing import List
from typing import Tuple
import sys
import re
import argparse


def find(line: str, needle: str, regex: bool) -> bool:
    result = re.search(needle, line) if regex else needle in line
    return True if result else False


def get_lines_with_needle(lines: List[str], needle: str, regex: bool) -> List[str]:
    lines_with_needle = []
    for line in lines:
        if find(line, needle, regex):
            lines_with_needle.append(line)
    return lines_with_needle


def print_lines(files_and_lines: List[Tuple[str, List[str]]], format_str: str, count: bool):
    for file, lines in files_and_lines:
        if count:
            print(format_str.format(file, len(lines)))
        else:
            for line in lines:
                print(format_str.format(file, line))


def read_from_stdin() -> List[str]:
    lines = []
    for line in sys.stdin.readlines():
        lines.append(line.rstrip('\n'))
    return lines


def read_from_file(file_name: str) -> List[str]:
    lines = []
    with open(file_name, 'r') as in_file:
        for line in in_file.readlines():
            lines.append(line.rstrip('\n'))
    return lines


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    args = parser.parse_args(args_str)

    format_str = '{}:{}' if len(args.files) > 1 else '{}{}'
    files_and_lines_with_needle = []
    if args.files:
        for file_name in args.files:
            lines = read_from_file(file_name)
            lines_with_needle = get_lines_with_needle(lines, args.needle, args.regex)
            files_and_lines_with_needle.append(
                (file_name if len(args.files) > 1 else '', lines_with_needle))
    else:
        lines = read_from_stdin()
        lines_with_needle = get_lines_with_needle(lines, args.needle, args.regex)
        files_and_lines_with_needle.append(('', lines_with_needle))

    print_lines(files_and_lines_with_needle, format_str, args.count)


if __name__ == '__main__':
    main(sys.argv[1:])
