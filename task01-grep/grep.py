#!/usr/bin/env python3
from typing import List
import sys
import argparse
import re


def parsing(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=str)
    parser.add_argument('fs', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='cnt', action='store_true')
    return parser.parse_args(args_str)


def line_processing(args: argparse.Namespace) -> str:
    if not args.regex:
        return re.escape(args.n)
    else:
        return args.n


def print_from_file(lines: List[str], filename: str, len_namespace_files: int):
    if len_namespace_files == 1:
        print(*lines, sep='\n')
    else:
        for line in lines:
            print(f'{filename}:{line}', sep='\n')


def filew(filename: str, args: argparse.Namespace):
    with open(filename, 'r') as f:
        line_pattern = line_processing(args)

        lines = [line.rstrip('\n') for line in f]
        good_lines = [line for line in lines if re.search(line_pattern, line)]
        output_lines = [str(len(good_lines))] if args.cnt else good_lines

        print_from_file(output_lines, filename, len(args.fs))


def print_from_stdin(lines: List[str]):
    print(*lines, sep='\n')


def stdinw(args: argparse.Namespace):
    line_pattern = line_processing(args)

    lines = [line.rstrip('\n') for line in sys.stdin]
    good_lines = [line for line in lines if re.search(line_pattern, line)]
    output_lines = [str(len(good_lines))] if args.cnt else good_lines

    print_from_stdin(output_lines)


def main(args_str: List[str]):
    args = parsing(args_str)

    if args.fs:
        for file in args.fs:
            filew(file, args)

    else:
        stdinw(args)


if __name__ == '__main__':
    main(sys.argv[1:])
