#!/usr/bin/env python3
from typing import List
from typing import TextIO
import sys
import re
import argparse


def reader(fname: str, needle: str, wh: TextIO,
           key_c: bool, key_add_fname: bool) -> None:
    str_list = [line.rstrip('\n') for line in wh if re.search(needle, line)]
    files_output(fname, str_list, key_c, key_add_fname)


def files_output(fname: str, str_list: list,
                 key_c: bool, key_add_fname: bool) -> None:
    if key_add_fname:
        if not key_c:
            for line in str_list:
                print(f'{fname}:{line}')
        else:
            print(f'{fname}:{len(str_list)}')
    else:
        if not key_c:
            for line in str_list:
                print(f'{line}')
        else:
            print(len(str_list))


def main(args_str: List[str]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', action='store_true')
    args = parser.parse_args(args_str)

    # STUB BEGINS
    needle = args.needle if args.regex else re.escape(args.needle)
    if len(args.files) > 1:
        key_add_fname = True
    else:
        key_add_fname = False
    if args.files:
        for i in args.files:
            with open(i, 'r') as in_file:
                reader(i, needle, in_file, args.c, key_add_fname)
    else:
        reader('', needle, sys.stdin, args.c, key_add_fname)


if __name__ == '__main__':
    main(sys.argv[1:])
