#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def parse_args(args_str: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    return parser.parse_args(args_str)


def print_in_files(print_filenames: bool, file_name: str, line: str) -> None:
    if print_filenames:
        print(f'{file_name}:{line}')
    else:
        print(line)


def working_with_stdin(pattern: str, count: bool) -> None:
    counter = 0
    for line in sys.stdin.readlines():
        line = line.rstrip('\n')
        if re.search(pattern, line):
            if not count:
                print(line)
            counter += 1
    if count:
        print(counter)


def working_with_files(files: List[str], pattern: str, count: bool) -> None:
    for file_name in files:
        counter = 0
        with open(file_name, 'r') as file:
            for line in file.readlines():
                line = line.rstrip('\n')
                if re.search(pattern, line):
                    if not count:
                        print_in_files(len(files) > 1, file_name, line)
                    counter += 1
            if count:
                print_in_files(len(files) > 1, file_name, str(counter))


def main(args_str: List[str]) -> None:
    args = parse_args(args_str)
    if args.regex:
        pattern = args.pattern
    else:
        pattern = re.escape(args.pattern)
    if args.files:
        working_with_files(args.files, pattern, args.count)
    else:
        working_with_stdin(pattern, args.count)


if __name__ == '__main__':
    main(sys.argv[1:])

