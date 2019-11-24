#!/usr/bin/env python3
"""
Grep(task01-grep)
by Obriadina Aleksandra
"""
from typing import List, TextIO
import sys
import re
import argparse


def parse_arguments(args_str: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-l', dest='files_with_matches', action='store_true')
    parser.add_argument('-L', dest='files_without_match', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-i', dest='ignore_case', action='store_true')
    parser.add_argument('-v', dest='invert_match', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    args = parser.parse_args(args_str)
    return args


def print_answer(lines: List[str], number_of_files: int, file_name: str, count_mode: bool) -> None:
    """ (1) if number of files is more than 1, prints <file_name>:<line>
        (2) if -c flag, prints the number of needles in stdin or in files;
        (3) if (1) and (2), prints <file_name>:<number of needles in <file_name>>"""
    if number_of_files <= 1:
        prefix = ''
    else:
        prefix = file_name + ':'
    if count_mode:
        print(prefix, len(lines), sep='')
    else:
        for line in lines:
            print(prefix, line, sep='')


def is_regex(needle: str, line: str, ignore_case_mode: bool, full_match_mode: bool) -> bool:
    """ Returns true if regex is found false otherwise """
    if full_match_mode:
        search_mode = re.fullmatch
    else:
        search_mode = re.search
    if ignore_case_mode:
        return search_mode(needle, line, re.IGNORECASE) is not None
    else:
        return search_mode(needle, line) is not None


def is_substring(needle: str, line: str, ignore_case_mode: bool, full_match_mode: bool) -> bool:
    """ Returns true if substring is found false otherwise """
    if ignore_case_mode:
        new_needle = needle.lower()
        new_line = line.lower()
    else:
        new_needle = needle
        new_line = line
    if full_match_mode:
        return new_needle == new_line
    else:
        return new_needle in new_line


def find_in_input(count_mode: bool, regex_mode: bool, ignore_case_mode: bool, invert_mode: bool,
                  full_match_mode: bool, needle: str, file: TextIO,
                  file_name: str, number_of_input_data: int) -> None:
    """ Prints lines with needles (substring or regex) or amount of them
        Works for -c and -E flags and input: stdin or file(s) """
    if regex_mode:
        search_mode = is_regex
    else:
        search_mode = is_substring
    answer_lines = []
    for line in file.readlines():
        line = line.rstrip('\n')
        if search_mode(needle, line, ignore_case_mode, full_match_mode) != invert_mode:
            answer_lines.append(line)
    print_answer(answer_lines, number_of_input_data, file_name, count_mode)


def find_in_files(args: argparse.Namespace) -> None:
    """ For each file, function opens it and calls find_in_input function
        one file: prints all lines with needles or amount of them (if -c)
        many files: prints <file_name> before searching results """
    for current_file in args.files:
        with open(current_file, 'r') as in_file:
            find_in_input(args.count, args.regex, args.ignore_case, args.invert_match, args.full_match,
                          args.needle, in_file, current_file, len(args.files))


def main(args_str: List[str]):
    """ Performs functionality of grep with flags -c and -E
        Input data: stdin or file(s) """
    args = parse_arguments(args_str)
    if args.files:
        find_in_files(args)
    else:
        find_in_input(args.count, args.regex, args.ignore_case, args.invert_match, args.full_match,
                      args.needle, sys.stdin, '', 0)


if __name__ == '__main__':
    main(sys.argv[1:])
