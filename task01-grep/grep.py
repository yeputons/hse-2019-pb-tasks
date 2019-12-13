#!/usr/bin/env python3

from typing import List, Iterable
import sys
import re
import argparse


def filter_strings_by_pattern_with_cond(pattern: str,
                                        data: Iterable[Iterable[str]],
                                        cond: bool) -> List[List[str]]:
    return [[line for line in item if cond ^ bool(re.search(pattern, line))]
            for item in data]


def count_filtered_strings(data: Iterable[Iterable[str]]) -> List[List[str]]:
    return [[str(sum(1 for _ in item))] for item in data]


def format_output_string(name_file: str,
                         line: str,
                         cond: bool):
    if cond:
        return '{}:{}'.format(name_file, line)
    return line


def print_lines(files: Iterable[str],
                data: Iterable[Iterable[str]],
                cond: bool):
    for name_file, item in zip(files, data):
        for line in item:
            print(format_output_string(name_file, line, cond))


def strip_lines(lines: Iterable[str]) -> List[str]:
    return [line.rstrip('\n') for line in lines]


def match_files_with_filtered_strings(files: Iterable[str],
                                      data: Iterable[Iterable[str]],
                                      cond: bool) -> List[List[str]]:
    result = []
    for name_file, item in zip(files, data):
        if bool(item) ^ cond:
            result.append(name_file)
    return [result]


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-i', dest='ignore', action='store_true')
    parser.add_argument('-v', dest='invert', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', dest='count', action='store_true')
    group.add_argument('-l', dest='only_files_with_filtered_strings', action='store_true')
    group.add_argument('-L', dest='only_files_without_filtered_strings', action='store_true')

    args = parser.parse_args(args_str)

    pattern = args.needle
    count = args.count
    regex = args.regex
    files = args.files
    ignore = args.ignore
    invert = args.invert
    full_match = args.full_match
    only_files_with_filtered_strings = args.only_files_with_filtered_strings
    only_files_without_filtered_strings = args.only_files_without_filtered_strings

    input_data = []
    if files:
        for file in files:
            with open(file, 'r') as input_file:
                input_data.append(strip_lines(input_file.readlines()))
    else:
        input_data.append(strip_lines(sys.stdin.readlines()))

    if not regex:
        pattern = re.escape(pattern)

    if full_match:
        pattern = '^{}$'.format(pattern)

    if ignore:
        pattern = re.compile(pattern, re.IGNORECASE)
    else:
        pattern = re.compile(pattern)

    filtered_strings = filter_strings_by_pattern_with_cond(pattern,
                                                           input_data,
                                                           invert)

    output_data = filtered_strings

    if count:
        output_data = count_filtered_strings(filtered_strings)
    elif only_files_with_filtered_strings:
        output_data = match_files_with_filtered_strings(files,
                                                        filtered_strings,
                                                        False)
    elif only_files_without_filtered_strings:
        output_data = match_files_with_filtered_strings(files,
                                                        filtered_strings,
                                                        True)

    if only_files_with_filtered_strings or \
       only_files_without_filtered_strings or \
       not files:
        files = [None]

    print_lines(files, output_data, bool(len(files) > 1))


if __name__ == '__main__':
    main(sys.argv[1:])
