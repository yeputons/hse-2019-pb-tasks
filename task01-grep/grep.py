#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def regular_expression_check(pattern: str, line: str,
                             amount_output_format: bool, file_name: str,
                             name_in_output: bool) -> int:
    if re.search(pattern, line):
        return print_format(file_name, line, name_in_output,
                            amount_output_format)
    return 0


def which_keys_included(is_regex: bool, amount_output_format: bool,
                        pattern: str, line: str, file_name: str,
                        name_in_output: bool) -> int:
    if is_regex:
        return regular_expression_check(pattern, line, amount_output_format,
                                        file_name, name_in_output)
    elif pattern in line:
        return print_format(file_name, line, name_in_output,
                            amount_output_format)
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


def lines_reader(line: str, counter: int, is_regex: bool,
                 amount_output_format: bool, pattern: str,
                 file_name: str, name_in_output: bool) -> int:
    line = line.rstrip('\n')
    counter += which_keys_included(is_regex, amount_output_format, pattern,
                                   line, file_name, name_in_output)
    return counter


def input_type_parser(files: List[str], pattern: str, is_regex: bool,
                      amount_output_format: bool) -> None:
    counter = 0
    if files:
        name_in_output = len(files) > 1
        for file_name in files:
            with open(file_name, 'r') as in_file:
                for line in in_file.readlines():
                    counter = lines_reader(line, counter, is_regex,
                                           amount_output_format, pattern,
                                           file_name, name_in_output)
            if amount_output_format:
                print(f'{file_name}:{counter}')
                counter = 0
    else:
        for line in sys.stdin.readlines():
            counter = lines_reader(line, counter, is_regex,
                                   amount_output_format, pattern, '', False)
        if amount_output_format:
            print(counter)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='is_regex', action='store_true')
    parser.add_argument('-c', dest='amount_output_format', action='store_true')
    args = parser.parse_args(args_str)

    # STUB BEGINS
    input_type_parser(args.files, args.pattern, args.is_regex,
                      args.amount_output_format)
    # STUB ENDS


if __name__ == '__main__':
    main(sys.argv[1:])
