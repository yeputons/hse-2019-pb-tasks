#!/usr/bin/env python3
import io
from typing import List
import sys
import re
import argparse


# Print when -l or -L flags are not given
def print_in_format(right_files, length: int):
    if length > 1:
        for file in right_files:
            print(file[0], ':', file[1], sep='')
    else:
        for file in right_files:
            print(file[1])


# Print when -c flag is given
def print_in_format_count(length, file, number):
    if length > 1:
        print(file.name, ':', number, sep='')
    else:
        print(number)


# Verifying that needle can be found in line
def search(needle: str, line: str, regex: bool, ignore_register: bool, full_match: bool) -> bool:
    if regex and ignore_register and full_match:
        if re.fullmatch(needle, line, re.IGNORECASE):
            return True
    if regex and ignore_register and not full_match:
        if re.search(needle, line, re.IGNORECASE):
            return True
    if regex and not ignore_register and full_match:
        if re.fullmatch(needle, line):
            return True
    if regex and not ignore_register and not full_match:
        if re.search(needle, line):
            return True
    if not regex and not ignore_register and full_match:
        return needle == line
    if not regex and not ignore_register and not full_match:
        return needle in line
    string = line.lower()
    if not regex and ignore_register and full_match:
        return needle.lower() == string
    if not regex and ignore_register and not full_match:
        return needle.lower() in string
    return False


# Print with -l or -L flags
def l_format(right_files):
    files = []
    for line in right_files:
        if line[0] not in files:
            files.append(line[0])
    for line in files:
        print(line)


# General function in which format of printing is decided
def print_result(not_right_files, right_files, l1_format, l2_format, length: int):
    if l1_format:
        l_format(right_files)
    elif l2_format:
        l_format(not_right_files)
    else:
        print_in_format(right_files, length)


# Append found line either to list with results or to list with not suitable lines
def append_to_list(invert: bool, right_files, not_right_files, line, length, file: io.StringIO):
    if not invert:
        if length > 1:
            right_files.append([file.name, line])
        else:
            right_files.append(['sys.stdin', line])
    else:
        if length > 1:
            not_right_files.append([file.name, line])
        else:
            not_right_files.append(['sys.stdin', line])


# Principal function in which all the files are processed
def process(needle: str, files: List[io.StringIO], regex: bool, count: bool,
            ignore_register: bool, invert: bool, full_match: bool,
            l1_format: bool, l2_format: bool):
    not_right_files = []  # type: List[str]
    right_files = []  # type: List[str]
    for file in files:
        number = 0
        for line in file.readlines():
            line = line.strip('\n')
            if search(needle, line, regex, ignore_register, full_match):
                append_to_list(invert, right_files, not_right_files, line, len(files), file)
                if not invert and count:
                    number += 1
            else:
                append_to_list(not invert, right_files, not_right_files, line, len(files), file)
                if invert and count:
                    number += 1
        if count:
            print_in_format_count(len(files), file, number)
    if not count:
        print_result(not_right_files, right_files, l1_format, l2_format, len(files))


def parser_initialisation() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Print lines/count number of enters in text')
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*', type=argparse.FileType('r'), default=[sys.stdin])
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='c', action='store_true')
    parser.add_argument('-i', dest='i', action='store_true')
    parser.add_argument('-v', dest='v', action='store_true')
    parser.add_argument('-x', dest='x', action='store_true')
    parser.add_argument('-l', dest='l', action='store_true')
    parser.add_argument('-L', dest='L', action='store_true')
    return parser


def extract_args(args_str: List[str]) -> argparse.Namespace:
    parser = parser_initialisation()
    return parser.parse_args(args_str)


def main(args_str: List[str]):
    args = extract_args(args_str)
    process(args.needle, args.files, args.regex, args.c, args.i, args.v, args.x, args.l, args.L)


if __name__ == '__main__':
    main(sys.argv[1:])
