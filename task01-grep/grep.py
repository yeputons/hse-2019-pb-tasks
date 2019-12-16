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


def print_filenames(filename: str, match: List[str], rev: bool) -> None:
    if rev ^ (len(match) > 0):
        print(filename)


def get_matched_strings(
        strings: List[str],
        pattern: str,
        match_function: Callable[[str, str], bool]) -> List[str]:

    return list(
        filter(
            lambda string: match_function(string, pattern),
            strings
        ))


def select_matcher(pattern_regex: bool,
                   pattern_ignore_case: bool,
                   pattern_full_match: bool,
                   pattern_reverse_result: bool) -> Callable[[str, str], bool]:
    def match_function(string: str, pattern: str) -> bool:
        pattern = pattern if pattern_regex else re.escape(pattern)
        ignore_case = re.IGNORECASE if pattern_ignore_case else 0
        if pattern_full_match:
            result = bool(re.fullmatch(pattern, string, flags=ignore_case))
        else:
            result = bool(re.search(pattern, string, flags=ignore_case))
        if pattern_reverse_result:
            return not result
        return result

    return match_function


def select_printer(arg_print_filenames: bool,
                   arg_print_filenames_without: bool,
                   arg_print_count: bool,
                   is_single: bool) -> Callable[[str, List[str]], None]:
    def print_function(filename: str, match: List[str]) -> None:
        if arg_print_filenames:
            print_filenames(filename, match, False)
        elif arg_print_filenames_without:
            print_filenames(filename, match, True)
        elif arg_print_count:
            print_count(filename, match, is_single)
        else:
            print_all(filename, match, is_single)

    return print_function


def main(args_str: List[str]):
    parser = argparse.ArgumentParser(description='search for PATTERN in FILES')
    parser.add_argument('pattern', type=str)

    pattern_selection_group = parser.add_argument_group('pattern selection')
    output_control_group = parser.add_argument_group('output control')

    pattern_selection_group.add_argument(
        '-v',
        dest='pattern_reverse_result',
        action='store_true',
        help='select non-matching lines')
    pattern_selection_group.add_argument(
        '-E',
        dest='pattern_regex',
        action='store_true',
        help='PATTERN is a regular expression')
    pattern_selection_group.add_argument(
        '-x',
        dest='pattern_full_match',
        action='store_true',
        help='force PATTERN to match only whole lines')
    pattern_selection_group.add_argument(
        '-i',
        dest='pattern_ignore_case',
        action='store_true',
        help='ignore case distinctions')

    output_control_group.add_argument(
        '-c',
        dest='print_count',
        action='store_true',
        help='print count of selected lines')
    output_control_group.add_argument(
        '-l',
        dest='print_filenames',
        action='store_true',
        help='print names of files with matches')
    output_control_group.add_argument(
        '-L',
        dest='print_filenames_without',
        action='store_true',
        help='print names of files without any matches')
    parser.add_argument('files', metavar='file', type=str, nargs='*')
    args = parser.parse_args(args_str)
    filenames = args.files
    files = files_to_strings(filenames)
    if not files:
        filenames = ['sys.stdin']
        files = stdin_to_strings()

    match_function = select_matcher(args.pattern_regex,
                                    args.pattern_ignore_case,
                                    args.pattern_full_match,
                                    args.pattern_reverse_result)

    matched_strings = [
        get_matched_strings(strings,
                            args.pattern,
                            match_function)
        for filename, strings in zip(filenames, files)
    ]

    print_result_function = select_printer(args.print_filenames,
                                           args.print_filenames_without,
                                           args.print_count,
                                           len(filenames) == 1)

    for filename, match in zip(filenames, matched_strings):
        print_result_function(filename, match)


if __name__ == '__main__':
    main(sys.argv[1:])
