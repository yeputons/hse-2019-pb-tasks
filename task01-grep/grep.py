#!/usr/bin/env python3
from typing import List, IO
import sys
import re
import argparse


def process_lines(source: IO[str], pattern: str, is_c: bool) -> List[str]:
    matching_lines = []
    for line in source.readlines():
        line = line.rstrip('\n')
        if re.search(pattern, line):
            matching_lines.append(line)
    if is_c:
        matching_lines = [str(len(matching_lines))]
    return matching_lines


def print_lines(lines: List[str]) -> None:
    for i in range(len(lines)):
        print(lines[i])


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    args = parser.parse_args(args_str)

    needle = args.needle if args.regex else re.escape(args.needle)
    flag_c = args.count

    if args.files:
        if len(args.files) == 1:
            for filename in args.files:
                with open(filename, 'r') as file:
                    lines = process_lines(file, needle, flag_c)
                    print_lines(lines)
        else:
            for filename in args.files:
                with open(filename, 'r') as file:
                    lines = process_lines(file, needle, flag_c)
                    lines = [f'{filename}:{line}' for line in lines]
                    print_lines(lines)
    else:
        lines = process_lines(sys.stdin, needle, flag_c)
        print_lines(lines)


if __name__ == '__main__':
    main(sys.argv[1:])
