#!/usr/bin/env python3

from typing import List, Callable
import sys
import re
import argparse


def files_to_strings(files: List[str]) -> List[List[str]]:
    result_files = []
    for filename in files:
        try:
            with open(filename, 'r') as f:
                result_files.append([string.rstrip('\n')
                                     for string in f.readlines()])
        except (FileNotFoundError, IsADirectoryError) as exception:
            print(exception)
            sys.exit()
    return result_files


def stdin_to_strings() -> List[List[str]]:
    return [[string.rstrip('\n')
             for string in sys.stdin.readlines()]]


def match_regex(string: str, pattern: str) -> bool:
    return bool(re.search(pattern, string))


def match_substr(string: str, pattern: str) -> bool:
    return pattern in string


def print_all(filename: str, match: List[str], single_file: bool) -> None:
    for string in match:
        if not single_file:
            print(f'{filename}:{string}')
        else:
            print(string)


def print_count(filename: str, match: List[str], single_file: bool) -> None:
    if not single_file:
        print(f'{filename}:{len(match)}')
    else:
        print(len(match))


def get_matched_strings(
        strings: List[str],
        pattern: str,
        match_function: Callable[[str, str], bool]) -> List[str]:

    return list(
        filter(
            lambda string: match_function(string, pattern),
            strings
        ))


def main(args_str: List[str]):
    parser = argparse.ArgumentParser(description='search for PATTERN in FILES')
    parser.add_argument('pattern', type=str)
    pattern_selection_group = parser.add_argument_group('pattern selection')
    output_control_group = parser.add_argument_group('output control')
    pattern_selection_group.add_argument(
        '-E', dest='pattern_regex', action='store_true', help='PATTERN is a regular expression')
    output_control_group.add_argument(
        '-c', dest='print_count', action='store_true', help='print count of selected lines')
    parser.add_argument('files', metavar='file', type=str, nargs='*')
    args = parser.parse_args(args_str)

    filenames = args.files
    files = files_to_strings(args.files)
    if len(files) == 0:
        filenames = ['sys.stdin']
        files = stdin_to_strings()

    match_function = match_substr
    if args.pattern_regex:
        match_function = match_regex

    matched_strings = [
        get_matched_strings(strings, args.pattern, match_function)
        for filename, strings in zip(filenames, files)
    ]

    print_result_function = print_all
    if args.print_count:
        print_result_function = print_count

    for filename, match in zip(filenames, matched_strings):
        print_result_function(filename, match, len(filenames) == 1)


if __name__ == '__main__':
    main(sys.argv[1:])
