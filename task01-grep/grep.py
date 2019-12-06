#!/usr/bin/env python3
from typing import List, IO
from pathlib import Path
import sys
import re
import argparse


def print_out_result(result: List[str], is_amount: bool, print_name: bool, name_of_file: str):
    if is_amount:
        result = [str(len(result))]
    if print_name:
        result = [f'{name_of_file}:' + str(x) for x in result]
    for x in result:
        print(x)


def grep_input(input_stream: IO[str], pattern: str, is_amount: bool, print_name: bool,
               name_of_file: str):
    result = []
    for line in input_stream:
        line = line.rstrip('\n')
        if re.search(pattern, line):
            result.append(line)
    print_out_result(result, is_amount, print_name, name_of_file)


def redirect_input_stream(paths: List[Path], pattern: str, is_amount: bool):
    if not paths:
        grep_input(sys.stdin, pattern, is_amount, False, str(paths))
    else:
        for path in paths:
            path = Path(path)
            if path.is_dir():
                print(f'Is a directory: {path}')
            elif path.is_file():
                grep_input(path.open('r'), pattern, is_amount, len(paths) > 1, path.name)
            else:
                print(f'File not found')


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str, help='a pattern to search for')
    parser.add_argument('files', metavar='FILES', nargs='*',
                        help='the files(s) to search')
    parser.add_argument('-c', '--is_amount', action='store_true',
                        help='print out the amount of found lines')
    parser.add_argument('-E', '--is_regex', action='store_true',
                        help='search for a regular expression')
    args = parser.parse_args(args_str)
    pattern = args.pattern if args.is_regex else re.escape(args.pattern)
    redirect_input_stream(args.files, pattern, args.is_amount)


if __name__ == '__main__':
    main(sys.argv[1:])
