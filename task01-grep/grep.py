#!/usr/bin/env python3
from typing import List
from typing import Iterable
from typing import Pattern
import sys
import re
import argparse


def compile_pattern(pattern: str, is_regex: bool, is_ignore: bool) -> Pattern[str]:
    if not is_regex:
        pattern = re.escape(pattern)
    return re.compile(pattern, flags=re.IGNORECASE) if is_ignore else re.compile(pattern)


def is_matching(line: str, pattern: Pattern[str],
                is_inverse: bool, is_full_match: bool) -> bool:
    return is_inverse ^ bool(re.fullmatch(pattern, line)
                             if is_full_match else re.search(pattern, line))


def filter_matching_lines(lines: Iterable, pattern: Pattern[str],
                          is_full_match: bool, is_inverse: bool) -> List[str]:
    return [line for line in lines
            if is_matching(line, pattern, is_inverse, is_full_match)]


def format_output(lines: List[str], counting_mode: bool,
                  is_lines: bool, is_no_lines: bool,
                  source: str) -> List[str]:
    if is_lines or is_no_lines:
        return [source] if is_no_lines ^ bool(lines) else []
    if counting_mode:
        lines = [str(len(lines))]
    if source:
        return [f'{source}:{line}' for line in lines]
    else:
        return lines


def strip_lines(source: Iterable) -> List[str]:
    return [line.rstrip('\n') for line in source]


def grep_from_raw(raw_lines: Iterable, pattern: Pattern[str],
                  counting_mode: bool, is_lines: bool,
                  is_no_lines: bool, is_full_match: bool, is_inverse: bool,
                  source: str) -> List[str]:
    lines = strip_lines(raw_lines)
    value = filter_matching_lines(lines, pattern,
                                  is_full_match, is_inverse)
    value = format_output(value, counting_mode, is_lines, is_no_lines, source)
    return value


def print_answer(result: Iterable) -> None:
    for line in result:
        if line:
            print(line)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='counting_mode', action='store_true')
    parser.add_argument('-i', dest='ignore', action='store_true')
    parser.add_argument('-v', dest='inverse', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    parser.add_argument('-l', dest='lines', action='store_true')
    parser.add_argument('-L', dest='no_lines', action='store_true')
    args = parser.parse_args(args_str)
    pattern: Pattern[str] = compile_pattern(args.pattern, args.regex, args.ignore)
    for file in args.files:
        with open(file, 'r') as input_file:
            result = grep_from_raw(input_file.readlines(), pattern,
                                   args.counting_mode, args.lines, args.no_lines,
                                   args.full_match, args.inverse,
                                   file if len(args.files) > 1 else None)
            print_answer(result)

    if not args.files:
        result = grep_from_raw(sys.stdin.readlines(), pattern,
                               args.counting_mode, args.lines, args.no_lines,
                               args.full_match, args.inverse, '')
        print_answer(result)


if __name__ == '__main__':
    main(sys.argv[1:])
