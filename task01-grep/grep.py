#!/usr/bin/env python3
from typing import List
from typing import TextIO
import sys
import re
import argparse
import copy


def format_lines(filename: str, needle: str, input_type: TextIO,
                 count: bool, add_filenames: bool, ignore_register: bool,
                 inverse: bool, file_with: bool, accuracy: bool, regex: bool) -> None:
    lines_without_line_break = [
        line.rstrip('\n') for line in input_type]
    if ignore_register:
        ignoring_register = [
            line.lower() for line in lines_without_line_break]
        needle = needle.lower()
        lines_without_line_break = copy.deepcopy(ignoring_register)
    matching_lines = [
        line for line in lines_without_line_break if re.search(
            needle, line)]
    not_matching_lines = [
        line for line in lines_without_line_break if not re.search(
            needle, line)]
    if regex and accuracy:
        lines_for_x = [
            line for line in lines_without_line_break if (
                needle == line)]
        matching_lines = copy.deepcopy(lines_for_x)
    if not regex and accuracy:
        lines_for_x_without_regex = [
            line for line in lines_without_line_break if re.fullmatch(
                needle, line)]
        matching_lines = copy.deepcopy(lines_for_x_without_regex)
    if inverse:
        matching_lines = copy.deepcopy(not_matching_lines)
    files_output(filename, matching_lines, count, add_filenames, file_with)


def files_output(filename: str, matching_lines: list,
                 count: bool, add_filenames: bool, file_with: bool) -> list:
    lines = [str(len(matching_lines))] if count else matching_lines
    if add_filenames:
        if not file_with:
            for line in lines:
                print(f'{filename}:{line}')
        else:
            print(f'{filename}')
    else:
        for line in lines:
            print(f'{line}')
    return lines


def main(args_str: List[str]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-i', dest='ignore', action='store_true')
    parser.add_argument('-v', dest='inverse', action='store_true')
    parser.add_argument('-l', dest='file_with', action='store_true')
    parser.add_argument('-L', dest='file_without', action='store_true')
    parser.add_argument('-x', dest='accuracy', action='store_true')
    args = parser.parse_args(args_str)

    # STUB BEGINS
    if args.file_without:
        args.file_with = True
        args.inverse = True
    needle = args.needle if args.regex else re.escape(args.needle)
    add_filenames = len(args.files) > 1
    if args.files:
        for filename in args.files:
            with open(filename, 'r') as in_file:
                format_lines(
                    filename, needle, in_file, args.count, add_filenames, args.ignore,
                    args.inverse, args.file_with, args.accuracy, args.regex)
    else:
        format_lines('', needle, sys.stdin, args.count, add_filenames,
                     args.ignore, args.inverse, args.file_with, args.accuracy, args.regex)


if __name__ == '__main__':
    main(sys.argv[1:])
