#!/usr/bin/env python3
from typing import List, IO
from pathlib import Path
import sys
import re
import argparse


def print_out_result(result: List[str], is_amount: bool, print_name: bool,
                     has_line: bool, no_lines: bool,
                     name_of_file: str, amount_of_lines: int):
    if is_amount:
        result = [str(len(result))]
    if print_name:
        result = [f'{name_of_file}:{x}' for x in result]
    if no_lines or has_line:
        result = []
    if (no_lines and amount_of_lines == 0) or (has_line and amount_of_lines > 0):
        result = [name_of_file]
    for x in result:
        print(x)


def check_pattern(line: str, pattern: str, full_match: bool, ignore_case: bool) -> bool:
    if full_match:
        return bool(re.fullmatch(pattern, line,
                                 re.IGNORECASE if ignore_case else not re.IGNORECASE))
    else:
        return bool(re.search(pattern, line,
                              re.IGNORECASE if ignore_case else not re.IGNORECASE))


def grep_input(input_stream: IO[str], pattern: str, is_amount: bool, print_name: bool,
               ignore_case: bool, inverse: bool,
               full_match: bool, has_line: bool, no_lines: bool, name_of_file: str):
    result = []
    for line in input_stream:
        line = line.rstrip('\n')
        check = check_pattern(line, pattern, full_match, ignore_case)
        if inverse:
            if not check:
                result.append(line)
        else:
            if check:
                result.append(line)
    print_out_result(result, is_amount, print_name, has_line,
                     no_lines, name_of_file, len(result))


def redirect_input_stream(paths: List[Path], pattern: str, is_amount: bool, ignore_case: bool,
                          inverse: bool, full_match: bool, has_line: bool, no_lines: bool):
    if not paths:
        grep_input(sys.stdin, pattern, is_amount, False,
                   ignore_case, inverse, full_match, has_line, no_lines, str(paths))
    else:
        for path in paths:
            path = Path(path)
            if path.is_file():
                grep_input(path.open('r'), pattern, is_amount,
                           len(paths) > 1 and not (has_line or no_lines),
                           ignore_case, inverse, full_match, has_line, no_lines, path.name)
            elif path.is_dir():
                print(f'Is a directory: {path}')
            else:
                print(f'Is not a file')


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str, help='a pattern to search for')
    parser.add_argument('files', metavar='FILES', nargs='*',
                        help='the files(s) to search')
    parser.add_argument('-c', '--is_amount', action='store_true',
                        help='print out the amount of found lines')
    parser.add_argument('-E', '--is_regex', action='store_true',
                        help='search for a regular expression')
    parser.add_argument('-i', '--ignore_case', action='store_true',
                        help='ignore case of characters')
    parser.add_argument('-v', '--inverse_result', action='store_true',
                        help='inverse the result')
    parser.add_argument('-x', '--full_match', action='store_true',
                        help='look for full matches')
    parser.add_argument('-l', '--has_line', action='store_true',
                        help='print name of files with at least one matching line')
    parser.add_argument('-L', '--no_lines', action='store_true',
                        help='print name of files with no matching lines')
    args = parser.parse_args(args_str)
    pattern = args.pattern if args.is_regex else re.escape(args.pattern)
    redirect_input_stream(args.files, pattern, args.is_amount, args.ignore_case,
                          args.inverse_result, args.full_match, args.has_line, args.no_lines)


if __name__ == '__main__':
    main(sys.argv[1:])
