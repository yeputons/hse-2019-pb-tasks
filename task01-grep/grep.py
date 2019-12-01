#!/usr/bin/env python3
from typing import List
from typing import IO
import sys
import re
import argparse

"""
# This function searches for the key line in one file
# that was given to it and returns a List of lines (type str)
# that contain that key line or the List of lines (type str)
# that do not contain it
"""


def find_in_file(regex: bool, invert: bool, ignore_case: bool, exact: bool,
                 f: IO, key: str):
    answ: List[str] = []
    for line in f.readlines():
        line = line.rstrip('\n')
        if not ignore_case:
            is_exact: bool = (not regex and line == key) or \
                       (regex and re.fullmatch(key, line))
        else:
            is_exact: bool = (not regex and line.lower() == key.lower()) or \
                       (regex and re.fullmatch(key, line, re.IGNORECASE))
        line2 = line
        if ignore_case:
            key = key.lower()
            line = line.lower()
        is_researched: bool = (regex and re.search(key, line))
        is_not_researched: bool = (regex and not re.search(key, line))
        is_in_line: bool = (not regex and key in line)
        is_not_in_line: bool = (not regex and not (key in line))
        if ((not invert) and (exact and is_exact)) or \
                (invert and (exact and not is_exact)) or \
                (((not invert) and is_researched) or
                 (invert and is_not_researched)) or \
                (((not invert) and is_in_line) or
                 (invert and is_not_in_line)):
            answ.append(line2)
    return answ


"""
# This function prints a file name or a list of answer strings in requested
# format according to the keys given.
# This function has no return value
"""


def print_in_format(count: bool, form: bool,
                    only_names_with: bool, only_names_without: bool,
                    answ: List[str], f: str):
    tmp = len(answ)
    not_empty = tmp > 0
    if only_names_with and not_empty:
        print(f)
        return
    if only_names_with and not not_empty:
        return
    if only_names_without and not not_empty:
        print(f)
        return
    if only_names_without and not_empty:
        return
    if count:
        answ.clear()
        answ.append(str(tmp))
    for l in answ:
        if form:
            print(f'{f}:', end='')
        print(l)


"""
# This function searches for the key line through the list if files
# and prints an information about them in requested format
# using function print_in_format.
# This function has no return value
"""


def files_search(regex: bool, count: bool, invert: bool,
                 ignore_case: bool, exact: bool,
                 only_names_with: bool, only_names_without: bool,
                 files: List[str], key: str):
    form = len(files) > 1
    for f in files:
        with open(f, 'r') as in_file:
            answ = find_in_file(regex, invert, ignore_case, exact,
                                in_file, key)
            print_in_format(count, form, only_names_with, only_names_without,
                            answ, f)


"""
# This function searches for the key line in the console input
# and prints them or prints an amount of them if variable count is True.
# This function has no return value
"""


def online_search(regex: bool, count: bool, invert: bool,
                  ignore_case: bool, exact: bool,
                  key: str):
    answ = find_in_file(regex, invert, ignore_case, exact, sys.stdin, key)
    if count:
        print(len(answ))
    else:
        for l in answ:
            print(l)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-l', dest='only_names_with', action='store_true')
    parser.add_argument('-L', dest='only_names_without', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-i', dest='ignore_case', action='store_true')
    parser.add_argument('-v', dest='invert', action='store_true')
    parser.add_argument('-x', dest='exact', action='store_true')
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    args = parser.parse_args(args_str)

    if args.files:
        files_search(args.regex, args.count, args.invert,
                     args.ignore_case, args.exact,
                     args.only_names_with, args.only_names_without,
                     args.files, args.needle)
    else:
        online_search(args.regex, args.count, args.invert,
                      args.ignore_case, args.exact,
                      args.needle)


if __name__ == '__main__':
    main(sys.argv[1:])
