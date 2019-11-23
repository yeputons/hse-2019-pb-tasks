#!/usr/bin/python
# -*- coding: UTF-8 -*-

from typing import List
import sys
import re
import argparse


def print_everything(count: bool, len_list_of_files: int, in_file: str, string: List[str], counter: int):
    if count and not len_list_of_files == 1:
        print(f'{in_file}:{counter}')
    elif count and len_list_of_files == 1:
        print(counter)
    elif not count and not len_list_of_files == 1:
        for needle in string:
            print(in_file + ':' + needle)
    else:
        for needle in string:
            print(needle)


def run_search(in_file: str, count: bool, if_file: bool, len_list_of_files: int, pattern: str):
    counter = 0
    string = []
    if if_file:
        fin = open(in_file, 'r')
    else:
        fin = in_file
    for line in fin.readlines():
        line = line.rstrip('\n')
        if pattern in line:
            counter += 1
            string.append(line)
    print_everything(count, len_list_of_files, in_file, string, counter)


def run_regex(in_file: str, count: bool, if_file: bool, len_list_of_files: int, pattern: str):
    counter = 0
    string = []
    if if_file:
        fin = open(in_file, 'r')
    else:
        fin = in_file
    for line in fin.readlines():
        line = line.rstrip('\n')
        if re.search(pattern, line):
            counter += 1
            string.append(line)
    print_everything(count, len_list_of_files, in_file, string, counter)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    args = parser.parse_args(args_str)

    if args.files:
        for file in args.files:
            try:
                fin = open(file, 'r')
            except IOError as e:
                print(f'I cannot open {file} file')
                args.files.remove(file)
        for file in args.files:
            if args.regex:
                run_regex(file, args.count, True, len(args.files), args.needle)
            else:
                run_search(file, args.count, True, len(args.files), args.needle)
    else:
        if args.regex:
            run_regex(sys.stdin, args.count, False, 1, args.needle)
        else:
            run_search(sys.stdin, args.count, False, 1, args.needle)




if __name__ == '__main__':
    main(sys.argv[1:])