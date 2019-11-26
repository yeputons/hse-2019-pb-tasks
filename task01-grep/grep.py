#!/usr/bin/env python3
import os
from typing import List, Iterable
import sys
import re
import argparse


def find_regex_mode(pattern: str, line: str) -> bool:
    return re.search(pattern, line) is not None


def find_pattern_in_line(regex_mode: bool, pattern: str, line: str) -> bool:
    if not regex_mode:
        pattern = re.escape(pattern)
    return find_regex_mode(pattern, line)


def format_output(print_file_name: bool, file_name: str) -> str:
    print_format = '{}'
    if print_file_name:
        print_format = '{0}:{1}'.format(file_name, print_format)
    return print_format


def print_result(format_of_output: str, output: list) -> None:
    for print_output in output:
        print(format_of_output.format(print_output))


def find_pattern(counting_mode: bool, regex_mode: bool, file: list, pattern: str) -> list:
    ans = []
    lines_count = 0
    for line in file:
        if find_pattern_in_line(regex_mode, pattern, line):
            ans.append(line)
            lines_count += 1
    if counting_mode:
        return list(str(lines_count))
    else:
        return ans


def read_from_file(file: Iterable) -> list:
    data_from_file = []
    for line in file:
        line = line.rstrip('\n')
        data_from_file.append(line)
    return data_from_file


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='counting_mode', action='store_true')
    parser.add_argument('-E', dest='regex_mode', action='store_true')
    args = parser.parse_args(args_str)
    print_file_name = len(args.files) > 1
    if len(args.files) != 0:
        for cur_file in args.files:
            if not os.path.exists(cur_file):
                "File {} doesn't exist".format(cur_file)
            else:
                with open(cur_file, 'r') as in_file:
                    source_from_file = read_from_file(in_file)
                    source_from_file = find_pattern(args.counting_mode, args.regex_mode,
                                                    source_from_file, args.pattern)
                    print_format = format_output(print_file_name, cur_file)
                    print_result(print_format, source_from_file)
    else:
        source_from_file = read_from_file(sys.stdin)
        source_from_file = find_pattern(args.counting_mode, args.regex_mode,
                                        source_from_file, args.pattern)
        print_format = format_output(print_file_name, ' ')
        print_result(print_format, source_from_file)


if __name__ == '__main__':
    main(sys.argv[1:])
