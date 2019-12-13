#!/usr/bin/env python3
from typing import List, Pattern, Optional
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


def compile_pattern(pattern: str, is_regular: bool, is_ignore: bool) -> Pattern[str]:
    if not is_regular:
        pattern = re.escape(pattern)
    return re.compile(pattern, flags=re.IGNORECASE if is_ignore else 0)


def strip_lines(lines: List[str]) -> List[str]:
    return [line.rstrip('\n') for line in lines]


def read_files(files: List[str]) -> List[List[str]]:
    lines_of_lines = []
    for file in files:
        with open(file, 'r') as input_file:
            lines_of_lines.append(input_file.readlines())
    return lines_of_lines


def bool_match(line: str, pattern: Pattern[str], is_invert: bool,
               is_match: bool) -> bool:
    match_line = pattern.fullmatch(line) if is_match else pattern.search(line)
    return is_invert ^ bool(match_line)


def processing_result_lines(lines: List[str], pattern: Pattern[str], is_invert: bool,
                            is_match: bool) -> List[str]:
    return [line for line in lines if bool_match(line, pattern, is_invert, is_match)]


def process_file_with_str_or_without_str(lines: List[str],
                                         source: str, is_without: bool) -> List[str]:
    return [source] if bool(lines) ^ is_without else []


def process_count(lines: List[str], stream_name: Optional[str]) -> List[str]:
    stream_name = f'{stream_name}:' if stream_name else ''
    lines = [str(len(lines))]
    return [f'{stream_name}{line}' for line in lines]


def process_no_flags(lines: List[str], stream_name: Optional[str]) -> List[str]:
    return [f'{stream_name}:{line}' if stream_name else line for line in lines]


def processing_underprint_results(lines: List[str], stream_name: str, is_count: bool,
                                  is_file_with_str: bool, is_file_without_str: bool) -> List[str]:
    if is_file_with_str or is_file_without_str:
        lines = process_file_with_str_or_without_str(lines, stream_name, is_file_without_str)
    if is_count:
        lines = process_count(lines, stream_name)
    if not is_count | is_file_without_str | is_file_with_str:
        lines = process_no_flags(lines, stream_name)
    return lines


def print_grep_results(result: List[str]) -> None:
    for word in result:
        print(word)


def main(args_str: List[str]):
    args = init_arguments(args_str)

    pattern = compile_pattern(args.pattern, args.regex, args.ignore)

    if args.files:
        stream_names = args.files
        lines_of_lines = read_files(stream_names)
        if len(args.files) <= 1:
            stream_names = [None]
    else:
        lines_of_lines = [sys.stdin.readlines()]
        stream_names = [None]

    for stream_name, lines in zip(stream_names, lines_of_lines):
        lines = strip_lines(lines)
        lines = processing_result_lines(lines, pattern, args.invert, args.match)
        lines = processing_underprint_results(lines, stream_name, args.count,
                                              args.file_with_str, args.file_without_str)
        print_grep_results(lines)


if __name__ == '__main__':
    main(sys.argv[1:])
