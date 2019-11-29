#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def find_in_string(is_regex: bool, needle: str, line: str) -> bool:
    if is_regex:
        return re.search(needle, line) is not None
    return needle in line


def print_answer(is_count: bool, right_list: list, file_name: str) -> None:
    if is_count:
        action_count(right_list, file_name)
    else:
        print_screen(right_list, file_name)


def action_count(right_list: list, file_name: str) -> None:
    print(file_name, len(right_list), sep='')


def create_right_list(is_regex: bool, input_list: list, needle: str, right_list: list) -> None:
    for line in input_list:
        line = line.rstrip('\n')
        if find_in_string(is_regex, needle, line):
            right_list.append(line)


def print_screen(right_list: list, file_name: str):
    for line in right_list:
        print(file_name, line, sep='')


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    args = parser.parse_args(args_str)

    if args.files:
        for name_file in args.files:
            right_list: list
            right_list = []
            with open(name_file, 'r') as in_file:
                create_right_list(args.regex, in_file.readlines(), args.needle, right_list)
            if len(args.files) == 1:
                print_answer(args.count, right_list, '')
            else:
                print_answer(args.count, right_list, name_file + ':')
    else:
        right_list = []
        create_right_list(args.regex, sys.stdin.readlines(), args.needle, right_list)
        print_answer(args.count, right_list, '')


if __name__ == '__main__':
    main(sys.argv[1:])
