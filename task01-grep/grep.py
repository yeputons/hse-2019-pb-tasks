#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def get_list(regx: bool, inv: bool, sub: bool, ignore: bool, print_found: bool,
             print_not_found: bool, file_name: str, needle: str, fin):
    if not (print_not_found or print_found):
        return [line.rstrip('\n') for line in fin if find(regx, inv, sub, ignore, needle, line)]
    found = False
    for line in fin:
        if find(regx, inv, sub, ignore, needle, line):
            found = True
    if print_found and found or print_not_found and not found:
        return file_name
    return None


def find(regx: bool, inv: bool, sub: bool, ignore: bool, needle: str, line: str):
    if ignore and regx:
        return re.search(needle, line, re.IGNORECASE) != inv
    if ignore:
        needle = needle.upper()
        line = line.upper()
    if sub:
        return (regx and re.fullmatch(needle, line) or not regx and (needle + '\n') == line) != inv
    return (bool(regx and re.search(needle, line)) or not regx and needle in line) != inv


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
    parser.add_argument('-v', dest='inv', action='store_true')
    parser.add_argument('-x', dest='sub', action='store_true')
    parser.add_argument('-E', dest='regx', action='store_true')
    parser.add_argument('-i', dest='ignore', action='store_true')
    parser.add_argument('-l', dest='print_found', action='store_true')
    parser.add_argument('-L', dest='print_not_found', action='store_true')
    return parser.parse_args(args_str)


def main(args_str: List[str]):
    args = create_parser(args_str)
    num_of_files = len(args.files)
    if num_of_files > 0:
        for file_name in args.files:
            with open(file_name, 'r') as fin:
                list_of_lines = get_list(args.regx, args.inv,
                                         args.sub, args.ignore, args.print_found,
                                         args.print_not_found, file_name, args.needle, fin)
                if isinstance(list_of_lines, str) and (args.print_found or args.print_not_found):
                    print(list_of_lines)
                elif list_of_lines:
                    prefix = file_name + ':' if num_of_files > 1 else ''
                    check_count(args.count, list_of_lines, prefix)
    else:
        list_of_lines = get_list(args.regx, args.inv, args.sub,
                                 args.ignore, False, False, '', args.needle, sys.stdin)
        check_count(args.count, list_of_lines)


if __name__ == '__main__':
    main(sys.argv[1:])
