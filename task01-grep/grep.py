#!/usr/bin/env python3
from argparse import ArgumentParser
from typing import List
import sys
import re
import argparse


def print_files(files: List[str], file: str, line: str) -> None:
    if len(files) > 1:
        print(f'{file}:{line}')
    else:
        print(f'{line}')


def search_files(files: List[str], pattern: str, counter: bool, regex: bool) -> None:
    for file in files:
        cnt = 0
        with open(file, 'r') as in_file:
            for line in in_file.readlines():
                line = line.rstrip('\n')
                if not regex:
                    if pattern in line and not counter:
                        print_files(files, file, line)
                    if pattern in line and counter:
                        cnt += 1
                else:
                    if re.search(pattern, line) and not counter:
                        print_files(files, file, line)
                    if re.search(pattern, line) and counter:
                        cnt += 1
        if counter and len(files) > 1:
            print(f'{file}:{cnt}')
        elif counter:
            print(f'{cnt}')


def search_std(pattern: str, counter: bool, regex: bool) -> None:
    cnt = 0
    for line in sys.stdin.readlines():
        line = line.rstrip('\n')
        if not regex:
            if pattern in line and not counter:
                print(f'{line}')
            if pattern in line and counter:
                cnt += 1
        else:
            if re.search(pattern, line) and not counter:
                print(f'{line}')
            if re.search(pattern, line) and counter:
                cnt += 1
    if counter:
        print(f'{cnt}')


def main(args_str: List[str]):
    parser: ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    args = parser.parse_args(args_str)

    if len(args.files) == 0:
        search_std(args.pattern, args.count, args.regex)
    else:
        search_files(args.files, args.pattern, args.count, args.regex)


if __name__ == '__main__':
    main(sys.argv[1:])