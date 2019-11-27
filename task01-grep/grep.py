#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def parse_all(args_str: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='sum', action='store_true')
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    args_out = parser.parse_args(args_str)
    return args_out


def count_lines(word, lines: List[str]):
    number_of_lines = 0
    for line in lines:
        line = line.rstrip('\n')
        if word in line:
            number_of_lines += 1
    print(number_of_lines)


def print_lines(word, lines: List[str]):
    for line in lines:
        line = line.rstrip('\n')
        if word in line:
            print(line)


def print_lines_regex(word, lines: List[str]):
    for line in lines:
        line = line.rstrip('\n')
        if re.search(word, line):
            print(line)


def print_in_files(word, lines: List[str], file, amount_of_files):
    for line in lines:
        line = line.rstrip('\n')
        if word in line:
            if (amount_of_files > 1):
                print(file + ':', end='')
            print(line)


def main(args_str: List[str]):
    args = parse_all(args_str)

    # STUB BEGINS
    amount_of_files = len(args.files)
    word = args.needle
    if (amount_of_files >= 1):
        if (args.sum):
            for file in args.files:
                with open(file, 'r') as in_file:
                    if (amount_of_files > 1):
                        print(file + ':', end='')
                    count_lines(word, in_file.readlines())
        else:
            for file in args.files:
                with open(file, 'r') as in_file:
                    print_in_files(word, in_file.readlines(), file, amount_of_files)
    else:
        lines = sys.stdin.readlines()
        if (args.regex):
            if (args.sum):
                count_lines(word, lines)
            print_lines_regex(word, lines)
        else:
            if (args.sum):
                count_lines(word, lines)
            else:
                print_lines(word, lines)
    # STUB ENDS


if __name__ == '__main__':
    main(sys.argv[1:])
