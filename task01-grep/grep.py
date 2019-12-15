#!/usr/bin/env python3
from typing import List, IO
import sys
import re
import argparse


def is_match(regex_key: bool, line: str, pattern: str) -> bool:
    if regex_key:
        return bool(re.search(pattern, line))
    else:
        return pattern in line


def get_matches(regex_key: bool, needle: str, stream: IO[str]) -> List[str]:
    lines = [line.rstrip('\n') for line in stream]
    return [line for line in lines if is_match(regex_key, line, needle)]


def main(args_str: List[str]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='count', action='store_true', help='key')
    parser.add_argument('-E', dest='regex_key', action='store_true', help='key')
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    args = parser.parse_args(args_str)

    files_in_input = bool(args.files)
    files: List[str] = ['']
    if args.files:
        files = args.files
    for file in files:
        with open(file, 'r') if files_in_input else sys.stdin as opened_file:
            lines = get_matches(args.regex_key, args.needle, opened_file)
            lines = [str(len(lines))] if args.count else lines
            if len(args.files) > 1:
                lines = [f'{file}:{line}' for line in lines]
            for line in lines:
                print(line)


if __name__ == '__main__':
    main(sys.argv[1:])
