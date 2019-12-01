#!/usr/bin/env python3
from typing import List, Dict
import sys
import re
import argparse


def parse_arguments(arguments: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-l', dest='names_only', action='store_true')
    parser.add_argument('-L', dest='inverted_ans_names_only', action='store_true')
    parser.add_argument('-i', dest='ignore_case', action='store_true')
    parser.add_argument('-v', dest='inverted_found', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    return parser.parse_args(arguments)


def create_flags_dict(args: argparse.Namespace) -> Dict:
    """
    Returns a dictionary which contain
    information about flags appearance
    """
    flags = {'c': args.count,
             'E': args.regex,
             'l': args.names_only,
             'L': args.inverted_ans_names_only,
             'i': args.ignore_case,
             'v': args.inverted_found,
             'x': args.full_match}
    return flags


def find_if_desired(flags: Dict, needle, line: str) -> bool:
    """
    Returns True or False depending on
    flags and the presence of needle in line
    """
    if not flags['E']:
        needle = re.escape(needle)
    if flags['i']:
        needle = needle.lower()
        line = line.lower()
    if flags['x']:
        is_desired = re.fullmatch(needle, line)
    else:
        is_desired = re.search(needle, line)
    if flags['v']:
        return not bool(is_desired)
    return bool(is_desired)


def create_ans_list(needle: str, search_lines: List[str], flags: Dict) -> List[str]:
    """
    Returns a list with lines
    which contain a string or a regex needle.
    """
    needle_lines = []
    for line in search_lines:
        line = line.rstrip('\n')
        if find_if_desired(flags, needle, line):
            needle_lines.append(line)
    return needle_lines


def print_output(ans_list: List[str], flags: Dict, prefix: str):
    """
    List output containing lines
    with string or regex needle
    or that list length output.
    """
    if flags['c']:
        print(prefix, len(ans_list), sep='')
    else:
        for answer in ans_list:
            print(prefix, answer, sep='')


def print_file_name(flags: Dict, file_name: str, is_found: int):
    """
    Print name of file which contain
    or not contain desired lines
    """
    if flags['L'] and not is_found or flags['l'] and is_found:
        print(file_name)


def work_with_file(file, prefix, needle: str, flags: Dict):
    """
    Single file processing
    with file's lines input
    and files lines or file name output
    which contain string or regex needle
    or a number of that lines.
    """
    with open(file, 'r') as in_file:
        input_lines = in_file.readlines()
        ans_list = create_ans_list(needle, input_lines, flags)
        if flags['L'] or flags['l']:
            print_file_name(flags, file, len(ans_list))
            return
        print_output(ans_list, flags, prefix)


def main(args_str: List[str]):
    """
    The designated start of the program.
    Depending on the number of input files,
    starts functions for working with files
    or functions for working with standard input.
    """
    args = parse_arguments(args_str)
    flags = create_flags_dict(args)
    if len(args.files) > 1:
        for file in args.files:
            work_with_file(file, file + ':', args.needle, flags)
    elif len(args.files) == 1:
        work_with_file(args.files[0], '', args.needle, flags)
    else:
        input_lines = sys.stdin.readlines()
        print_output(create_ans_list(args.needle, input_lines, flags),
                     flags,
                     '')


if __name__ == '__main__':
    main(sys.argv[1:])
