#!/usr/bin/env python3
from typing import List, TextIO
import sys
import re
import argparse


def search_needle_in_line(needle, line: str, regex: bool) -> bool:
    if regex:
        return bool(re.search(needle, line))
    else:
        return needle in line


def print_asked_string(line_list: List[str], counter: bool, filename: str):
    if filename != '':
        filename += ':'

    if counter:
        print(filename + str(len(line_list)))
    else:
        for line in line_list:
            print(f'{filename}{line}')


def find_in_file(file: TextIO, needle: str, regex, counter: bool, filename: str = ''):
    line_list = []

    for line in file.readlines():
        line = line.rstrip('\n')
        if search_needle_in_line(needle, line, regex):
            line_list.append(line)

    print_asked_string(line_list, counter, filename)


def read(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='counter', action='store_true')
    return parser.parse_args(args_str)


def main(args_str: List[str]):
    args = read(args_str)

    if args.files == []:
        find_in_file(sys.stdin, args.needle, args.regex, args.counter)

    for filename in args.files:
        with open(filename, 'r') as file:
            if len(args.files) == 1:
                filename = ''
            find_in_file(file, args.needle, args.regex, args.counter, filename)


if __name__ == '__main__':
    main(sys.argv[1:])