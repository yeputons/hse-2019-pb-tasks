# !/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def read_stdin() -> List[str]:
    new_lines = [line for line in sys.stdin.readlines()]
    return new_lines


def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as in_file:
        new_lines = [line for line in in_file.readlines()]
    return new_lines


def is_line_in_answer(line: str, pattern: str, text_flags: dict) -> bool:
    result = False
    if not text_flags.get('is_regex'):
        pattern = re.escape(pattern)
    if text_flags.get('full_matches'):
        pattern = '^' + pattern + '$'
    if text_flags.get('is_ignore_case') and \
            re.search(re.compile(pattern.lower()), line.lower()) or \
            not text_flags.get('is_ignore_case') and \
            re.search(re.compile(pattern), line):
        result = True
    if text_flags.get('invert_result'):
        if result:
            result = False
        else:
            result = True
    return result


def working_with_text_flags(lines: List[str], pattern: str, flags: dict) -> List[str]:
    new_list_of_lines = [line for line in lines if is_line_in_answer(line, pattern, flags)]
    return new_list_of_lines


def working_with_print_flags(lines: List[str], prefix: str,
                             number_of_files: int, flags: dict) -> List[str]:
    if flags.get('count_mode'):
        lines = [str(len(lines))]
    if number_of_files > 2:
        lines = [f'{prefix}:{line}' for line in lines]
    lines = [line.rstrip('\n') for line in lines]
    if flags.get('filenames_matches_exist'):
        if len(lines) > 0:
            lines = [prefix]
        else:
            lines = []
    if flags.get('filenames_matches_not_exist'):
        if len(lines) > 0:
            lines = []
        else:
            lines = [prefix]
    return lines


def printing(lines: list) -> None:
    for line in lines:
        print(line)


def format_and_print_lines(list_of_lines: List[List[str]], files: List[str],
                           flags: dict, pattern: str) -> None:
    files.append('')
    for i, lines in enumerate(list_of_lines):
        lines = working_with_text_flags(lines, pattern, flags)
        lines = working_with_print_flags(lines, files[i], len(files), flags)
        printing(lines)


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
    flags = {'is_regex': args.regex, 'count_mode': args.count, 'is_ignore_case': args.ignore,
             'invert_result': args.invert, 'full_matches': args.full_matches,
             'filenames_matches_exist': args.filenames_exist,
             'filenames_matches_not_exist': args.filenames_not_exist}
    if len(args.files) > 0:
        list_of_lines = [read_file(filename) for filename in args.files]
    else:
        list_of_lines = [read_stdin()]
    format_and_print_lines(list_of_lines, args.files, flags, args.pattern)


if __name__ == '__main__':
    main(sys.argv[1:])
