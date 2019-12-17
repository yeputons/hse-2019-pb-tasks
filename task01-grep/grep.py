#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def parse_args(args_str: List[str]) -> argparse.Namespace:
    # Automatically recognises everything that is needed
    # Stores information into Namespace
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-l', dest='print_files', action='store_true')
    parser.add_argument('-L', dest='print_not_files', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-i', dest='ignore_case', action='store_true')
    parser.add_argument('-v', dest='invert', action='store_true')
    parser.add_argument('-x', dest='fullmatch', action='store_true')
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    return parser.parse_args(args_str)


def get_lines_from_file(filename: str) -> List[str]:
    # Turns contents of the file into separate lines
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.rstrip('\n'))
    return lines


def find_pattern_common(args: argparse.Namespace, line: str) -> bool:
    # Checks whether there is a match between given pattern and line
    # Applicable for common expressions
    if args.ignore_case:
        args.pattern = args.pattern.lower()
        line = line.lower()
    if args.fullmatch:
        return args.pattern == line
    return args.pattern in line


def find_pattern_regex(args: argparse.Namespace, line: str) -> bool:
    # Checks whether there is a match between given pattern and line
    # Applicable for regular expressions
    search = re.fullmatch if args.fullmatch else re.search
    if args.ignore_case:
        return search(args.pattern, line, re.IGNORECASE) is not None
    return re.search(args.pattern, line) is not None


def is_matching(args: argparse.Namespace, line: str) -> bool:
    # Desides whether to choose the line according to keys
    if args.regex and find_pattern_regex(args, line) != args.invert:
        return True
    if not args.regex and find_pattern_common(args, line) != args.invert:
        return True
    return False


def choose_format(args: argparse.Namespace) -> str:
    # Select an appropriate format for raw data
    if args.print_files or args.print_not_files:
        return '{0}'
    return '{0}:{1}' if len(args.files) > 1 else '{1}'


def print_output(lines: List[str], file_name: str, args: argparse.Namespace) -> None:
    chosen_lines = []
    for line in lines:
        if is_matching(args, line):
            chosen_lines.append(line)
    fmt = choose_format(args)
    if args.count:
        print(fmt.format(file_name, len(chosen_lines)))
    else:
        if args.print_not_files:
            if len(chosen_lines) == 0:
                print(fmt.format(file_name, ''))
        elif args.print_files and len(chosen_lines) > 0:
            print(fmt.format(file_name, ''))
        else:
            for line in chosen_lines:
                print(fmt.format(file_name, line))


def main(args_str: List[str]) -> None:
    args = parse_args(args_str)
    lines_to_check = []

    if args.files != []:
        for file in args.files:
            lines_to_check.append(get_lines_from_file(file))
    else:
        lines_to_check = [[line.rstrip('\n') for line in sys.stdin.readlines()]]
        args.files.append('')

    for lines, file_name in zip(lines_to_check, args.files):
        print_output(lines, file_name, args)


if __name__ == '__main__':
    main(sys.argv[1:])
