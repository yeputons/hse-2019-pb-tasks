#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def e_flag(pattern: str, line: str, c_key: bool, file_name: str, files_amount: int) -> int:
    if re.search(pattern, line):
        return print_format(file_name, line, files_amount, c_key)
    return 0


def key_checker(e_key: bool, c_key: bool, pattern: str, line: str, file_name: str,
                files_amount: int) -> int:
    if e_key:
        return e_flag(pattern, line, c_key, file_name, files_amount)
    elif pattern in line:
        return print_format(file_name, line, files_amount, c_key)
    return 0


def print_format(file_name: str, line: str, files_amount, c_key: bool) -> int:
    if c_key:
        return 1
    if files_amount > 1:
        print(f'{file_name}:{line}')
    else:
        print(line)
    return 0


def file_input_format(files: str, pattern: str, e_key: bool, c_key: bool) -> None:
    for file in files:
        counter = 0
        with open(file, 'r') as in_file:
            for line in in_file.readlines():
                line = line.rstrip('\n')
                counter += key_checker(e_key, c_key, pattern, line, file, len(files))
        if c_key:
            print(f'{file}:{counter}')


def konsole_input_format(pattern: str, c_key: bool, e_key: bool) -> None:
    counter = 0
    for line in sys.stdin.readlines():
        line = line.rstrip('\n')
        counter += key_checker(e_key, c_key, pattern, line, '', 0)
    if c_key:
        print(counter)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='e_key', action='store_true')
    parser.add_argument('-c', dest='c_key', action='store_true')
    args = parser.parse_args(args_str)

    # STUB BEGINS
    if args.files:
        file_input_format(args.files, args.pattern, args.e_key, args.c_key)
    else:
        konsole_input_format(args.pattern, args.c_key, args.e_key)
    # STUB ENDS


if __name__ == '__main__':
    main(sys.argv[1:])
