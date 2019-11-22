#!/usr/bin/env python3
from typing import List, Callable
import sys
import re
import argparse


def get_required_lines(lines: List[str], check: Callable):
    res = []

    for line in lines:
        if check(line):
            res.append(line)
    return res


def get_file_lines(filename: str) -> List[str]:
    lines = []

    with open(filename, 'r') as in_file:
        for line in in_file:
            lines.append(line.rstrip('\n'))
    return lines


def print_fmt(lines: List[str], line_format: str, file_name: str, count: bool):
    if count:
        print(line_format.format(file_name, len(lines)))
    else:
        for line in lines:
            print(line_format.format(file_name, line))


def get_matching(args: argparse.Namespace) -> Callable:
    flags = 0
    needle = args.needle
    if args.ignore:
        flags |= re.I
    if not args.regex:
        needle = re.escape(needle)
    if args.inverse:
        needle = '^((?!'+ needle + ').)*$'
    #print(needle)
    if args.full_match:
    	return re.compile(needle, flags=flags).fullmatch
    return re.compile(needle, flags=flags).search

def get_format(args: argparse.Namespace) -> str:
    if len(args.files) > 1:
        return '{0}:{1}'
    elif args.has_lines or args.no_lines:
        return '{0}'
    return '{1}'


def parse_args(args_str: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-i', dest='ignore', action='store_true')
    parser.add_argument('-v', dest='inverse', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    parser.add_argument('-l', dest='has_lines', action='store_true')
    parser.add_argument('-L', dest='no_lines', action='store_true')

    return parser.parse_args(args_str)


def main(args_str: List[str]):
    args = parse_args(args_str)

    check = get_matching(args)
    fmt = get_format(args)
    all_lines = []

    if args.files != []:
        for filename in args.files:
            all_lines.append(get_file_lines(filename))
    else:
        all_lines = [list(map(str.rstrip, sys.stdin.readlines()))]
        args.files.append('')

    for lines, file_name in zip(all_lines, args.files):
        print_fmt(get_required_lines(lines, check), fmt, file_name, args.count)


if __name__ == '__main__':
    main(sys.argv[1:])
