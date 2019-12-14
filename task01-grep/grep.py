#!/usr/bin/env python3

from typing import List, Optional, Iterable, Any

import sys
import re
import argparse


def format_output_line(source: Optional[str], result) -> str:
    return '{}:{}'.format(source, result)


def filter_lines(lines: List[str],
                 pattern: str,
                 is_regex: bool = False,
                 is_ignorecase: bool = False,
                 is_fullmatch: bool = False) -> List[str]:
    if not is_regex:
        pattern = re.escape(pattern)

    regular_expression = re.compile(pattern, re.IGNORECASE if is_ignorecase else 0)

    search_function = regular_expression.fullmatch if is_fullmatch else regular_expression.search
    return [line for line in lines if search_function(line)]


def format_output_lines(lines: List[str], source: Optional[str]) -> List[str]:
    return [format_output_line(source, line) for line in lines]


def invert_inclusions(temp_inclusion: Iterable[Any], full_list: Iterable[Any]):
    return [line for line in full_list if line not in temp_inclusion]


def exec_grep(lines: List[str], pattern: str,
              is_regex: bool = False,
              counting_mode: bool = False,
              is_ignorecase: bool = False,
              is_fullmatch: bool = False,
              is_invert: bool = False,
              source: Optional[str] = None) -> List[str]:

    result = filter_lines(lines, pattern, is_regex, is_ignorecase, is_fullmatch)

    if is_invert:
        result = invert_inclusions(result, lines)

    if counting_mode:
        result = [str(len(result))]

    if source:
        result = format_output_lines(result, source)

    return result


def print_result(result: List[str]) -> None:
    for line in result:
        print(line)


def get_striped_lines(lines: Iterable[str]) -> List[str]:
    return [line.rstrip('\n') for line in lines]


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('filenames', nargs='*')

    parser.add_argument('-c', dest='counting_mode', action='store_true')
    parser.add_argument('-E', dest='is_regex', action='store_true')
    parser.add_argument('-i', dest='is_ignorecase', action='store_true')
    parser.add_argument('-x', dest='is_fullmatch', action='store_true')
    parser.add_argument('-v', dest='is_invert', action='store_true')
    parser.add_argument('-l', dest='mached_files_printing_mode', action='store_true')
    parser.add_argument('-L', dest='unmached_files_printing_mode', action='store_true')

    args = parser.parse_args(args_str)

    files = [open(file, 'r') for file in args.filenames]

    if not args.filenames:
        files.append(sys.stdin)

    source_printing_mode = len(args.filenames) > 1

    filenames_for_print = []

    for file in files:
        lines = get_striped_lines(file)
        result = exec_grep(lines, args.pattern, args.is_regex, args.counting_mode,
                           args.is_ignorecase, args.is_fullmatch, args.is_invert,
                           file.name if source_printing_mode else None)

        if args.mached_files_printing_mode or args.unmached_files_printing_mode:
            if result:
                filenames_for_print.append(file.name)
        else:
            print_result(result)

    if args.unmached_files_printing_mode:
        filenames_for_print = invert_inclusions(filenames_for_print,
                                                [file.name for file in files])

    print_result(filenames_for_print)


if __name__ == '__main__':
    main(sys.argv[1:])
