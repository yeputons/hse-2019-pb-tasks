#!/usr/bin/env python3
import io
from typing import List
import sys
import re
import argparse


def add_arguments(args_str) -> argparse.Namespace:
    """Return the list of function arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str,
                        help='what PATTERN search in files')
    parser.add_argument('files', nargs='*', default=[sys.stdin],
                        type=argparse.FileType('r'),
                        help='files to look for PATTERN (on default stdin)')
    # Pattern selection and interpretation:
    parser.add_argument('-E', dest='regex', action='store_true',
                        help='PATTERNS are extended regular expressions')
    parser.add_argument('-i', dest='iflag', action='store_true',
                        help='ignore case distinctions')
    parser.add_argument('-x', dest='whole_line', action='store_true',
                        help='force PATTERN to match only whole lines')
    # Miscellaneous:
    parser.add_argument('-v', dest='inversion', action='store_true',
                        help='select non-matching lines')
    # Output control:
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-L', dest='files_without_lines', action='store_true',
                       help='print only names of FILEs with no selected lines')
    group.add_argument('-l', dest='only_names_of_files', action='store_true',
                       help='print only names of FILEs with selected lines')
    group.add_argument('-c', dest='cflag', action='store_true',
                       help='print only a count of selected lines per FILE')
    return parser.parse_args(args_str)


def print_formatted_lines(list_of_lines: List[str], file: io.StringIO, number_of_files: int,
                          files_without_lines: bool, only_names_of_files: bool, cflag: bool):
    """
    Accepts the list of lines to be output.
    if there are more than 1 file, it also displays the file name.
    """
    str_result = ''
    if number_of_files > 1:
        str_result += file.name + ':'
    if cflag:
        print(str_result, len(list_of_lines), sep='')
        return

    if files_without_lines:
        if len(list_of_lines) == 0:
            print(file.name)
        return

    if only_names_of_files:
        if len(list_of_lines) != 0:
            print(file.name)
        return

    for line in list_of_lines:
        print(str_result, line, sep='')


def find_and_print_lines(needle: str, files: List[io.StringIO],
                         regex: bool, whole_line: bool, iflag: bool, inversion: bool,
                         files_without_lines: bool, only_names_of_files: bool, cflag: bool):
    """Find all suitable lines in all files and display them on the screen"""
    for file in files:
        list_of_lines = []
        for line in file.readlines():
            line = line.rstrip('\n')
            if check_line(needle, line, regex, whole_line, iflag, inversion):
                list_of_lines.append(line)
        print_formatted_lines(list_of_lines, file, len(files),
                              files_without_lines, only_names_of_files, cflag)


def check_line(needle: str, line: str,
               regex: bool, whole_line: bool,
               iflag: bool, inversion: bool) -> bool:
    """Checking for needle in the line with all the flags"""
    flags = 0
    if iflag:
        if regex:
            flags = re.IGNORECASE
        else:
            needle = needle.casefold()
            line = line.casefold()

    if whole_line:
        res = (needle == line and not regex) or (regex and bool(re.fullmatch(needle, line, flags)))
    else:
        res = (needle in line and not regex) or (regex and bool(re.search(needle, line, flags)))
    return inversion ^ res


def main(args_str: List[str]):
    args = add_arguments(args_str)
    find_and_print_lines(args.needle, args.files,
                         args.regex, args.whole_line, args.iflag, args.inversion,
                         args.files_without_lines, args.only_names_of_files, args.cflag)
    for file in args.files:
        file.close()


if __name__ == '__main__':
    main(sys.argv[1:])
