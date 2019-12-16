#!/usr/bin/env python3
from typing import List
from typing import Tuple
import sys
import re
import argparse


def has_needle(line: str, needle: str, regex: bool,
               ignore_case: bool, inverted: bool, full_match: bool) -> bool:
    if not regex:
        needle = re.escape(needle)
    re_needle = re.compile(needle, re.IGNORECASE if ignore_case else 0)
    search = re.fullmatch if full_match else re.search
    result = search(re_needle, line) is not None
    return result ^ inverted


def find_in_file(lines: List[str], needle: str, regex: bool, ignore_case: bool,
                 inverted: bool, full_match: bool) -> List[str]:
    result = []
    for line in lines:
        line = line.rstrip('\n')
        if has_needle(line, needle, regex, ignore_case, inverted, full_match):
            result.append(line)
    return result


def print_res(result: List[Tuple[str, List[str]]], count: bool,
              only_files: bool, only_not_files: bool, one_file: bool):
    for file_name, lines in result:
        if only_files:
            if lines:
                print(file_name)
            continue
        if only_not_files:
            if not lines:
                print(file_name)
            continue
        if one_file:
            file_name = ''
        else:
            file_name += ':'
        if count:
            print(file_name, len(lines), sep='')
        else:
            for line in lines:
                print(file_name, line, sep='')


def read_input(files: List[str], normal_search: bool) -> Tuple[List[Tuple[str, List[str]]], bool]:
    lines = []
    num_files = len(files)
    one_file = normal_search and num_files <= 1
    if num_files == 0:
        lines.append(('', sys.stdin.readlines()))
    else:
        for file in files:
            with open(file, 'r') as in_file:
                lines.append((file, in_file.readlines()))
    return lines, one_file


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
    normal_search = not (args.only_files or args.only_not_files)
    lines, one_file = read_input(args.files, normal_search)
    result = []
    for file_name, line in lines:
        found = find_in_file(line, args.needle, args.regex,
                             args.ignore_case, args.inverted, args.full_match)
        result.append((file_name, found))
    print_res(result, args.count, args.only_files, args.only_not_files, one_file)


if __name__ == '__main__':
    main(sys.argv[1:])
