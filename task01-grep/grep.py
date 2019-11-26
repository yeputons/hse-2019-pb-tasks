#!/usr/bin/env python3
from typing import List
from typing import TextIO
import sys
import re
import argparse


def to_find_reg(line: str, needle: str) -> bool:
    return re.search(needle, line) is not None


def to_find_substring(line: str, needle: str) -> bool:
    return needle in line


def to_find(line: str, needle: str, regex: bool) -> bool:
    if regex:
        return to_find_reg(line, needle)
    else:
        return to_find_substring(line, needle)


def print_result(file_name: str, number_of_file: int, output: str) -> None:
    if number_of_file <= 1:
        print(output)
    else:
        print(f'{file_name}:{output}')


def counter(in_file: TextIO, args: argparse.Namespace, file_name: str) -> None:
    line_counter = 0
    for line in in_file.readlines():
        line = line.rstrip('\n')
        if to_find(line, args.needle, args.regex):
            line_counter += 1
    print_result(file_name, len(args.files), str(line_counter))


def string_finder(in_file: TextIO, args: argparse.Namespace, file_name: str) -> None:
    for line in in_file.readlines():
        line = line.rstrip('\n')
        if to_find(line, args.needle, args.regex):
            print_result(file_name, len(args.files), line)


def finder(in_file: TextIO, args: argparse.Namespace, file_name: str) -> None:
    if not args.count:
        string_finder(in_file, args, file_name)
    else:
        counter(in_file, args, file_name)


def file_read(args: argparse.Namespace) -> None:
    for file_name in args.files:
        with open(file_name, 'r') as in_file:
            finder(in_file, args, file_name)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    args = parser.parse_args(args_str)
    if len(args.files) > 0:
        file_read(args)
    else:
        finder(sys.stdin, args, 'none_file')


if __name__ == '__main__':
    main(sys.argv[1:])
