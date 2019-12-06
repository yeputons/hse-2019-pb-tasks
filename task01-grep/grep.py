#!/usr/bin/env python3
from typing import List, Pattern
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


def full_find_pattern(pattern: Pattern[str], line: str, is_full: bool) -> bool:
    if is_full:
        return bool(re.fullmatch(pattern, line))
    return bool(re.search(pattern, line))


def filter_lines(lines: List[str], compiled_pattern: Pattern[str],
                 is_invert: bool, is_full: bool) -> List[str]:
    return list(filter(lambda line:
                       is_invert ^ full_find_pattern(compiled_pattern, line, is_full), lines))


def format_output(file_name: str, output_storage: str, is_many: bool) -> str:
    print_format = '{}'
    if is_many:
        print_format = '{0}:{1}'.format(file_name, output_storage)
    return print_format


def print_output(out: List[str], is_many: bool, file_name: str) -> None:
    for line in out:
        print(format_output(file_name, line, is_many).format(line))


def print_with_flags(file_name: str, counter: int,
                     is_counter: bool, is_many: bool, is_found: bool, is_not_found: bool) -> None:
    if is_counter:
        print(format_output(file_name, str(counter), is_many).format(str(counter)))
    elif (is_found and counter > 0) or (is_not_found and counter == 0):
        print(file_name)


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

    is_many = len(args.files) > 1

    compiled_pattern = compile_pattern(args.pattern, args.ignore, args.regex)

    for file in args.files:

        src = read_files(file) if exist_file else strip_lines(sys.stdin.readlines())

        filtered_lines = filter_lines(src, compiled_pattern, args.invert, args.full)

        counter = len(filtered_lines)
        if args.counter or args.found or args.not_found:
            print_with_flags(file, counter, args.counter, is_many, args.found, args.not_found)
        else:
            print_output(filtered_lines, is_many, file)


if __name__ == '__main__':
    main(sys.argv[1:])
