#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def parse_count(needle, files):

    if len(files) == 0:
        counter = 0
        for line in sys.stdin.readlines():
            line = line.rstrip('\n')
            if needle in line:
                counter += 1
        print(counter)
    else:
        for f in files:
            counter = 0
            with open(f, 'r') as in_file:
                for line in in_file.readlines():
                    line = line.rstrip('\n')
                    if needle in line:
                        counter += 1
            print(f'{f}:{counter}')


def parse_files(needle, files):
    for f in files:
        with open(f, 'r') as in_file:
            for line in in_file.readlines():
                line = line.rstrip('\n')
                if needle in line:
                    if len(files) > 1:
                        print(f'{f}:{line}')
                    else:
                        print(line)


def parse_std(needle):
    for line in sys.stdin.readlines():
        line = line.rstrip('\n')
        if needle in line:
            print(line)


def parse_e_flag(needle, files):

    if len(files) == 0:
        for line in sys.stdin.readlines():
            line = line.rstrip('\n')
            if re.search(needle, line):
                print(line)
    else:
        for f in files:
            with open(f, 'r') as in_file:
                for line in in_file.readlines():
                    line = line.rstrip('\n')
                    if re.search(needle, line):
                        if len(files) > 1:
                            print(f'{f}:{line}')
                        else:
                            print(line)


def my_grep(args):

    if args.count:
        parse_count(args.needle, args.files)
    else:
        if args.regex:
            parse_e_flag(args.needle, args.files)
        else:
            if len(args.files) == 0:
                parse_std(args.needle)
            else:
                parse_files(args.needle, args.files)


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
