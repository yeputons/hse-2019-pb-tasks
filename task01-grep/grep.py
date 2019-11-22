#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def parse_args(args_str) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    return parser.parse_args(args_str)


def print_in_files(amount: bool, file_name: str, line: str) -> None:
    if amount:
        print(f'{file_name}:{line}')
    else:
        print(line)


def working_with_stdin(pattern: str, regex: bool, count: bool) -> None:
    counter = 0
    for line in sys.stdin.readlines():
        line = line.rstrip('\n')
        if (pattern in line or re.search(pattern, line)):
            counter += 1
        if regex:
            if re.search(pattern, line):
                print(line)
        if (not regex and not count):
            if pattern in line:
                print(line)
    if count:
        print(counter)


def working_with_files(files: List[str], pattern: str, regex: bool, count: bool) -> None:
    for file_name in files:
        counter = 0
        with open(file_name, 'r') as file:
            for line in file.readlines():
                line = line.rstrip('\n')
                if (pattern in line or re.search(pattern, line)):
                    counter += 1
                if regex:
                    if re.search(pattern, line):
                        print_in_files(bool(len(files) > 1), file_name, line)
                if (not regex and not count):
                    if pattern in line:
                        print_in_files(bool(len(files) > 1), file_name, line)
            if count:
                print_in_files(bool(len(files) > 1), file_name, str(counter))


def main(args_str: List[str]) -> None:
    args = parse_args(args_str)
    if args.files:
        working_with_files(args.files, args.pattern, args.regex, args.count)
    else:
        working_with_stdin(args.pattern, args.regex, args.count)


if __name__ == '__main__':
    main(sys.argv[1:])
