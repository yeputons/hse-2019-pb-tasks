#!/usr/bin/env python3
import io
from typing import List
import sys
import re
import argparse


# Print when -l or -L flags are not given
def print_in_format(chosen_files: List[str], length: int, count: bool, file: io.StringIO):
    if count:
        if length > 1:
            print(file.name, ':', len(chosen_files), sep='')
        else:
            print(len(chosen_files))
    elif length > 1:
        for files in chosen_files:
            print(files[0], ':', files[1], sep='')
    else:
        for files in chosen_files:
            print(files[1])


# Verifying that needle can be found in line
def search(needle: str, line: str, regex: bool, ignore_register: bool, full_match: bool) -> bool:
    if not regex:
        needle = re.escape(needle)
    if ignore_register:
        needle = needle.lower()
        line = line.lower()
    if full_match:
        return bool(re.fullmatch(needle, line))
    return bool(re.search(needle, line))


# Print when -l or -L flags are given
def l_format(chosen_files: List[str]):
    files: List[str] = []
    for line in chosen_files:
        if line[0] not in files:
            files.append(line[0])
    for line in files:
        print(line)


# General function in which format of printing is decided
def print_result(not_chosen_files: List[str], chosen_files: List[str], l1_format: bool,
                 l2_format: bool, length: int, count: bool, file: io.StringIO):
    if l1_format:
        l_format(chosen_files)
    elif l2_format:
        l_format(not_chosen_files)
    else:
        print_in_format(chosen_files, length, count, file)


# Append found line to list with results
def append_to_list(chosen_files, line: str, length: int, file: io.StringIO):
    if length > 1:
        chosen_files.append([file.name, line])
    else:
        chosen_files.append(['sys.stdin', line])


# Principal function in which all the files are processed
def process(needle: str, files: List[io.StringIO], regex: bool, count: bool,
            ignore_register: bool, invert: bool, full_match: bool,
            l1_format: bool, l2_format: bool):
    for file in files:
        not_chosen_files: List[str] = []
        chosen_files: List[str] = []
        for line in file.readlines():
            line = line.strip('\n')
            if search(needle, line, regex, ignore_register, full_match):
                if invert:
                    append_to_list(not_chosen_files, line, len(files), file)
                else:
                    append_to_list(chosen_files, line, len(files), file)
            else:
                if invert:
                    append_to_list(chosen_files, line, len(files), file)
                else:
                    append_to_list(not_chosen_files, line, len(files), file)
        print_result(not_chosen_files, chosen_files, l1_format, l2_format, len(files), count, file)
    for file in files:
        file.close()


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
