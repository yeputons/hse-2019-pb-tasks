#!/usr/bin/env python3
from typing import List
from pathlib import Path
import sys
import re
import argparse


def check_line(line: str, pattern: str, is_regex: bool):
    if is_regex:
        return re.search(pattern, line)
    else:
        return pattern in line


def print_lines(lines: List[str], filename: str, print_name: bool, print_number: bool):
    for line in lines:
        if not print_number:
            if print_name:
                print(f'{filename}:{line}')
            else:
                print(line)
        else:
            if print_name:
                print(f'{filename}:{len(lines)}')
                break
            else:
                print(f'{len(lines)}')
                break


def input_from_files(files: List[str], pattern: str, print_number: bool, is_regex: bool):
    lines = []
    print_name = bool(len(files) > 1)
    for filename in files:
        if Path(filename).is_file():
            with open(filename, 'r') as in_file:
                for line in in_file.readlines():
                    line = line.rstrip('\n')
                    if check_line(line, pattern, is_regex):
                        lines.append(f'{line}')
                print_lines(lines, filename, print_name, print_number)
                lines.clear()


def input_from_stdin(pattern: str, print_number: bool, is_regex: bool):
    lines = []
    for line in sys.stdin.readlines():
        line = line.rstrip('\n')
        if check_line(line, pattern, is_regex):
            lines.append(line)
    if print_number:
        print(f'{len(lines)}')
    else:
        print(*lines, sep='\n')


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='print_number', action='store_true')
    parser.add_argument('-E', dest='is_regex', action='store_true')
    args = parser.parse_args(args_str)
    if len(args.files) == 0:
        input_from_stdin(args.pattern, args.print_number, args.is_regex)
    else:
        input_from_files(args.files, args.pattern, args.print_number, args.is_regex)


if __name__ == '__main__':
    main(sys.argv[1:])
