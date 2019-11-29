#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def find_in_string(is_register: bool, is_full: bool, is_invert: bool,
                   is_miss: bool, is_regex: bool, needle: str, line: str) -> bool:
    ans = needle in line
    cmd = 0
    if is_register:
        cmd = re.IGNORECASE
        needle = needle.lower()
        line = line.lower()
    if is_regex:
        if is_full:
            ans = re.fullmatch(needle, line, cmd) is not None
        else:
            ans = re.search(needle, line, cmd) is not None
    if is_invert:
        ans = not ans
    if is_miss:
        ans = not ans
    return ans


def print_answer(is_count: bool, right_list: list, file_name: str) -> None:
    if is_count:
        action_count(right_list, file_name)
    else:
        print_screen(right_list, file_name)


def action_count(right_list: list, file_name: str) -> None:
    print(file_name, len(right_list), sep='')


def create_right_list(is_register: bool, is_full: bool, is_invert: bool, is_miss: bool,
                      is_regex: bool, input_list: list, needle: str, right_list: list) -> None:
    for line in input_list:
        line = line.rstrip('\n')
        if find_in_string(is_register, is_full, is_invert, is_miss, is_regex, needle, line):
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
    parser.add_argument('-i', dest='register', action='store_true')
    parser.add_argument('-v', dest='invert', action='store_true')
    parser.add_argument('-x', dest='full', action='store_true')
    parser.add_argument('-l', dest='one', action='store_true')
    parser.add_argument('-L', dest='miss', action='store_true')
    args = parser.parse_args(args_str)
    if args.miss:
        args.one = True

    if args.files:
        for name_file in args.files:
            right_list: list
            right_list = []
            with open(name_file, 'r') as in_file:
                create_right_list(args.register, args.full, args.invert, args.miss,
                                  args.regex, in_file.readlines(), args.needle, right_list)
            if len(args.files) == 1:
                print_answer(args.count, right_list, '')
            else:
                if args.one:
                    if len(right_list) > 0:
                        print_answer(args.count, [''], name_file)
                else:
                    print_answer(args.count, right_list, name_file + ':')
    else:
        right_list = []
        create_right_list(args.register, args.full, args.invert, args.miss,
                          args.regex, sys.stdin.readlines(), args.needle, right_list)
        print_answer(args.count, right_list, '')


if __name__ == '__main__':
    main(sys.argv[1:])
