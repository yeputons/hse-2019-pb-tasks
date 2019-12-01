#!/usr/bin/env python3
from typing import Iterable
from typing import Optional
from typing import List
import sys
import re
import os
import argparse


def print_result(result: Iterable) -> None:
    for line in result:
        print(line)


def match_pattern(pattern: str, line: str, is_regex: bool) -> bool:
    if is_regex:
        return bool(re.search(pattern, line))
    else:
        return pattern in line


def filter_lines(pattern: str, lines: Iterable, is_regex: bool) -> List[str]:
    return [line for line in lines if match_pattern(pattern, line, is_regex)]


def grep_lines(lines: Iterable, filename: Optional[str], pattern: str, is_regex: bool,
               counting_mode: bool) -> List[str]:
    result = filter_lines(pattern, lines, is_regex)
    if counting_mode:
        result = [str(len(result))]
    if filename:
        result = [f'{filename}:{line}' for line in result]
    return result


def strip_lines(lines: Iterable) -> List[str]:
    return [line.rstrip('\n') for line in lines]


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    args = parser.parse_args(args_str)

    if not args.files:
        all_lines = [sys.stdin.readlines()]
        filenames = [None]
    else:
        all_lines, filenames = [], []
        for filename in args.files:
            if os.path.isfile(filename):
                filenames.append(filename)
        for filename in filenames:
            with open(filename, 'r') as input_file:
                all_lines.append(input_file.readlines())

    for lines, filename in zip(all_lines, filenames):
        lines = strip_lines(lines)
        print_result(grep_lines(lines, filename if len(args.files) > 1 else None, args.needle,
                                args.regex, args.count))


if __name__ == '__main__':
    main(sys.argv[1:])
