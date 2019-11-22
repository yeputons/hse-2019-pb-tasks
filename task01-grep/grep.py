#!/usr/bin/env python3
from typing import List
from typing import IO
import sys
import re
import argparse


def parse_args(args_str: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='counting', action='store_true')
    args = parser.parse_args(args_str)
    return args


def making_list(needle: str, stream: IO[str]) -> List[str]:
    lines: List[str] = []
    for line in stream:
        line = line.rstrip('\n')
        if re.search(needle, line):
            lines.append(line)
    return lines


def search_in_file(files: List[str], needle: str, counting: bool) -> None:
    for file in files:
        with open(file, 'r') as in_file:
            lines = making_list(needle, in_file)
        lines = [str(len(lines))] if counting else lines
        if len(files) > 1:
            lines = [f'{file}:{line}' for line in lines]
        for line in lines:
            print(line)


def search_in_stdin(needle: str, counting: bool) -> None:
    lines = making_list(needle, sys.stdin)
    lines = [str(len(lines))] if counting else lines
    for line in lines:
        print(line)


def main(args_str: List[str]) -> None:
    args = parse_args(args_str)
    needle = args.needle if args.regex else re.escape(args.needle)
    if args.files:
        search_in_file(args.files, needle, args.counting)
    else:
        search_in_stdin(needle, args.counting)


if __name__ == '__main__':
    main(sys.argv[1:])
