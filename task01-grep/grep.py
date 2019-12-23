#!/usr/bin/env python3
from typing import List
from typing import Tuple
import sys
import re
import argparse


def count(lines: List[str], regex: bool, pattern: str) -> int:
    res = 0
    for string in lines:
        if regex:
            if re.search(pattern, string):
                res += 1
        else:
            if (pattern in string):
                res += 1
    return res


def search_file(name: str, check: bool, regex: bool, lines: List[str], pattern: str):
    for string in lines:
        if regex:
            if re.search(pattern, string):
                if check:
                    print(name + ':' + string)
                else:
                    print(string)
        else:
            if pattern in string:
                if check:
                    print(name + ':' + string)
                else:
                    print(string)


def file_to_lines(file: str) -> List[str]:
    if file == 'sys.stdin':
        return [line.rstrip('\n') for line in sys.stdin.readlines()]
    with open(file, 'r') as in_file:
        return [line.rstrip('\n') for line in in_file.readlines()]


def files_to_lines(files: List[str]) -> List[Tuple[str, List[str]]]:
    return [(file, file_to_lines(file)) for file in files]


def search_global(files: List[str], regex: bool, pattern: str, count_check: bool):
    f = files_to_lines(files)
    for file, lines in f:
        if count_check:
            if len(f) > 1:
                print(file + ':' + str(count(lines, regex, pattern)))
            else:
                print(count(lines, regex, pattern))
        else:
            search_file(file, len(f) > 1, regex, lines, pattern)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    args = parser.parse_args(args_str)
    if len(args.files) > 0:
        search_global(args.files, args.regex, args.needle, args.count)
    else:
        search_global(['sys.stdin'], args.regex, args.needle, args.count)


if __name__ == '__main__':
    main(sys.argv[1:])