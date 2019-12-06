#!/usr/bin/env python3

from typing import List, Iterable
import sys
import re
import argparse


def filter_strings_by_pattern(pattern: str,
                              data: Iterable[Iterable[str]]) -> List[List[str]]:
    return [[line for line in item if re.search(pattern, line)] for item in data]


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


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')

    args = parser.parse_args(args_str)

    pattern = args.needle
    count = args.count
    regex = args.regex
    files = args.files

    input_data = []
    if files:
        for file in files:
            with open(file, 'r') as input_file:
                input_data.append(strip_lines(input_file.readlines()))
    else:
        input_data.append(strip_lines(sys.stdin.readlines()))
        files.append(None)

    if not regex:
        pattern = re.escape(pattern)
    pattern = re.compile(pattern)

    filtered_strings = filter_strings_by_pattern(pattern, input_data)

    output_data = filtered_strings

    if count:
        output_data = count_filtered_strings(filtered_strings)

    print_lines(files, output_data, len(files) > 1)


if __name__ == '__main__':
    main(sys.argv[1:])
