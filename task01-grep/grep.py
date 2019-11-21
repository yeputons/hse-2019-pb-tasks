#!/usr/bin/env python3
from typing import List
from typing import IO
import sys
import re
import argparse


# This function searches for the key line in one file
# that was given to it and returns a List of lines (type str)
# that contain that key line


def find_in_file(regex: bool, f: IO, key: str):
    answ: List[str] = []
    for line in f.readlines():
        line = line.rstrip('\n')
        if regex and re.search(key, line) or not regex and key in line:
            answ.append(line)
    return answ


# This function searches for the key line through the list if files
# and prints them or prints an amount of them if variable count is True.
# This function has no return value


def files_search(regex: bool, count: bool, files: List[str], key: str):
    form = False
    if len(files) > 1:
        form = True
    for f in files:
        with open(f, 'r') as in_file:
            answ = find_in_file(regex, in_file, key)
        if count:
            if form:
                print(f'{f}:', end='')
            print(f'{len(answ)}')
        else:
            for l in answ:
                if form:
                    print(f'{f}:', end='')
                print(l)


# This function searches for the key line in the console input
# and prints them or prints an amount of them if variable count is True.
# This function has no return value


def online_search(regex: bool, count: bool, key: str):
    answ = find_in_file(regex, sys.stdin, key)
    if count:
        print(len(answ))
    else:
        for l in answ:
            print(l)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    args = parser.parse_args(args_str)

    if args.files:
        files_search(args.regex, args.count, args.files, args.needle)
    else:
        online_search(args.regex, args.count, args.needle)


if __name__ == '__main__':
    main(sys.argv[1:])
