#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def print_count(args: argparse.Namespace, data: List[str]):
    count = 0
    for line in data:
        line = line.rstrip('\n')
        if args.needle in line:
            count += 1
    return count


def print_count_e(args: argparse.Namespace, data: List[str]):
    count = 0
    for line in data:
        line = line.rstrip('\n')
        if re.search(args.needle, line):
            count += 1
    return count


def print_count_files(args: argparse.Namespace, data: List[str]):
    if not args.files:
        if args.extended:
            print(print_count_e(args, data))
        else:
            print(print_count(args, data))
    else:
        for line in data:
            filename = line
            with open(line, 'r') as in_file:
                if args.extended:
                    if len(data) > 1:
                        print(f'{filename}:{print_count_e(args, in_file.readlines())}')
                    else:
                        print(print_count_e(args, in_file.readlines()))
                else:
                    if len(data) > 1:
                        print(f'{filename}:{print_count(args, in_file.readlines())}')
                    else:
                        print(print_count(args, in_file.readlines()))


def print_file(args: argparse.Namespace, dest: List[str], filename):
    for line in dest:
        line = line.rstrip('\n')
        if args.extended:
            if re.search(args.needle, line):
                printer(args, filename, line)
        else:
            if args.needle in line:
                printer(args, filename, line)


def printer(args: argparse.Namespace, filename: str, line):
    if len(args.files) > 1:
        print(f'{filename}:{line}')
    else:
        print(line)


def print_files(args: argparse.Namespace, data: List[str]):
    if not args.files:
        print_file(args, data, data)
    else:
        for line in data:
            filename = line
            with open(line, 'r') as in_file:
                print_file(args, in_file.readlines(), filename)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', metavar='file', type=str, nargs='*')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-E', dest='extended', action='store_true')
    args = parser.parse_args(args_str)

    data = args.files
    if len(data) == 0:
        data = sys.stdin.readlines()

    if args.count:
        print_count_files(args, data)
    else:
        print_files(args, data)


if __name__ == '__main__':
    main(sys.argv[1:])
