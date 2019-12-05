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


def check_if_line_in_answer(line: str, pattern: str, is_ignore_case: bool, invert_result: bool) -> bool:
    result = False
    if is_ignore_case and \
            re.search(re.compile(pattern.lower()), line.lower()) or \
            not is_ignore_case and \
            re.search(re.compile(pattern), line):
        result = True
    if invert_result:
        return not result
    return result


def working_with_text_flags(lines: List[str], pattern: str, is_ignore_case: bool, invert_result: bool) -> List[str]:
    lines = [line.rstrip('\n') for line in lines]
    new_list_of_lines = [line for line in lines if
                         check_if_line_in_answer(line, pattern, is_ignore_case, invert_result)]
    return new_list_of_lines


def working_with_print_flags(lines: List[str], source: str,
                             number_of_files: bool, flags: dict) -> List[str]:
    if flags.get('count_mode'):
        lines = [str(len(lines))]
    if number_of_files:
        lines = [f'{source}:{line}' for line in lines]
    if flags.get('filenames_matches_exist'):
        if lines:
            lines = [source]
        else:
            lines = []
    if flags.get('filenames_matches_not_exist'):
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
    print_flags = {'count_mode': args.count, 'filenames_matches_exist': args.filenames_exist,
                   'filenames_matches_not_exist': args.filenames_not_exist}
    if len(args.files) > 0:
        list_of_lines = [read_file(filename) for filename in args.files]
    else:
        list_of_lines = [read_stdin()]
    args.files.append('')
    pattern = pattern_format(args.pattern, args.regex, args.full_matches)
    for i, lines in enumerate(list_of_lines):
        lines = working_with_text_flags(lines, pattern, args.ignore, args.invert)
        lines = working_with_print_flags(lines, args.files[i], len(args.files) > 2, print_flags)
        printing(lines)


if __name__ == '__main__':
    main(sys.argv[1:])
