#!/usr/bin/env python3
from typing import List
from typing import Iterable
from typing import Pattern
import sys
import re
import argparse as ap


def parse_args(args_str: List[str]) -> ap.Namespace:
    parser = ap.ArgumentParser()
    parser.add_argument('-v', dest='inverse', action='store_true')
    parser.add_argument('-i', dest='ignore', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    parser.add_argument('-c', dest='counting_mode', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-l', dest='with_files', action='store_true')
    parser.add_argument('-L', dest='with_files_invert', action='store_true')
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    return parser.parse_args(args_str)


def compile_pattern(pattern: str, is_regex: bool, is_ignore: bool = False) -> Pattern:
    if not is_regex:
        pattern = re.escape(pattern)
    return re.compile(pattern, flags=re.IGNORECASE) if is_ignore else re.compile(pattern)


def is_matching(line: str, pattern: Pattern[str],
                inverse: bool = False, full_match: bool = False) -> bool:
    return inverse ^ bool(re.fullmatch(pattern, line)
                          if full_match else re.search(pattern, line))


def filter_matching_lines(lines: List[str], pattern: Pattern[str],
                          full_match: bool = False, inverse: bool = False) -> List[str]:
    return [line for line in lines
            if is_matching(line, pattern, inverse, full_match)]


def format_output(lines: List[str], counting_mode: bool,
                  with_files: bool = False, with_files_invert: bool = False,
                  source: str = None) -> List[str]:
    if with_files or with_files_invert:
        assert source
        return [source] if with_files_invert ^ bool(lines) else []
    if counting_mode:
        lines = [str(len(lines))]
    if source:
        return [f'{source}:{line}' for line in lines]
    else:
        return lines


def strip_lines(source: Iterable) -> List[str]:
    return [line.rstrip('\n') for line in source]


def grep_from_raw(raw_lines: Iterable, pattern: Pattern[str],
                  counting_mode: bool, with_files: bool = False,
                  with_files_invert: bool = False, full_match: bool = False, inverse: bool = False,
                  source: str = None) -> List[str]:
    lines = strip_lines(raw_lines)
    value: List[str] = filter_matching_lines(lines, pattern,
                                             full_match, inverse)
    value = format_output(value, counting_mode, with_files, with_files_invert, source)
    return value


def print_answer(result: List[str]) -> None:
    for line in result:
        print(line)


def main(args_str: List[str]):
    args: ap.Namespace = parse_args(args_str)
    pattern: Pattern[str] = compile_pattern(args.pattern, args.regex, args.ignore)
    for file in args.files:
        with open(file, 'r') as input_file:
            result = grep_from_raw(input_file.readlines(), pattern,
                                   args.counting_mode, args.with_files, args.with_files_invert,
                                   args.full_match, args.inverse,
                                   file if len(args.files) > 1 else None)
            print_answer(result)

    if not args.files:
        result = grep_from_raw(sys.stdin.readlines(), pattern,
                               args.counting_mode, args.with_files, args.with_files_invert,
                               args.full_match, args.inverse)
        print_answer(result)


if __name__ == '__main__':
    main(sys.argv[1:])
