#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def has_needle(line: str, needle: str, regex: bool) -> bool:
    if regex:
        return re.search(needle, line) is not None
    else:
        return needle in line


def find_in_file(lines: List[str], needle: str, regex: bool, file_name: str, need_cnt: bool):
    count = 0
    for line in lines:
        line = line.rstrip('\n')
        if has_needle(line, needle, regex):
            if need_cnt:
                count += 1
            else:
                print(file_name, line, sep='')
    if need_cnt:
        print(file_name, count, sep='')


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    args = parser.parse_args(args_str)
    num_files = len(args.files)
    if num_files == 0:
        lines = sys.stdin.readlines()
        find_in_file(lines, args.needle, args.regex, '', args.count)
    else:
        for file in args.files:
            with open(file, 'r') as in_file:
                file_name = '' if num_files == 1 else file + ':'
                lines = in_file.readlines()
                find_in_file(lines, args.needle, args.regex, file_name, args.count)


if __name__ == '__main__':
    main(sys.argv[1:])
