#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse
import os.path


def get_lines(in_lines: List[str]) -> List[str]:
    lines = []
    for line in in_lines:
        lines.append(line.rstrip('\n'))
    return lines


def read_files(file_name: str) -> List[str]:
    with open(file_name, 'r') as in_file:
        lines = get_lines(in_file.readlines())
    return lines


def filter_lines(lines: List[str], pattern: str, is_regex: bool) -> List[str]:
    if is_regex:
        return list(filter(lambda line: re.search(re.compile(pattern), line), lines))
    else:
        return list(filter(lambda line: re.search(re.escape(pattern), line), lines))


def count_lines(lines: list) -> int:
    return len(lines)


def print_output(out: list, is_many: bool, file_name: str) -> None:
    for line in out:
        if is_many:
            print(f'{file_name}:{line}')
        else:
            print(line)


def print_counter(counter: int, is_many: bool, file_name: str) -> None:
    if is_many:
        print(f'{file_name}:{counter}')
    else:
        print(counter)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('-c', dest='counter', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('files', nargs='*')
    args = parser.parse_args(args_str)

    exist_file = len(args.files) > 0

    if not args.files:
        args.files.append(sys.stdin)
    else:
        for file in args.files:
            if not os.path.exists(file):
                print(f"File {file} doesn't exist")
                sys.exit()

    is_many = len(args.files) > 1

    for file in args.files:

        src = read_files(file) if exist_file else get_lines(sys.stdin.readlines())

        if args.counter:
            print_counter(count_lines(filter_lines(src, args.pattern, args.regex)), is_many, file)
        else:
            print_output(filter_lines(src, args.pattern, args.regex), is_many, file)


if __name__ == '__main__':
    main(sys.argv[1:])
