#!/usr/bin/env python3
from typing import List, Pattern
import sys
import re
import argparse


def init_arguments(args_str: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-i', dest='ignore', action='store_true')
    parser.add_argument('-v', dest='invert', action='store_true')
    parser.add_argument('-x', dest='match', action='store_true')
    parser.add_argument('-l', dest='file_with_str', action='store_true')
    parser.add_argument('-L', dest='file_without_str', action='store_true')

    args = parser.parse_args(args_str)
    return args


def compile_pattern(pattern: str, is_regular: bool, ignored: bool) -> Pattern[str]:
    if not is_regular:
        pattern = re.escape(pattern)
    return re.compile(pattern, flags=re.IGNORECASE if ignored else 0)


def strip_lines(lines: List[str]) -> List[str]:
    return [line.rstrip('\n') for line in lines]


def read_files(files: List[str]) -> List[List[str]]:
    all_lines = []
    for file in files:
        with open(file, 'r') as input_file:
            all_lines.append(input_file.readlines())
    return all_lines


def bool_match(line: str, pattern: Pattern[str], inverted: bool,
               matched: bool) -> bool:
    match_line = pattern.fullmatch(line) if matched else pattern.search(line)
    return inverted ^ bool(match_line)


def filter_lines(lines: List[str], pattern: Pattern[str], inverted: bool,
                 matched: bool) -> List[str]:
    return [line for line in lines if bool_match(line, pattern, inverted, matched)]


def parse_output_results(lines: List[str], source: str, counted: bool,
                         file_with_str: bool, file_without_str: bool) -> List[str]:
    if file_with_str or file_without_str:
        lines = [source] if bool(lines) ^ file_without_str else []
    else:
        filename_prefix = f'{source}:' if source else ''
        if counted:
            lines = [str(len(lines))]
        lines = [f'{filename_prefix}{line}' for line in lines]
    return lines


def print_output_results(result: List[str]) -> None:
    for word in result:
        print(word)


def main(args_str: List[str]):
    args = init_arguments(args_str)

    pattern = compile_pattern(args.pattern, args.regex, args.ignore)

    if args.files:
        stream_names = args.files
        lines_of_lines = read_files(stream_names)
    else:
        lines_of_lines = [sys.stdin.readlines()]
        stream_names = [None]

    if len(args.files) == 1 and not (args.file_with_str and args.file_without_str):
        stream_names = [None]

    for stream_name, lines in zip(stream_names, lines_of_lines):
        lines = strip_lines(lines)
        lines = filter_lines(lines, pattern, args.invert, args.match)
        lines = parse_output_results(lines, stream_name, args.count,
                                     args.file_with_str, args.file_without_str)
        print_output_results(lines)


if __name__ == '__main__':
    main(sys.argv[1:])
