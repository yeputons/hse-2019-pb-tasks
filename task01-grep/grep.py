#!/usr/bin/env python3
from typing import List
from typing import Tuple
import sys
import re
import argparse


def has_needle(line: str, needle: str, regex: bool,
               ignore_case: bool, inverted: bool, full_match: bool) -> bool:
    if regex:
        if ignore_case:
            needle = re.compile(needle, re.IGNORECASE)
        else:
            needle = re.compile(needle)
        if full_match:
            search = re.fullmatch
        else:
            search = re.search
        result = search(needle, line) is not None
    else:
        if ignore_case:
            needle = needle.lower()
            line = line.lower()
        if full_match:
            result = needle == line
        else:
            result = needle in line
    return result ^ inverted


def find_in_file(lines: List[str], needle: str, regex: bool, ignore_case: bool,
                 inverted: bool, full_match: bool) -> List[str]:
    result = []
    for line in lines:
        line = line.rstrip('\n')
        if has_needle(line, needle, regex, ignore_case, inverted, full_match):
            result.append(line)
    return result


def print_res(result: List[Tuple[str, List[str]]], count: bool, only_files: bool, is_stdin: bool):
    for file_name, lines in result:
        if not is_stdin and not only_files and len(result) > 1:
            file_name += ':'
        if count:
            print(file_name, len(lines), sep='')
        elif only_files:
            print(file_name)
        else:
            for line in lines:
                print(file_name, line, sep='')


def parse_arguments(args_str: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-i', dest='ignore_case', action='store_true')
    parser.add_argument('-v', dest='inverted', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    parser.add_argument('-l', dest='only_files', action='store_true')
    parser.add_argument('-L', dest='only_not_files', action='store_true')
    return parser.parse_args(args_str)


def main(args_str: List[str]):
    args = parse_arguments(args_str)
    num_files = len(args.files)
    if num_files == 0:
        lines = sys.stdin.readlines()
        found = find_in_file(lines, args.needle, args.regex, args.ignore_case,
                             args.inverted, args.full_match)
        result = [('', found)]
        print_res(result, args.count, False, True)
    else:
        result = []
        for file in args.files:
            with open(file, 'r') as in_file:
                file_name = '' if num_files == 1 else file
                lines = in_file.readlines()
                found = find_in_file(lines, args.needle, args.regex,
                                     args.ignore_case, args.inverted, args.full_match)
                if args.only_files and found:
                    result.append((file_name, found))
                if args.only_not_files and not found:
                    result.append((file_name, found))
                if not args.only_files and not args.only_not_files:
                    result.append((file_name, found))
        print_res(result, args.count, args.only_files or args.only_not_files, False)


if __name__ == '__main__':
    main(sys.argv[1:])
