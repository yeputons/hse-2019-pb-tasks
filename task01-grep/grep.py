#!/usr/bin/env python3
from typing import List
from typing import TextIO
import sys
import re
import argparse


def reader(fname: str, needle: str, wh: TextIO, fl: bool, length: int) -> None:
    b = list()
    for line in wh:
        line = line.rstrip('\n')
        if re.search(needle, line):
            b.append(line)
            if not fl:
                files_output(length, fname, line)
    if fl:
        files_output(length, fname, len(b))


def in_stdin(needle: str, fl: bool) -> None:
    reader('', needle, sys.stdin, fl, 1)


def files_output(length: int, fname: str, line: object) -> None:
    if length > 1:
        print(f'{fname}:{line}')
    else:
        print(line)


def in_files(fname: str, needle: str, fl: bool, length: int) -> None:
    with open(fname, 'r') as in_file:
        reader(fname, needle, in_file, fl, length)


def main(args_str: List[str]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', action='store_true')
    args = parser.parse_args(args_str)

    # STUB BEGINS
    needle = args.needle if args.regex else re.escape(args.needle)
    if len(args.files) == 0:
        in_stdin(needle, args.c)
    else:
        for i in args.files:
            in_files(i, needle, args.c, len(args.files))


if __name__ == '__main__':
    main(sys.argv[1:])
