#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def get_list(regex: bool, needle: str, fin):
    return [line.rstrip('\n') for line in fin if find(regex, needle, line)]


def find(regex: bool, needle: str, line: str):
    return regex and re.search(needle, line) or not regex and needle in line


def print_list_count(list_of_lines: list, prefix: str = ''):
    print(prefix, len(list_of_lines), sep='')


def print_list(list_of_lines: list, prefix: str = ''):
    for line in list_of_lines:
        print(prefix, line, sep='')


def create_parser(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    return parser.parse_args(args_str)


def main(args_str: List[str]):
    args = create_parser(args_str)
    num_of_files = len(args.files)

    if num_of_files > 0:
        for file_name in args.files:
            with open(file_name, 'r') as fin:
                list_of_lines = get_list(args.regex, args.needle, fin)
                prefix = file_name + ':' if num_of_files > 1 else ''
                if args.count:
                    print_list_count(list_of_lines, prefix)
                else:
                    print_list(list_of_lines, prefix)
    else:
        list_of_lines = get_list(args.regex, args.needle, sys.stdin)
        if args.count:
            print_list_count(list_of_lines)
        else:
            print_list(list_of_lines)


if __name__ == '__main__':
    main(sys.argv[1:])
