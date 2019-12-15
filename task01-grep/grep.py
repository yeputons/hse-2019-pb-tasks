#!/usr/bin/env python3
from typing import List, Pattern, Optional
import sys
import re
import argparse
import os.path


def strip_lines(lines: List[str]) -> List[str]:
    return [line.rstrip('\n') for line in lines]


def read_files(file_name: str) -> List[str]:
    with open(file_name, 'r') as input_file:
        lines = strip_lines(input_file.readlines())
    return lines


def find_pattern(pattern: Pattern[str], line: str, full_match_required: bool) -> bool:
    if full_match_required:
        return bool(re.fullmatch(pattern, line))
    return bool(re.search(pattern, line))


def filter_lines(lines: List[str], compiled_pattern: Pattern[str],
                 is_invert: bool, full_match_required: bool) -> List[str]:
    return [line for line in lines
            if is_invert ^ find_pattern(compiled_pattern, line, full_match_required)]


def format_output(file_name: str, output_storage: Optional[str], require_prefix: bool) -> str:
    print_format = '{}'.format(output_storage)
    if require_prefix:
        print_format = '{}:'.format(file_name) + print_format
    return print_format


def print_output(out: List[str], require_prefix: bool, file_name: str) -> None:
    for line in out:
        print_format = format_output(file_name, line, require_prefix)
        print(print_format)


def format_with_flags(file_name: str, counter: int, is_counter: bool,
                      require_prefix: bool, is_found: bool, is_not_found: bool) -> str:
    print_format = ''
    if is_counter:
        print_format = format_output(file_name, str(counter), require_prefix)
    elif (is_found and counter > 0) or (is_not_found and counter == 0):
        print_format = '{}'.format(file_name)
    return print_format


def print_with_flags(file_name: str, counter: int, is_counter: bool,
                     require_prefix: bool, is_found: bool, is_not_found: bool) -> None:
    print_format = format_with_flags(file_name,
                                     counter, is_counter, require_prefix, is_found, is_not_found)
    if not print_format == '':
        print(print_format)


def existing_files(input_files: List[str]) -> int:
    if not input_files:
        input_files.append('sys.stdin')
    else:
        for file in input_files:
            if not os.path.exists(file):
                print(f"File {file} doesn't exist")
                return 1
    return 0


def compile_pattern(pattern: str, is_ignore: bool, is_regex: bool) -> Pattern[str]:
    flag = 0
    if is_ignore:
        flag = re.IGNORECASE
    if not is_regex:
        pattern = re.escape(pattern)
    return re.compile(pattern, flags=flag)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('-c', dest='counter', action='store_true')
    parser.add_argument('-l', dest='found', action='store_true')
    parser.add_argument('-L', dest='not_found', action='store_true')
    parser.add_argument('-i', dest='ignore', action='store_true')
    parser.add_argument('-v', dest='invert', action='store_true')
    parser.add_argument('-x', dest='full', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('files', nargs='*')
    args = parser.parse_args(args_str)

    exist_file = len(args.files) > 0

    if existing_files(args.files) != 0:
        return

    require_prefix = len(args.files) > 1

    compiled_pattern = compile_pattern(args.pattern, args.ignore, args.regex)

    for file in args.files:

        src = read_files(file) if exist_file else strip_lines(sys.stdin.readlines())

        filtered_lines = filter_lines(src, compiled_pattern, args.invert, args.full)

        counter = len(filtered_lines)
        if args.counter or args.found or args.not_found:
            print_with_flags(file, counter,
                             args.counter, require_prefix, args.found, args.not_found)
        else:
            print_output(filtered_lines, require_prefix, file)


if __name__ == '__main__':
    main(sys.argv[1:])
