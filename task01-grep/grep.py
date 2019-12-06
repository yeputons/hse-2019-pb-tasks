#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse
from pathlib import Path


def exists_in_line(pattern: str, line: str, is_regex: bool, is_i: bool, is_x: bool) -> bool:
    flags = 0
    if is_i:
        flags |= re.IGNORECASE
        if not is_regex:
            line = line.lower()
            pattern = pattern.lower()
    if is_regex:
        if is_x:
            return bool(re.fullmatch(pattern, line, flags=flags))
        return bool(re.search(pattern, line, flags=flags))
    if is_x:
        return pattern == line
    return pattern in line


def search_in_lines(lines_to_search_from: List[str], is_regex: bool,
                    pattern: str, is_i: bool, is_v: bool, is_x: bool) -> List[str]:
    found_lines: List[str] = []
    not_found_lines: List[str] = []
    for line in lines_to_search_from:
        line = line.rstrip('\n')
        if exists_in_line(pattern, line, is_regex, is_i, is_x):
            found_lines.append(line)
        else:
            not_found_lines.append(line)
    if is_v:
        return not_found_lines
    return found_lines


def print_line(line: str, prefix: str):
    if len(prefix) > 0:
        print(prefix, end='')
    print(line)


def print_results(prefix: str, is_count: bool, found_lines: List[str], is_l: bool,
                  is_big_l: bool):
    if is_count:
        print_line(str(len(found_lines)), prefix)
    elif is_l:
        if len(found_lines) > 0:
            print_line('', prefix)
    elif is_big_l:
        if len(found_lines) == 0:
            print_line('', prefix)
    else:
        for line in found_lines:
            print_line(line, prefix)


def find_pattern(files: List[str], is_count: bool, is_regex: bool,
                 pattern: str, is_i: bool, is_v: bool, is_x: bool, is_l: bool, is_big_l: bool):
    prefix = ''
    found_lines: List[str]
    if len(files) > 0:
        for file_name in files:
            p = Path.cwd()
            file = p.joinpath(file_name)
            if file.exists() and file.is_file():
                with file.open() as in_file:
                    found_lines = search_in_lines(in_file.readlines(),
                                                  is_regex, pattern, is_i, is_v, is_x)
                    if len(files) > 1:
                        prefix = file_name + ':'
                    if is_l or is_big_l:
                        prefix = file_name
                    print_results(prefix, is_count, found_lines, is_l, is_big_l)
            else:
                print(f'Can not open a file:{file_name}. Error has occurred')
    else:
        found_lines = search_in_lines(sys.stdin.readlines(), is_regex, pattern, is_i, is_v, is_x)
        print_results(prefix, is_count, found_lines, is_l, is_big_l)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser(description='searches for "needle" and prints it')
    parser.add_argument('needle', type=str, help='regular expression or str to search')
    parser.add_argument('files', nargs='*', help='files to search from')
    parser.add_argument('-E', dest='regex', action='store_true', help='search regular expression')
    parser.add_argument('-c', action='store_true', help='count')
    parser.add_argument('-i', action='store_true', help='ignorecase')
    parser.add_argument('-v', action='store_true', help='inverse')
    parser.add_argument('-x', action='store_true', help='fullmatch')
    parser.add_argument('-l', action='store_true')
    parser.add_argument('-L', action='store_true')
    args = parser.parse_args(args_str)
    find_pattern(args.files, args.c, args.regex, args.needle, args.i, args.v,
                 args.x, args.l, args.L)


if __name__ == '__main__':
    main(sys.argv[1:])
