#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def parse_count(args):

    if len(args.files) == 0:
        counter = 0
        for line in sys.stdin.readlines():
            line = line.rstrip('\n')
            if args.needle in line:
                counter += 1
        print(counter)
    else:
        for f in args.files:
            counter = 0
            with open(f, 'r') as in_file:
                for line in in_file.readlines():
                    line = line.rstrip('\n')
                    if args.needle in line:
                        counter += 1
            print(f"{f}:{counter}")


def parse_files(args):
    for f in args.files:
        with open(f, 'r') as in_file:
            for line in in_file.readlines():
                line = line.rstrip('\n')
                if args.needle in line:
                    if len(args.files) > 1:
                        print(f"{f}:{line}")
                    else:
                        print(line)


def parse_std(needle):
    for line in sys.stdin.readlines():
        line = line.rstrip('\n')
        if needle in line:
            print(line)


def parse_e_flag(args):

    if len(args.files) == 0:
        for line in sys.stdin.readlines():
            line = line.rstrip('\n')
            if re.search(args.needle, line):
                print(line)
    else:
        for f in args.files:
            with open(f, 'r') as in_file:
                for line in in_file.readlines():
                    line = line.rstrip('\n')
                    if re.search(args.needle, line):
                        if len(args.files) > 1:
                            print(f"{f}:{line}")
                        else:
                            print(line)


def my_grep(args):

    if args.count:
        parse_count(args)
    else:
        if args.regex:
            parse_e_flag(args)
        else:
            if len(args.files) == 0:
                parse_std(args.needle)
            else:
                parse_files(args)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    args = parser.parse_args(args_str)

    my_grep(args)


if __name__ == '__main__':
    main(sys.argv[1:])
