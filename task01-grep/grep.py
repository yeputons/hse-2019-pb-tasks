#!/usr/bin/env python3
from typing import List
from typing import TextIO
import sys
import re
import argparse


def format_lines(filename: str, needle: str, input_type: TextIO,
                 count: bool, add_filenames: bool) -> None:
    lines_without_line_break = [
        line.rstrip('\n') for line in input_type]
    matching_lines = [
        line for line in lines_without_line_break if re.search(
            needle, line)]
    files_output(filename, matching_lines, count, add_filenames)


def files_output(filename: str, matching_lines: list,
                 count: bool, add_filenames: bool) -> list:
    lines = [str(len(matching_lines))] if count else matching_lines
    if add_filenames:
        for line in lines:
            print(f'{filename}:{line}')
    else:
        for line in lines:
            print(f'{line}')
    return lines


def main(args_str: List[str]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    args = parser.parse_args(args_str)

    # STUB BEGINS
    needle = args.needle if args.regex else re.escape(args.needle)
    add_filenames = len(args.files) > 1
    if args.files:
        for filename in args.files:
            with open(filename, 'r') as in_file:
                format_lines(
                    filename, needle, in_file, args.count, add_filenames)
    else:
        format_lines('', needle, sys.stdin, args.count, add_filenames)


if __name__ == '__main__':
    main(sys.argv[1:])
