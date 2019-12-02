#!/usr/bin/env python3
from typing import List, Iterable, Pattern
import sys
import re
import argparse as ap


def parse_args(args_str: List[str]) -> ap.Namespace:
    parser = ap.ArgumentParser()
    parser.add_argument('-v', dest='invert_mode', action='store_true', help='invert result')
    parser.add_argument('-i', dest='ignore_case', action='store_true', help='ignore case')
    parser.add_argument('-x', dest='full_match', action='store_true', help='only full matched ines')
    parser.add_argument('-c', dest='count', action='store_true', help='count matches')
    parser.add_argument('-E', dest='regex', action='store_true',
                        help='given string is understood as regex')
    parser.add_argument('-l', dest='only_files', action='store_true',
                        help='return only file names')
    parser.add_argument('-L', dest='only_files_invert', action='store_true',
                        help='Require file name to be set')
    parser.add_argument('pattern', type=str, help='first string after flags')
    parser.add_argument('file_names', nargs='*',
                        help='arguments after pattern are files names')
    return parser.parse_args(args_str)


def match_line(pattern: Pattern[str], line: str,
               full_match: bool = False, invert_mode: bool = False) -> bool:
    return invert_mode ^ bool(re.fullmatch(pattern, line)
                              if full_match else re.search(pattern, line))


def match_lines(pattern: Pattern[str], data: List[str],
                full_match: bool = False, invert_mode: bool = False) -> List[str]:
    return [line for line in data if match_line(pattern, line, full_match, invert_mode)]


def strip_lines(lines: Iterable) -> List[str]:
    return [line.rstrip('\n') for line in lines]


def compile_pattern(pattern: str, is_regex: bool, ignore_case: bool = False) -> Pattern:
    if not is_regex:
        pattern = re.escape(pattern)
    return re.compile(pattern, flags=re.IGNORECASE) if ignore_case else re.compile(pattern)


def format_data(data: List[str], counting_mode: bool, only_files: bool = False,
                only_files_invert: bool = False, source_name: str = None) -> List[str]:
    if only_files or only_files_invert:
        assert source_name
        return [source_name] if only_files_invert ^ bool(data) else []
    if counting_mode:
        data = [str(len(data))]
    if source_name:
        return ['{}:{}'.format(source_name, line) for line in data]
    else:
        return data


def find_in_source(source: Iterable, pattern: Pattern[str],
                   counting_mode: bool, full_match: bool = False,
                   invert_mode: bool = False, only_files: bool = False,
                   only_files_invert: bool = False, source_name: str = None) -> List[str]:
    result: List[str] = match_lines(pattern, strip_lines(source), full_match, invert_mode)
    return format_data(result, counting_mode, only_files, only_files_invert, source_name)


def print_result(lines: List[str]) -> None:
    for line in lines:
        print(line)


def main(args_str: List[str]):
    args: ap.Namespace = parse_args(args_str)
    result: List[str] = []
    pattern: Pattern[str] = compile_pattern(args.pattern, args.regex, args.ignore_case)
    if args.file_names:
        for file_name in args.file_names:
            with open(file_name, 'r') as file:
                source_name: str = file_name if len(
                    args.file_names) > 1 or args.only_files or args.only_files_invert else None
                result += find_in_source(file, pattern, args.count, args.full_match,
                                         args.invert_mode, args.only_files, args.only_files_invert,
                                         source_name)
    else:
        result = find_in_source(sys.stdin, pattern, args.count, args.full_match,
                                args.invert_mode, args.only_files, args.only_files_invert)
    print_result(result)


if __name__ == '__main__':
    main(sys.argv[1:])
