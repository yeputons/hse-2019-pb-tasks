#!/usr/bin/env python3
from typing import List, TextIO
import sys
import re
import argparse


def search_needle_in_line(line: str, needle='', regex=False, ignore=False, full_match=False,
                          inverse=False) -> bool:
    if not regex:
        needle = re.escape(needle)

    ignore = re.IGNORECASE if ignore else 0

    if full_match:
        res = re.fullmatch(needle, line, flags=ignore) is not None
    else:
        res = re.search(needle, line, flags=ignore) is not None

    if inverse:
        res = not res

    return res


def find_in_file(file: TextIO, args: argparse.Namespace, filename: str = ''):
    line_list = []

    for line in file.readlines():
        line = line.rstrip('\n')
        if search_needle_in_line(line, needle=args.needle, regex=args.regex, ignore=args.ignore,
                                 full_match=args.full_match, inverse=args.inverse):
            line_list.append(line)

    print_asked_string(line_list, counter=args.counter, no_lines=args.no_lines,
                       has_lines=args.has_lines, files=args.files, filename=filename)


def print_asked_string(line_list: List[str], counter=False,
                       no_lines=False, has_lines=False, files=None, filename=''):
    if files is None:
        files = []
    if counter:
        if len(files) > 1:
            print(f'{filename}:{len(line_list)}')
        else:
            print(len(line_list))
        return
    if no_lines:
        if not line_list:
            print(filename)
        return
    if line_list:
        if has_lines:
            print(filename)
        else:
            for line in line_list:
                print(f'{filename}:{line}' if len(files) > 1 else line)


def read(args_str: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='counter', action='store_true')
    parser.add_argument('-i', dest='ignore', action='store_true')
    parser.add_argument('-v', dest='inverse', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    parser.add_argument('-l', dest='has_lines', action='store_true')
    parser.add_argument('-L', dest='no_lines', action='store_true')

    return parser.parse_args(args_str)


def main(args_str: List[str]):
    args = read(args_str)

    if not args.files:
        find_in_file(sys.stdin, args)

    for filename in args.files:
        with open(filename, 'r') as file:
            find_in_file(file, args, filename)


if __name__ == '__main__':
    main(sys.argv[1:])
