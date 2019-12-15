#!/usr/bin/env python3
import os
from typing import List, Iterable, Pattern, Dict
import sys
import re
import argparse


def find_pattern_in_line(pattern: Pattern[str], line: str, fullmatch: bool) -> bool:
    if fullmatch:
        return re.fullmatch(pattern, line) is not None
    return re.search(pattern, line) is not None


def cast_to_regex(regex_mode: bool, ignore_case: bool, pattern: str) -> Pattern[str]:
    if not regex_mode:
        pattern = re.escape(pattern)
    if ignore_case:
        return re.compile(pattern, flags=re.IGNORECASE)
    return re.compile(pattern)


def format_data(print_file_name: bool, source: str) -> str:
    if print_file_name:
        return '{0}:{1}'.format(source, '{}')
    return '{}'


def print_result(output_format: str, filename: str, output: List[str],
                 at_least_one_found: bool, no_one_found: bool) -> None:
    if at_least_one_found and output:
        print(filename)
    elif no_one_found and not output:
        print(filename)
    elif not at_least_one_found and not no_one_found:
        for print_output in output:
            print(output_format.format(print_output))


def find_pattern(counting_mode: bool, lines: List[str], pattern: Pattern[str], fullmatch: bool,
                 invert_result: bool) -> List[str]:
    result = [line for line in lines if invert_result ^
              find_pattern_in_line(pattern, line, fullmatch)]
    if counting_mode:
        return [str(len(result))]
    else:
        return result


def strip_lines(file: Iterable[str]) -> List[str]:
    return [line.rstrip('\n') for line in file]


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='counting_mode', action='store_true')
    parser.add_argument('-E', dest='regex_mode', action='store_true')
    parser.add_argument('-i', dest='ignore_case', action='store_true')
    parser.add_argument('-v', dest='invert_result', action='store_true')
    parser.add_argument('-x', dest='fullmatch', action='store_true')
    parser.add_argument('-l', dest='at_least_one_found', action='store_true')
    parser.add_argument('-L', dest='no_one_found', action='store_true')

    args = parser.parse_args(args_str)
    print_file_name = len(args.files) > 1
    pattern = cast_to_regex(args.regex_mode, args.ignore_case, args.pattern)
    files_content: Dict[str, List[str]] = {}
    if args.files:
        for filename in args.files:
            if not os.path.exists(filename):
                "File {} doesn't exist".format(filename)
            else:
                with open(filename, 'r') as input_file:
                    files_content[filename] = strip_lines(input_file)
    else:
        files_content[''] = strip_lines(sys.stdin)

    for filename, lines_from_file in files_content.items():
        lines_from_file = find_pattern(args.counting_mode, lines_from_file,
                                        pattern, args.fullmatch, args.invert_result)
        print_format = format_data(print_file_name, filename)
        print_result(print_format, filename, lines_from_file,
                     args.at_least_one_found, args.no_one_found)


if __name__ == '__main__':
    main(sys.argv[1:])
