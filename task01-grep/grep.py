#!/usr/bin/env python3
from typing import List, IO
import sys
import argparse
import re


def parsing(args_str: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='cnt', action='store_true')
    return parser.parse_args(args_str)


def format_lines(args: argparse.Namespace, good_lines: List[str], filename: str) -> List[str]:
    output_lines = [str(len(good_lines))] if args.cnt else good_lines
    if len(args.files) <= 1:
        return output_lines
    return [f'{filename}:{line}' for line in output_lines]


def processing_lines(args: argparse.Namespace, source: IO[str], filename: str) -> None:
    line_pattern = args.needle if args.regex else re.escape(args.needle)

    lines = [line.rstrip('\n') for line in source]

    good_lines = [line for line in lines if re.search(line_pattern, line)]
    output_lines = format_lines(args, good_lines, filename)

    if output_lines:
        print(*output_lines, sep='\n')


def main(args_str: List[str]) -> None:
    args = parsing(args_str)

    if args.files:
        for file in args.files:
            with open(file, "r") as f:
                processing_lines(args, f, file)

    else:
        processing_lines(args, source=sys.stdin, filename='')


if __name__ == '__main__':
    main(sys.argv[1:])
