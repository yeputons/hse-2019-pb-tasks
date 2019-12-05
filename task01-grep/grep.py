#!/usr/bin/env python3
from typing import List, TextIO
import sys
import re
import argparse


def search_needle_in_line(line: str, args: argparse.Namespace) -> bool:
    needle = args.needle

    if not args.regex:
        needle = re.escape(needle)

    ignore = re.IGNORECASE if args.ignore else 0

    if args.full_match:
        res = re.fullmatch(needle, line, flags=ignore) is not None
    else:
        res = re.search(needle, line, flags=ignore) is not None

    # possibly double inverse
    if args.no_lines:
        res = not res
    if args.inverse: 
        res = not res

    return res


def find_in_file(file: TextIO, args: argparse.Namespace, filename: str = ''):
    line_list = []

    for line in file.readlines():
        line = line.rstrip('\n')
        if search_needle_in_line(line, args):
            line_list.append(line)

    print_asked_string(line_list, args, filename)


def print_asked_string(line_list: List[str], args: argparse.Namespace, filename: str):
    if args.counter:
        filename += ':' if len(args.files) > 0 else ''
        print(f'{filename}{len(line_list)}')
    elif line_list:
        if args.has_lines or args.no_lines:
            print(filename)
        else:
            for line in line_list:
                print(f'{filename}:{line}' if len(args.files) > 1 else line)




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

    
    if args.files == []:
        find_in_file(sys.stdin, args)

    for filename in args.files:
        with open(filename, 'r') as file:
            find_in_file(file, args, filename)

if __name__ == '__main__':
    main(sys.argv[1:])