# !/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def read_stdin() -> List[str]:
    return sys.stdin.readlines()


def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as in_file:
        return in_file.readlines()


def pattern_format(pattern: str, is_regex: bool, full_matches: bool) -> str:
    if not is_regex:
        pattern = re.escape(pattern)
    if full_matches:
        pattern = f'^({pattern})$'
    return pattern


def check_if_line_in_answer(line: str, pattern: str, is_ignore_case: bool,
                            invert_result: bool) -> bool:
    result = False
    if is_ignore_case and re.search(re.compile(pattern.lower()), line.lower()):
        result = True
    if not is_ignore_case and re.search(re.compile(pattern), line):
        result = True
    if invert_result:
        return not result
    return result


def format_strings_with_text_flags(lines: List[str], pattern: str, is_ignore_case: bool,
                                   invert_result: bool) -> List[str]:
    new_list_of_lines = [line for line in lines
                         if check_if_line_in_answer(line, pattern, is_ignore_case, invert_result)]
    return new_list_of_lines


def format_lines_with_print_flags(lines: List[str], source: str,
                                  number_of_files: bool, count_mode: bool,
                                  filenames_matches_exist: bool,
                                  filenames_matches_not_exist: bool) -> List[str]:
    if count_mode:
        lines = [str(len(lines))]
    if number_of_files:
        lines = [f'{source}:{line}' for line in lines]
    if filenames_matches_exist:
        if lines:
            lines = [source]
        else:
            lines = []
    if filenames_matches_not_exist:
        if lines:
            lines = []
        else:
            lines = [source]
    return lines


def printing(lines: list) -> None:
    for line in lines:
        print(line)


def main(args_str: List[str]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-i', dest='ignore', action='store_true')
    parser.add_argument('-v', dest='invert', action='store_true')
    parser.add_argument('-x', dest='full_matches', action='store_true')
    parser.add_argument('-l', dest='filenames_exist', action='store_true')
    parser.add_argument('-L', dest='filenames_not_exist', action='store_true')
    args = parser.parse_args(args_str)

    if args.files:
        list_of_lines = [read_file(filename) for filename in args.files]
    else:
        list_of_lines = [read_stdin()]
    args.files.append('')
    pattern = pattern_format(args.pattern, args.regex, args.full_matches)
    for i, lines in enumerate(list_of_lines):
        lines = [line.rstrip('\n') for line in lines]
        lines = format_strings_with_text_flags(lines, pattern, args.ignore, args.invert)
        lines = format_lines_with_print_flags(lines, args.files[i], len(args.files) > 2, args.count,
                                              args.filenames_exist, args.filenames_not_exist)
        printing(lines)


if __name__ == '__main__':
    main(sys.argv[1:])
