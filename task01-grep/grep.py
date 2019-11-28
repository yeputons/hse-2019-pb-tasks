#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def parse_arguments(arguments: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    return parser.parse_args(arguments)


def create_ans_list(needle: str, search_lines: List[str], is_regex: bool) -> List[str]:
    """
    Returns a list with lines
    which contain a string or a regex needle.
    """
    needle_lines = []
    for line in search_lines:
        line = line.rstrip('\n')
        if is_regex:
            if re.search(needle, line):
                needle_lines.append(line)
        elif needle in line:
            needle_lines.append(line)
    return needle_lines


def print_output(ans_list: List[str], is_count: bool, prefix: str):
    """
    List output containing lines
    with string or regex needle
    or that list length output.
    """
    if is_count:
        print(prefix, len(ans_list), sep='')
    else:
        for answer in ans_list:
            print(prefix, answer, sep='')


def work_with_file(file, prefix, needle: str, is_regex, is_count: bool):
    """
    Single file processing
    with file's lines input
    and files lines output
    witch contain string or regex needle
    or a number of that lines.
    """
    with open(file, 'r') as in_file:
        input_lines = [s for s in in_file.readlines()]
        print_output(create_ans_list(needle, input_lines, is_regex),
                     is_count,
                     prefix)


def main(args_str: List[str]):
    """
    The designated start of the program.
    Depending on the number of input files,
    starts functions for working with files
    or functions for working with standard input.
    """
    args = parse_arguments(args_str)
    if len(args.files) > 1:
        for file in args.files:
            work_with_file(file, file + ':', args.needle, args.regex, args.count)
    elif len(args.files) == 1:
        work_with_file(args.files[0], '', args.needle, args.regex, args.count)
    else:
        input_lines = [s for s in sys.stdin.readlines()]
        print_output(create_ans_list(args.needle, input_lines, args.regex),
                     args.count,
                     '')


if __name__ == '__main__':
    main(sys.argv[1:])
