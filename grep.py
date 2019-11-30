#!/usr/bin/env python3

from typing import List, TextIO
import sys
import re
import argparse


def format_input(regex: bool, stdin_or_file: bool, word: str, file: TextIO) -> List[str]:
    lines: List[str] = []
    for line in (sys.stdin if stdin_or_file else file):
        lines = conditions(regex, word, line, lines)
    return lines


def conditions(regex: bool, word: str, line: str, lines: List[str]) -> List[str]:
    line = line.rstrip('\n')
    if regex and re.search(word, line):
        lines.append(line)
    elif word in line:
        lines.append(line)
    return lines


def print_output(file_count: int, lines: List[str], file: str) -> None:
    for line in lines:
        print(line if file_count <= 1 else '{}:{}'.format(file, line))


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*', type=str)
    parser.add_argument('-E', '--regex', action='store_true',
                        help='Write it if you want to find regular expression')
    parser.add_argument('-c', '--count', action='store_true',
                        help='Counting number of strings in file or a'
                             'standard input')
    args = parser.parse_args(args_str)
    ls = []
    for file in args.files:
        with open('{}'.format(file), 'r') as in_file:
            ls = format_input(args.regex, False, args.needle, in_file)
            if args.count:
                ls = ['{}'.format(len(ls))]
            print_output(len(args.files), ls, file)
    if not args.files:
        ls = format_input(args.regex, True, args.needle, '')
        if args.count:
            ls = ['{}'.format(len(ls))]
        print_output(len(args.files), ls, '')


if __name__ == '__main__':
    main(sys.argv[1:])
