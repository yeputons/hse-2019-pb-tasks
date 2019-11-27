#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def parse_all(args_str: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='sum', action='store_true')
    parser.add_argument('-i', dest='register', action='store_true')
    parser.add_argument('-v', dest='reflection', action='store_true')
    parser.add_argument('-x', dest='equality', action='store_true')
    parser.add_argument('-l', dest='inside', action='store_true')
    parser.add_argument('-L', dest='outside', action='store_true')
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


def find_lines_in_file(word, lines: List[str], e, i, v, x):
    ans_list = []
    if e:
        for line in lines:
            line = line.rstrip('\n')
            if i:
                if x:
                    if v:
                        if re.fullmatch(word, line, flags=re.IGNORECASE):
                            continue
                        else:
                            ans_list.append(line)
                    else:
                        if re.fullmatch(word, line, flags=re.IGNORECASE):
                            ans_list.append(line)
                else:
                    if v:
                        if re.search(word, line, flags=re.IGNORECASE):
                            continue
                        else:
                            ans_list.append(line)
                    else:
                        if re.search(word, line, flags=re.IGNORECASE):
                            ans_list.append(line)
            else:
                if x:
                    if v:
                        if re.fullmatch(word, line):
                            continue
                        else:
                            ans_list.append(line)
                    else:
                        if re.fullmatch(word, line):
                            ans_list.append(line)
                else:
                    if v:
                        if re.search(word, line):
                            continue
                        else:
                            ans_list.append(line)
                    else:
                        if re.search(word, line):
                            ans_list.append(line)
    else:
        for line in lines:
            line = line.rstrip('\n')
            if word in line:
                ans_list.append(line)
    return ans_list


def print_in_file(file, lines: List[str], c, l_in, l_out, amount_of_files):
    if c:
        if amount_of_files > 1:
            print(file + ':', end='')
        print(len(lines))
    else:
        if l_in:
            if len(lines) > 0:
                print(file)
        else:
            if l_out:
                if len(lines) == 0:
                    print(file)
            else:
                for line in lines:
                    if amount_of_files > 1:
                        print(file + ':', end='')
                    print(line)


def main(args_str: List[str]):
    args = parse_all(args_str)

    # STUB BEGINS
    amount_of_files = len(args.files)
    word = args.needle
    if amount_of_files >= 1:
        for file in args.files:
            with open(file, 'r') as in_file:
                lines = find_lines_in_file(word, in_file.readlines(), args.regex,
                                           args.register, args.reflection, args.equality)
                print_in_file(file, lines, args.sum, args.inside, args.outside, amount_of_files)
    else:
        lines = sys.stdin.readlines()
        if args.regex:
            if args.sum:
                count_lines(word, lines)
            print_lines_regex(word, lines)
        else:
            if args.sum:
                count_lines(word, lines)
            else:
                print_lines(word, lines)
    # STUB ENDS


if __name__ == '__main__':
    main(sys.argv[1:])
