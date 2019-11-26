#!/usr/bin/env python3
from typing import List
from typing import Iterable
from typing import Optional
import sys
import re
import argparse


def make_format_lines_with_file_name(source: str, value: str) -> str:
    return f'{source}:{value}'


def is_matching(line: str, is_regex: bool, pattern: str) -> bool:
    if is_regex:
        return bool(re.search(pattern, line))
    else:
        return pattern in line


def filter_matching_lines(lines: Iterable, is_regex: bool, pattern: str) -> List[str]:
    line_value = []
    for line in lines:
        if is_matching(line, is_regex, pattern):
            line_value.append(line)
    return line_value


def format_output(lines: List[str], counting_mode: bool,
                  source: Optional[str]) -> List[str]:
    if counting_mode:
        lines = [str(len(lines))]
    if source:
        lines = [make_format_lines_with_file_name(source, line) for line in lines]

    return lines


def strip_lines(source: Iterable) -> List[str]:
    return [line.rstrip('\n') for line in source]


def grep_from_raw(raw_lines: Iterable, pattern: str, is_regex: bool,
                  counting_mode: bool, source: Optional[str] = None) -> List[str]:
    lines = strip_lines(raw_lines)
    value = filter_matching_lines(lines, is_regex, pattern)
    value = format_output(value, counting_mode, source)
    return value


def print_answer(result: Iterable) -> None:
    for line in result:
        print(line)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='counting_mode', action='store_true')
    args = parser.parse_args(args_str)
    for file in args.files:
        with open(file, 'r') as input_file:
            if len(args.files) > 1:
                result = grep_from_raw(input_file.readlines(), args.pattern, args.regex,
                                       args.counting_mode, file)
            else:
                result = grep_from_raw(input_file.readlines(), args.pattern,
                                       args.regex, args.counting_mode)
            print_answer(result)

    if not args.files:
        result = grep_from_raw(sys.stdin.readlines(), args.pattern,
                               args.regex, args.counting_mode, '')
        print_answer(result)


if __name__ == '__main__':
    main(sys.argv[1:])
