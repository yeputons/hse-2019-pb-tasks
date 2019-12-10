#!/usr/bin/env python3
import os
from typing import List, Iterable, Tuple, Pattern
import sys
import re
import argparse


def find_pattern_in_line(pattern: Pattern[str], line: str, equal: bool) -> bool:
    if equal:
        return re.fullmatch(pattern, line) is not None
    return re.search(pattern, line) is not None


def cast_to_regex(regex_mode: bool, pattern: str) -> str:
    if not regex_mode:
        return re.escape(pattern)
    return pattern


def format_output(print_file_name: bool, source: str) -> str:
    print_format = '{}'
    if print_file_name:
        print_format = '{0}:{1}'.format(source, print_format)
    return print_format


def print_result(format_of_output: str, filename: str, output: List[str],
                 at_least_one_found: bool, no_one_found: bool) -> None:
    if at_least_one_found and len(output) > 0:
        print(filename)
    if no_one_found and len(output) == 0:
        print(filename)
    if not at_least_one_found and not no_one_found:
        for print_output in output:
            print(format_of_output.format(print_output))


def find_pattern(counting_mode: bool, file: List[str], pattern: Pattern[str], equal: bool,
                 invert_result: bool) -> List[str]:
    result = [line for line in file if invert_result ^ find_pattern_in_line(pattern, line, equal)]
    if counting_mode:
        return [str(len(result))]
    else:
        return result


def strip_lines(file: Iterable) -> List[str]:
    return [line.rstrip('\n') for line in file]


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='counting_mode', action='store_true')
    parser.add_argument('-E', dest='regex_mode', action='store_true')
    parser.add_argument('-i', dest='ignore_case', action='store_true')
    parser.add_argument('-v', dest='invert_result', action='store_true')
    parser.add_argument('-x', dest='equal', action='store_true')
    parser.add_argument('-l', dest='at_least_one_found', action='store_true')
    parser.add_argument('-L', dest='no_one_found', action='store_true')

    args = parser.parse_args(args_str)
    print_file_name = len(args.files) > 1
    args.pattern = cast_to_regex(args.regex_mode, args.pattern)
    flag = 0
    if args.ignore_case:
        flag = re.IGNORECASE
    args.pattern = re.compile(args.pattern, flags=flag)
    data_from_files: List[Tuple[str, List[str]]] = []
    if len(args.files) != 0:
        for filename in args.files:
            if not os.path.exists(filename):
                "File {} doesn't exist".format(filename)
            else:
                with open(filename, 'r') as input_file:
                    data_from_files.append((filename, strip_lines(input_file)))
    else:
        data_from_files.append((' ', strip_lines(sys.stdin)))

    for filename, source_from_file in data_from_files:
        source_from_file = find_pattern(args.counting_mode, source_from_file,
                                        args.pattern, args.equal, args.invert_result)
        print_format = format_output(print_file_name, filename)
        print_result(print_format, filename, source_from_file,
                     args.at_least_one_found, args.no_one_found)


if __name__ == '__main__':
    main(sys.argv[1:])
