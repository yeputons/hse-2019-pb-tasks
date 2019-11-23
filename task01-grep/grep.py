#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse

global counter


def in_stdin(needle: str, flag: bool, flag_e: bool) -> None:
    counter = 0
    for line in sys.stdin.readlines():
        line = line.rstrip('\n')
        if flag_e is False:
            if needle in line:
                if flag:
                    counter += 1
                else:
                    print(line)
        else:
            if re.search(needle, line):
                if flag:
                    counter += 1
                else:
                    print(line)
    if flag:
        print(counter)


def files_output(len: int, filee: str, line: object) -> None:
    if len > 1:
        print(f'{filee}:{line}')
    else:
        print(line)


def in_files(filee: str, needle: str, flag: bool, flag_e: bool, len: int) -> None:
    counter = 0
    with open(filee, 'r') as in_file:
        for line in in_file.readlines():
            line = line.rstrip('\n')
            if flag_e:
                if re.search(needle, line):
                    if flag:
                        counter += 1
                    else:
                        files_output(len, filee, line)
            else:
                if needle in line:
                    if flag:
                        counter += 1
                    else:
                        files_output(len, filee, line)
        if flag:
            files_output(len, filee, counter)


def main(args_str: List[str]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', action='store_true')
    args = parser.parse_args(args_str)

    # STUB BEGINS
    if len(args.files) == 0:
        in_stdin(args.needle, args.c, args.regex)
    else:
        for i in args.files:
            in_files(i, args.needle, args.c, args.regex, len(args.files))


if __name__ == '__main__':
    main(sys.argv[1:])
