# !/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def process(args) -> None:
    if len(args.files) > 0:
        for value in args.files:
            lst_of_strings = read_file(value)
            lst_of_strings = string_processing(lst_of_strings, args.needle, args.regex, args.count)
            lst_of_strings = string_format(value, lst_of_strings, len(args.files))
            printing(lst_of_strings)
    if len(args.files) == 0:
        lst = read_stdin()
        lst = string_processing(lst, args.needle, args.regex, args.count)
        printing(lst)


def read_stdin() -> list:
    lst = list()
    for line in sys.stdin.readlines():
        lst.append(line.rstrip('\n'))
    return lst


def read_file(filename: str) -> list:
    lst = list()
    with open(filename, 'r') as in_file:
        for line in in_file.readlines():
            lst.append(line.rstrip('\n'))
    return lst


def string_processing(lst: list, needle: str, regex: bool, count: bool) -> list:
    lst1 = list()
    for line in lst:
        if regex and re.search(needle, line) or not regex and needle in line:
            lst1.append(line)
    if count:
        lst1 = [len(lst1)]
    return lst1


def string_format(filename: str, lst_of_strings: list, length: int) -> list:
    if length > 1:
        for i, string in enumerate(lst_of_strings):
            lst_of_strings[i] = filename + ':' + str(string)
    return lst_of_strings


def printing(lst: list) -> None:
    for value in lst:
        print(str(value))


def main(args_str: List[str]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    args = parser.parse_args(args_str)
    if args.regex:
        args.needle = re.compile(args.needle)
    process(args)


if __name__ == '__main__':
    main(sys.argv[1:])
