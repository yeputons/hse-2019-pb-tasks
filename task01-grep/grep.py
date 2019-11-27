#!/usr/bin/env python3

from typing import List
import sys
import re
import argparse


def filter_strings_by_pattern(pattern: str, data: List[List[str]]) -> List[List[str]]:
    result = []
    for file in data:
        result.append([line for line in file if re.search(pattern, line)])
    return result


def count_filtered_strings(data: List[List[str]]) -> List[List[str]]:
    return [[str(len(item))] for item in data]


def print_lines(files: List[str], data: List[List[str]], cond: bool):
    for index, file in enumerate(files):
        for string in data[index]:
            line = string
            if cond:
                line = file + ':' + string
            print(line)


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
            with open(file, 'r') as in_file:
                input_data.append([line.rstrip('\n') for line in in_file.readlines()])
    else:
        input_data.append([line.rstrip('\n') for line in sys.stdin.readlines()])
        files = [None]

    if regex:
        pattern = re.compile(pattern)
    else:
        pattern = re.escape(pattern)

    filtered_strings = filter_strings_by_pattern(pattern, input_data)

    output_data = filtered_strings

    if count:
        output_data = count_filtered_strings(filtered_strings)

    print_lines(files, output_data, bool(len(files) - 1))


if __name__ == '__main__':
    main(sys.argv[1:])
