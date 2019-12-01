#!/usr/bin/env python3
from typing import List
from typing import Tuple
import sys
import re
import argparse


def cnt(lines: List[str], regex: bool, pattern: str) -> int:
    x = 0
    for string in lines:
        if regex:
            if re.search(pattern, string):
                x += 1
        else:
            if (pattern in string):
                x += 1
    return x


def search(name: str, check: bool, regex: bool, lines: List[str], pattern: str):
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


def redef_file(file: str) -> List[str]:
    if file == 'sys.stdin':
        return [line.rstrip('\n') for line in sys.stdin.readlines()]
    with open(file, 'r') as in_file:
        return [line.rstrip('\n') for line in in_file.readlines()]


def redef_files(files: List[str]) -> List[Tuple[str, List[str]]]:
    return [(file, redef_file(file)) for file in files]


def gsearch(files: List[str], regex: bool, pattern: str, count_check: bool):
    f = redef_files(files)
    for file, lines in f:
        if count_check:
            if len(f) > 1:
                print(file + ':' + str(cnt(lines, regex, pattern)))
            else:
                print(cnt(lines, regex, pattern))
        else:
            search(file, len(f) > 1, regex, lines, pattern)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    args = parser.parse_args(args_str)
    if len(args.files) <= 0:
        gsearch(['sys.stdin'], args.regex, args.needle, args.count)
    else:
        gsearch(args.files, args.regex, args.needle, args.count)




if __name__ == '__main__':
    main(sys.argv[1:])