#!/usr/bin/env python3
import io
from typing import List
import sys
import re
import argparse


def print_in_format(file: io.StringIO, second: str, length: int):
    if length > 1:
        print(file.name, ':', second, sep='')
    else:
        print(second)


def search_print_count(needle: str, files: List[io.StringIO], regex: bool, count: bool):
    for file in files:
        number = 0
        for line in file.readlines():
            line = line.strip('\n')
            if (regex and re.search(needle, line)) or (not regex and needle in line):
                if count:
                    number += 1
                else:
                    print_in_format(file, line, len(files))
        if count:
            print_in_format(file, str(number), len(files))


def parser_initialisation() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Print lines/count number of enters in text')
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*', type=argparse.FileType('r'), default=[sys.stdin])
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='c', action='store_true')
    return parser


def extract_args(args_str: List[str]) -> argparse.Namespace:
    parser = parser_initialisation()
    return parser.parse_args(args_str)


def main(args_str: List[str]):
    args = extract_args(args_str)
    search_print_count(args.needle, args.files, args.regex, args.c)


if __name__ == '__main__':
    main(sys.argv[1:])
