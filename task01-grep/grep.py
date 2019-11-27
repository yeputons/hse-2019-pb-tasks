#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    args = parser.parse_args(args_str)

    # STUB BEGINS
    for line in sys.stdin.readlines():
        line = line.rstrip('\n')
        if args.needle in line:
            print('Found needle in ' + line)

    with open('input.txt', 'r') as in_file:
        for line in in_file.readlines():
            line = line.rstrip('\n')
            if re.search(args.needle, line):
                print(f'Found re in {line}')
    # STUB ENDS


if __name__ == '__main__':
    main(sys.argv[1:])
