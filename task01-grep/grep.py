#!/usr/bin/env python3
from typing import List
from typing import TextIO
import sys
import re
import argparse


def re_search_modifier(line: str, needle: str, match: bool,
                       ignore_case: bool, inverse: bool) -> bool:
    flags = 0
    if ignore_case:
        flags = re.IGNORECASE
    if match:
        reg = re.fullmatch
    else:
        reg = re.search
    search_result = reg(needle, line, flags=flags) is not None
    if inverse:
        return not search_result
    return search_result


def substring_search_modifier(line: str, needle: str, match: bool,
                              ignore_case: bool, inverse: bool) -> bool:
    if ignore_case:
        line = line.lower()
        needle = needle.lower()
    if match:
        search_result = (line == needle)
    else:
        search_result = needle in line
    if inverse:
        return not search_result
    return search_result


def printer_modifier(file_name: str, number_of_file: int, count: bool,
                     is_file: bool, counter: int, line: str) -> None:
    if count:
        print_result(file_name, number_of_file, str(counter))
    elif is_file:
        print_result(file_name, 0, file_name)
    else:
        print_result(file_name, number_of_file, line)


def print_result(file_name: str, number_of_file: int, output: str) -> None:
    if number_of_file <= 1:
        print(output)
    else:
        print(f'{file_name}:{output}')


def read(in_file: TextIO, args: argparse.Namespace, file_name: str) -> None:
    correct_line = 0
    for line in in_file.readlines():
        line = line.rstrip('\n')
        if args.regex:
            is_correct = re_search_modifier(line, args.needle,
                                            args.match, args.ignore_case, args.inverse)
        else:
            is_correct = substring_search_modifier(line, args.needle,
                                                   args.match, args.ignore_case, args.inverse)
        if is_correct:
            correct_line += 1
        if not (args.is_file or args.count) and is_correct:
            printer_modifier(file_name, len(args.files),
                             args.count, args.is_file, correct_line, line)
    if args.is_file and correct_line > 0:
        printer_modifier(file_name, len(args.files),
                         args.count, args.is_file, correct_line, 'stub')
    if args.count:
        printer_modifier(file_name, len(args.files),
                         args.count, args.is_file, correct_line, 'stub')


def open_file(args: argparse.Namespace) -> None:
    for file_name in args.files:
        with open(file_name, 'r') as in_file:
            read(in_file, args, file_name)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-x', dest='match', action='store_true')
    parser.add_argument('-i', dest='ignore_case', action='store_true')
    parser.add_argument('-v', dest='inverse', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-l', dest='is_file', action='store_true')
    parser.add_argument('-L', dest='is_not_file', action='store_true')
    args = parser.parse_args(args_str)
    if args.is_not_file:
        args.is_file = True
        args.inverse = not args.inverse
    if len(args.files) > 0:
        open_file(args)
    else:
        read(sys.stdin, args, 'none_file')


if __name__ == '__main__':
    main(sys.argv[1:])
