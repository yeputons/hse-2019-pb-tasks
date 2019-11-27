#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def condition_find(invert: bool, full_str: bool, test_str, pattern):
    if not invert:
        if full_str:
            return pattern.fullmatch(test_str)
        else:
            return pattern.search(test_str)
    else:
        if full_str:
            return not pattern.fullmatch(test_str)
        else:
            return not pattern.search(test_str)


# Returns list of lines from file which contain needle
def find(full_str: bool, register: bool, invert: bool, regex: bool, needle: str, in_file) -> list:
    if not regex:
        needle = re.escape(needle)
    if register:
        pattern = re.compile(needle, re.IGNORECASE)
    else:
        pattern = re.compile(needle)
    return [line.rstrip('\n') for line in in_file.readlines()
            if condition_find(invert, full_str, line.rstrip('\n'), pattern)]


# Determines the output format depending on the number of files
def format_write(files, found_str, key) -> str:
    if len(files) > 1:
        return str('{}:{}'.format(key, len(found_str[key])))
    else:
        return str(len(found_str[key]))


# Outputting the result in a format dependent on the key [-c]
def write(names_has: bool, names_has_not: bool, files: list, count: bool, found_str: dict):
    for key in found_str.keys():
        if count:
            print(format_write(files, found_str, key), end='\n')
        else:
            if names_has:
                if found_str[key]:
                    print(key)
            elif names_has_not:
                if not found_str[key]:
                    print(key)
            elif len(files) > 1:
                for j in found_str[key]:
                    print('{}:{}'.format(key, j))
            else:
                print('\n'.join(found_str[key]))


# Parser strings for the required substring, files and values for keys:
# [-E] - regular expression
# [-c] - output the number of suitable substrings
def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-i', dest='register', action='store_true')
    parser.add_argument('-v', dest='invert', action='store_true')
    parser.add_argument('-x', dest='full_str', action='store_true')
    parser.add_argument('-l', dest='names_has', action='store_true')
    parser.add_argument('-L', dest='names_has_not', action='store_true')
    args = parser.parse_args(args_str)

    found_str = dict()
    if len(args.files) > 0:
        for line in args.files:
            with open(line, 'r') as open_file:
                found_str[open_file.name] = find(args.full_str, args.register, args.invert,
                                                 args.regex, args.needle, open_file)
    else:
        found_str[str(sys.stdin)] = find(args.full_str, args.register, args.invert,
                                         args.regex, args.needle, sys.stdin)
        args.files.append(sys.stdin)

    write(args.names_has, args.names_has_not, args.files, args.count, found_str)


if __name__ == '__main__':
    main(sys.argv[1:])
