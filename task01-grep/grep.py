#!/usr/bin/env python3
from typing import List
from typing import Iterable
from typing import Union
import sys
import re
import argparse


def print_data(response: Union[str, int], name_of_file: str, is_needed_to_print: bool,
               is_name: bool):
    if is_name:
        print(f'{name_of_file}')
    else:
        if is_needed_to_print:
            print(f'{name_of_file}:', end='')
        print(f'{response}')


def matching_pattern(is_regex: bool, is_full_match: bool, is_register: bool,
                     pattern: str, line: str) -> bool:
    flags = 0
    beg = re.search
    if not is_regex:
        pattern = re.escape(pattern)
    if is_full_match:
        beg = re.fullmatch
    if is_register:
        flags = re.IGNORECASE
    res = beg(pattern, line, flags) is not None
    return res


# Простиии, я знаю, что это ужасная функция, но просто я не понимаю,
# как нормально её разбить на меньшие...


def process(list_of_lines: Iterable, name_of_file: str, needed_number_of_files: bool,
            pattern: str, is_regex: bool, is_count: bool, is_full_match: bool, is_register: bool,
            is_inversed_lines: bool, is_only_file: bool, is_inversed_file: bool):
    matching_lines = []
    not_matching_lines = []
    return_file = True
    for line in list_of_lines:
        line = line.rstrip('\n')
        if matching_pattern(is_regex, is_full_match, is_register, pattern, line):
            matching_lines.append(line)
        else:
            not_matching_lines.append(line)
    if is_count:
        is_name = False
        if is_inversed_lines:
            print_data(len(not_matching_lines), name_of_file, needed_number_of_files, is_name)
        else:
            print_data(len(matching_lines), name_of_file, needed_number_of_files, is_name)
    else:
        if is_inversed_file:
            lines = matching_lines if is_inversed_lines else not_matching_lines
            for line in lines:
                if return_file:
                    print_data(line, name_of_file, needed_number_of_files, is_inversed_file)
                    return_file = False
        elif is_only_file:
            lines = not_matching_lines if is_inversed_lines else matching_lines
            for line in lines:
                if return_file:
                    print_data(line, name_of_file, needed_number_of_files, is_only_file)
                    return_file = False
        else:
            is_name_of_file = False
            lines = not_matching_lines if is_inversed_lines else matching_lines
            for line in lines:
                print_data(line, name_of_file, needed_number_of_files, is_name_of_file)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='is_regex', action='store_true',
                        help='Looks for regular expression')
    parser.add_argument('-c', dest='is_count', action='store_true',
                        help='Counts how many lines contain the word or regular expression')
    parser.add_argument('-x', dest='is_full_match', action='store_true',
                        help='Returns full match')
    parser.add_argument('-v', dest='is_inversed_lines', action='store_true',
                        help='Returns the lines, which do not contain '
                             'the word or regular expression')
    parser.add_argument('-i', dest='is_register', action='store_true',
                        help='Ignores case')
    parser.add_argument('-l', dest='is_only_file', action='store_true',
                        help='Returns only names of files')
    parser.add_argument('-L', dest='is_inversed_file', action='store_true',
                        help='Returns only names of files, which do not contain the'
                             'word or regular expression')
    args = parser.parse_args(args_str)

    needed_number_of_files = bool(len(args.files) > 1)
    if args.files:
        for file in args.files:
            with open(file) as opened_file:
                process(opened_file.readlines(), file, needed_number_of_files, args.pattern,
                        args.is_regex, args.is_count, args.is_full_match, args.is_register,
                        args.is_inversed_lines, args.is_only_file, args.is_inversed_file)
    else:
        process(sys.stdin.readlines(), ' ', needed_number_of_files, args.pattern,
                args.is_regex, args.is_count, args.is_full_match, args.is_register,
                args.is_inversed_lines, args.is_only_file, args.is_inversed_file)


if __name__ == '__main__':
    main(sys.argv[1:])
