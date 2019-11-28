#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def get_list(regex: bool, inverse: bool, find_substr: bool, ignore_case: bool, print_found: bool,
             print_not_found: bool, file_name: str, needle: str, fin):
    if not (print_not_found or print_found):
        return [line.rstrip('\n') for line in fin if find(regex, inverse, find_substr, ignore_case, needle, line)]
    found = False
    for line in fin:
        if find(regex, inverse, find_substr, ignore_case, needle, line):
            found = True
    if print_found and found or print_not_found and not found:
        return file_name
    return None


def find(regex: bool, inverse: bool, find_substr: bool, ignore_case: bool, needle: str, line: str):
    if (ignore_case):
        needle = needle.upper()
        line = line.upper()
    if (find_substr):
        return (regex and re.fullmatch(needle, line) or not regex and (needle + '\n') == line) != inverse
    else:
        return (bool(regex and re.search(needle, line)) or not regex and needle in line) != inverse


def print_list_count(list_of_lines: list, prefix: str = ''):
    print(prefix, len(list_of_lines), sep='')


def print_list(list_of_lines: list, prefix: str = ''):
    for line in list_of_lines:
        print(prefix, line, sep='')


def check_count(count: bool, list_of_lines: list, prefix: str = ''):
    if count:
        print_list_count(list_of_lines, prefix)
    else:
        print_list(list_of_lines, prefix)


def create_parser(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-v', dest='inverse', action='store_true')
    parser.add_argument('-x', dest='find_substr', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-i', dest='ignore_case', action='store_true')
    parser.add_argument('-l', dest='print_found', action='store_true')
    parser.add_argument('-L', dest='print_not_found', action='store_true')
    return parser.parse_args(args_str)


def main(args_str: List[str]):
    args = create_parser(args_str)
    num_of_files = len(args.files)
    if num_of_files > 0:
        for file_name in args.files:
            with open(file_name, 'r') as fin:
                list_of_lines = get_list(args.regex, args.inverse, args.find_substr, args.ignore_case,
                                         args.print_found, args.print_not_found, file_name, args.needle, fin)
                if type(list_of_lines) == str:
                    print(list_of_lines)
                elif list_of_lines:
                    prefix = file_name + ':' if num_of_files > 1 else ''
                    check_count(args.count, list_of_lines, prefix)
    else:
        list_of_lines = get_list(args.regex, args.inverse, args.find_substr,
                                 args.ignore_case, False, False, '', args.needle, sys.stdin)
        check_count(args.count, list_of_lines)


if __name__ == '__main__':
    main(sys.argv[1:])
