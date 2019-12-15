#!/usr/bin/env python3

from typing import Iterable, List, Tuple
import sys
import re
import argparse


def regex_search(pattern: str,
                 string: str,
                 full: bool) -> bool:
    if full:
        return bool(re.fullmatch(pattern, string))
    return bool(re.search(pattern, string))


def filter_strings_by_pattern(pattern: str,
                              data: Iterable[Iterable[str]],
                              inverse: bool,
                              full: bool) -> List[List[str]]:
    return [[line for line in item
             if inverse ^ regex_search(pattern, line, full)] for item in data]


def count_filtered_strings(data: Iterable[List[str]]) -> List[List[str]]:
    return [[str(len(item))] for item in data]


def format_output_string(name_file: str,
                         string: str,
                         file_is: bool) -> str:
    if file_is:
        return '{}:{}'.format(name_file, string)
    return string


def print_lines(lines: Iterable[str],
                name_file: str,
                file_is: bool):
    for line in lines:
        output_string = format_output_string(name_file, line, file_is)
        print(output_string)


def strip_lines(lines: Iterable[str]) -> List[str]:
    return [line.rstrip('\n') for line in lines]


def match_files_with_filtered_strings(data: Iterable[Tuple[str, Iterable[str]]],
                                      flag_not_strings: bool) -> List[List[str]]:
    file_names = []
    for name_file, item in data:
        if bool(item) ^ flag_not_strings:
            file_names.append(name_file)
    return [file_names]


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
    group.add_argument('-l', dest='files_with_filtered_strings', action='store_true')
    group.add_argument('-L', dest='files_without_filtered_strings', action='store_true')

    args = parser.parse_args(args_str)

    pattern = args.needle
    count = args.count
    regex = args.regex
    files = args.files
    ignore = args.ignore
    invert = args.invert
    full_match = args.full_match
    files_with_filtered_strings = args.files_with_filtered_strings
    files_without_filtered_strings = args.files_without_filtered_strings

    input_data = []
    if files:
        for file in files:
            with open(file, 'r') as input_file:
                input_data.append(input_file.readlines())
    else:
        input_data.append(sys.stdin.readlines())

    data = [strip_lines(lines) for lines in input_data]

    if not regex:
        pattern = re.escape(pattern)

    flags = 0
    if ignore:
        flags = re.IGNORECASE
    pattern = re.compile(pattern, flags=flags)

    filtered_strings = filter_strings_by_pattern(pattern,
                                                 data,
                                                 invert,
                                                 full_match)

    output_data = filtered_strings

    if count:
        output_data = count_filtered_strings(filtered_strings)
    elif files_with_filtered_strings or files_without_filtered_strings:
        output_data = match_files_with_filtered_strings(
            list(zip(files, filtered_strings)),
            files_without_filtered_strings)

    if files_with_filtered_strings or \
       files_without_filtered_strings or \
       not files:
        files = [None]

    for lines, name_file in zip(output_data, files):
        print_lines(lines, name_file, len(files) > 1)


if __name__ == '__main__':
    main(sys.argv[1:])
