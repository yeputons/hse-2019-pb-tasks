#!/usr/bin/env python3
from typing import Iterable, List, Pattern
import sys
import re
import argparse


def print_result(result: Iterable) -> None:
    for line in result:
        print(line)


def compile_pattern(pattern: str, is_regex: bool, ignore_mode: bool):
    if not is_regex:
        pattern = re.escape(pattern)
    return re.compile(pattern, flags=re.IGNORECASE) if ignore_mode else re.compile(pattern)


def match_pattern(pattern: Pattern[str], line: str, full_match: bool, inverse_mode: bool) -> bool:
    matched = pattern.fullmatch(line) if full_match else re.search(pattern, line)
    return bool(matched) ^ inverse_mode


def filter_lines(pattern: Pattern[str], lines: Iterable, full_match: bool,
                 inverse_mode: bool) -> List[str]:
    return [line for line in lines if match_pattern(pattern, line, full_match, inverse_mode)]


def grep_lines(lines: Iterable, prefix: str, pattern: Pattern[str],
               counting_mode: bool, only_files_mode: bool, only_not_files_mode: bool,
               full_match: bool, inverse_mode: bool) -> List[str]:
    result = filter_lines(pattern, lines, full_match, inverse_mode)
    if only_files_mode or only_not_files_mode:
        return [prefix] if only_not_files_mode ^ bool(result) else []
    if counting_mode:
        result = [str(len(result))]
    if prefix:
        return [f'{prefix}:{line}' for line in result]
    else:
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
    parser.add_argument('-l', dest='only_files', action='store_true')
    parser.add_argument('-L', dest='only_not_files', action='store_true')
    args = parser.parse_args(args_str)

    if args.files:
        all_lines, filenames = [], []
        for filename in args.files:
            filenames.append(filename)
        for filename in filenames:
            with open(filename, 'r') as input_file:
                all_lines.append(input_file.readlines())
                all_lines = [strip_lines(line) for line in all_lines]
    else:
        all_lines = [sys.stdin.readlines()]
        all_lines = [strip_lines(line) for line in all_lines]
        filenames = [None]

    pattern = compile_pattern(args.needle, args.regex, args.ignore)

    for lines, filename in zip(all_lines, filenames):
        prefix = filename if len(args.files) > 1 else None
        print_result(grep_lines(lines, prefix, pattern, args.count, args.only_files,
                                args.only_not_files, args.full_match, args.inverse))


if __name__ == '__main__':
    main(sys.argv[1:])
