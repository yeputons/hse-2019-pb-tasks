#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def regular_expression_check(pattern: str, line: str, amount_output_format: bool,
                             file_name: str, name_in_output: bool) -> int:
    if re.search(pattern, line):
        return print_format(file_name, line, name_in_output, amount_output_format)
    return 0


def which_keys_included(regular_expression_format: bool, amount_output_format: bool,
                        pattern: str, line: str, file_name: str, name_in_output: bool) -> int:
    if regular_expression_format:
        return regular_expression_check(pattern, line, amount_output_format,
                                        file_name, name_in_output)
    elif pattern in line:
        return print_format(file_name, line, name_in_output, amount_output_format)
    return 0


def print_format(file_name: str, line: str, name_in_output: bool,
                 amount_output_format: bool) -> int:
    if amount_output_format:
        return 1
    if name_in_output:
        print(f'{file_name}:{line}')
    else:
        print(line)
    return 0


def input_from_file(files: List[str], pattern: str, regular_expression_format: bool,
                    amount_output_format: bool) -> None:
    name_in_output = len(files) > 1
    for file_name in files:
        counter = 0
        with open(file_name, 'r') as in_file:
            for line in in_file.readlines():
                line = line.rstrip('\n')
                counter += which_keys_included(regular_expression_format,
                                               amount_output_format, pattern,
                                               line, file_name, name_in_output)
        if amount_output_format:
            print(f'{file_name}:{counter}')


def input_from_console(pattern: str, amount_output_format: bool,
                       regular_expression_format: bool) -> None:
    counter = 0
    for line in sys.stdin.readlines():
        line = line.rstrip('\n')
        counter += which_keys_included(regular_expression_format, amount_output_format,
                                       pattern, line, '', False)
    if amount_output_format:
        print(counter)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regular_expression_format', action='store_true')
    parser.add_argument('-c', dest='amount_output_format', action='store_true')
    args = parser.parse_args(args_str)

    # STUB BEGINS
    if args.files:
        input_from_file(args.files, args.pattern, args.regular_expression_format,
                        args.amount_output_format)
    else:
        input_from_console(args.pattern, args.amount_output_format,
                           args.regular_expression_format)
    # STUB ENDS


if __name__ == '__main__':
    main(sys.argv[1:])
