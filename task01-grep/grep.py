#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


# Returns list of lines from file which contain needle
def find(regex: bool, needle: str, in_file) -> list:
    if not regex:
        needle = re.escape(needle)
    pattern = re.compile(needle)
    return [line.rstrip('\n') for line in in_file.readlines() if pattern.search(line.rstrip('\n'))]


# Determines the output format depending on the number of files
def format_write(files, found_str, key) -> str:
    if len(files) > 1:
        return str('{}:{}'.format(key, len(found_str[key])))
    else:
        return str(len(found_str[key]))


# Outputting the result in a format dependent on the key [-c]
def write(files: list, count: bool, found_str: dict):
    for key in found_str.keys():
        if count:
            print(format_write(files, found_str, key), end='\n')
        else:
            if len(files) > 1:
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
    args = parser.parse_args(args_str)

    found_str = dict()
    if len(args.files) > 0:
        for line in args.files:
            with open(line, 'r') as open_file:
                found_str[open_file.name] = find(args.regex, args.needle, open_file)
    else:
        found_str[str(sys.stdin)] = find(args.regex, args.needle, sys.stdin)
        args.files.append(sys.stdin)

    write(args.files, args.count, found_str)


if __name__ == '__main__':
    main(sys.argv[1:])
