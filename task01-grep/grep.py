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
        if line:
            print(line)


def match_pattern(pattern: str, line: str, is_regex: bool,
                  is_ignore: bool, is_full_match: bool) -> bool:
    if not is_regex:
        pattern = re.escape(pattern)
    if is_full_match:
        return bool(re.fullmatch(pattern, line, re.IGNORECASE * is_ignore))
    else:
        return bool(re.search(pattern, line, re.IGNORECASE * is_ignore))


def filter_lines(pattern: str, lines: Iterable, is_regex: bool, is_ignore: bool,
                 is_full_match: bool, is_inverse: bool) -> List[str]:
    if is_inverse:
        return [line for line in lines
                if not match_pattern(pattern, line, is_regex, is_ignore, is_full_match)]
    else:
        return [line for line in lines
                if match_pattern(pattern, line, is_regex, is_ignore, is_full_match)]


def format_lines(result, filename, is_has_lines, is_no_lines):
    if is_has_lines:
        if int(result) > 0:
            return f'{filename}'
    elif is_no_lines:
        if not int(result):
            return f'{filename}'
    else:
        return f'{filename}:{result}'


def grep_lines(lines: Iterable, filename: Optional[str], pattern: str, is_regex: bool,
               counting_mode: bool, is_ignore: bool, is_has_lines: bool, is_no_lines: bool,
               is_full_match: bool, is_inverse: bool) -> List[str]:
    result = filter_lines(pattern, lines, is_regex, is_ignore, is_full_match, is_inverse)
    if counting_mode or is_has_lines or is_no_lines:
        result = [str(len(result))]
    if filename:
        result = [format_lines(line, filename, is_has_lines, is_no_lines) for line in result]
    return result


def strip_lines(lines: Iterable) -> List[str]:
    return [line.rstrip('\n') for line in lines]


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-i', dest='ignore', action='store_true')
    parser.add_argument('-v', dest='inverse', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    parser.add_argument('-l', dest='has_lines', action='store_true')
    parser.add_argument('-L', dest='no_lines', action='store_true')
    args = parser.parse_args(args_str)

    if args.files:
        all_lines, filenames = [], []
        for filename in args.files:
            if os.path.isfile(filename):
                filenames.append(filename)
            else:
                print('File not found')
        for filename in filenames:
            with open(filename, 'r') as input_file:
                all_lines.append(input_file.readlines())
    else:
        all_lines = [sys.stdin.readlines()]
        filenames = [None]

    for lines, filename in zip(all_lines, filenames):
        lines = strip_lines(lines)
        prefix = filename if len(args.files) > 1 else None
        print_result(grep_lines(lines, prefix,
                                args.needle, args.regex, args.count, args.ignore,
                                args.has_lines, args.no_lines, args.full_match, args.inverse))


if __name__ == '__main__':
    main(sys.argv[1:])
