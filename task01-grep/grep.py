#!/usr/bin/env python3
from typing import List, Pattern
import sys
import re
import argparse


def create_needle(needle: str, is_regex: bool, is_register: bool) -> Pattern:
    if not is_regex:
        needle = re.escape(needle)
    return re.compile(needle, flags=re.IGNORECASE) if is_register else re.compile(needle)


def find_in_string(is_full: bool, is_invert: bool,
                   needle: Pattern[str], line: str) -> bool:
    return is_invert ^ bool(re.fullmatch(needle, line)
                            if is_full else re.search(needle, line))


def print_answer(is_count: bool, right_list: list, file_name: str) -> None:
    if is_count:
        action_count(right_list, file_name)
    else:
        print_screen(right_list, file_name)


def action_count(right_list: list, file_name: str) -> None:
    print(file_name, len(right_list), sep='')


def create_right_list(is_full: bool, is_invert: bool, is_miss: bool,
                      input_list: list, needle: Pattern[str]) -> list:
    right_list = []
    for line in input_list:
        line = line.rstrip('\n')
        if is_miss ^ find_in_string(is_full, is_invert, needle, line):
            right_list.append(line)
        elif is_miss:
            right_list.clear()
            break
    return right_list


def print_screen(right_list: list, file_name: str):
    for line in right_list:
        print(file_name, line, sep='')


def format_print(length: int, is_one: bool, is_count: bool, right_list: list, file_name: str):
    if length == 1:
        print_answer(is_count, right_list, '')
    else:
        if is_one:
            if len(right_list) > 0:
                print_answer(is_count, [''], file_name)
        else:
            print_answer(is_count, right_list, file_name + ':')


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-i', dest='register', action='store_true')
    parser.add_argument('-v', dest='invert', action='store_true')
    parser.add_argument('-x', dest='full', action='store_true')
    parser.add_argument('-l', dest='one', action='store_true')
    parser.add_argument('-L', dest='miss', action='store_true')
    args = parser.parse_args(args_str)

    needle: Pattern[str] = create_needle(args.needle, args.regex, args.register)

    if args.miss:
        args.one = True

    if args.files:
        for file_name in args.files:
            with open(file_name, 'r') as in_file:
                right_list = create_right_list(args.full, args.invert, args.miss,
                                               in_file.readlines(), needle)
            format_print(len(args.files), args.one, args.count, right_list, file_name)
    else:
        right_list = create_right_list(args.full, args.invert, args.miss,
                                       sys.stdin.readlines(), needle)
        print_answer(args.count, right_list, '')


if __name__ == '__main__':
    main(sys.argv[1:])
