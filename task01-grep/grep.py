from typing import List, IO
import sys
import re
import argparse


def parse_args(args_str: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    args = parser.parse_args(args_str)
    return args


def get_matching_lines(needle: str, stream: IO[str]) -> List[str]:
    lines = [line.rstrip('\n') for line in stream]
    return [line for line in lines if re.search(needle, line)]


def files_search(files: List[str], needle: str, count: bool):
    for file in files:
        with open(file, 'r') as in_file:
            lines = get_matching_lines(needle, in_file)
            lines = [str(len(lines))] if count else lines
            if len(files) != 1:
                lines = [f'{file}:{line}' for line in lines]
            for line in lines:
                print(line)


def stdin_search(needle: str, count: bool):
    lines = get_matching_lines(needle, sys.stdin)
    lines = [str(len(lines))] if count else lines
    for line in lines:
        print(line)


def main(args_str: List[str]):
    args = parse_args(args_str)
    needle = args.needle if args.regex else re.escape(args.needle)
    if args.files:
        files_search(args.files, needle, args.count)
    else:
        stdin_search(needle, args.count)


if __name__ == '__main__':
    main(sys.argv[1:])
