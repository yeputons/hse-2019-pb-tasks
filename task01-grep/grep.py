#!/usr/bin/env python3

from typing import List
from typing import Optional
from typing import Iterable


import sys
import re
import argparse


def format_output_line(source: Optional[str], result) -> str:
    return '{}:{}'.format(source, result)


def filter_lines(lines: List[str], pattern: str, is_regex: bool = False) -> List[str]:
    if not is_regex:
        pattern = re.escape(pattern)

    regular_expression = re.compile(pattern)

    return [line for line in lines if regular_expression.search(line)]


def format_output_lines(lines: List[str], source: Optional[str]) -> List[str]:
    return [format_output_line(source, line) for line in lines]


def exec_grep(lines: List[str], pattern: str,
              is_regex: bool = False,
              counting_mode: bool = False,
              source: Optional[str] = None) -> List[str]:

    result = filter_lines(lines, pattern, is_regex)

    if counting_mode:
        result = [str(len(result))]

    if source:
        result = format_output_lines(result, source)

    return result


def print_result(result: List[str]) -> None:
    for line in result:
        print(line)


def get_striped_lines(lines: Iterable) -> List[str]:
    return [line.rstrip('\n') for line in lines]


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('filenames', nargs='*')
    parser.add_argument('-c', dest='counting_mode', action='store_true')
    parser.add_argument('-E', dest='is_regex', action='store_true')

    args = parser.parse_args(args_str)

    files = [open(file, 'r') for file in args.filenames]

    if not args.filenames:
        files.append(sys.stdin)

    source_printing_mode = len(args.filenames) > 1

    for file in files:
        lines = get_striped_lines(file)
        print_result(exec_grep(lines, args.pattern, args.is_regex, args.counting_mode,
                               file.name if source_printing_mode else None))


if __name__ == '__main__':
    main(sys.argv[1:])
