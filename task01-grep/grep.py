#!/usr/bin/env python3
from typing import List
from typing import Tuple
from typing import TextIO
import sys
import re
import argparse


def get_lines_of_file(current_stream: TextIO) -> List[str]:
    return [line.rstrip('\n') for line in current_stream.readlines()]


def parse_files(files: List[Tuple[str, TextIO]]) -> List[Tuple[str, List[str]]]:
    return [(current_file, get_lines_of_file(stream)) for current_file, stream in files]


def check_entry(
        line: str, pattern: str, is_regex: bool, rev: bool, full_match: bool,
        case_ignore: bool) -> bool:
    if is_regex:
        searcher = re.search
        if full_match:
            searcher = re.fullmatch
        if case_ignore:
            return bool(searcher(pattern, line, flags=re.IGNORECASE)) ^ rev
        return bool(searcher(pattern, line)) ^ rev
    else:
        if case_ignore:
            pattern = pattern.casefold()
            line = line.casefold()
        if full_match:
            return (pattern == line) ^ rev
        return (pattern in line) ^ rev


def search_in_file(
        name_file: str, is_regex: bool, rev: bool, full_match: bool, case_ignore: bool,
        lines: List[str], pattern: str, fmt: str) -> bool:
    entry = 0
    for line in lines:
        if check_entry(line, pattern, is_regex, rev, full_match, case_ignore):
            entry = 1
            if fmt != '{0}':
                print(fmt.format(name_file, line))
    return bool(entry)


def count_in_lines(
        lines: List[str], is_regex: bool, rev: bool, full_match: bool,
        case_ignore: bool, pattern: str) -> int:
    res = 0
    for line in lines:
        res += check_entry(line, pattern, is_regex, rev, full_match, case_ignore)
    return res


def search_in_files(
        parse_data: List[Tuple[str, List[str]]], regex_flag: bool,
        rev: bool, full_match: bool, case_ignore: bool, pattern: str,
        count_output: bool, fmt: str):
    files_with_entry = []
    for current_file, lines_of_file in parse_data:
        if count_output:
            print(fmt.format(
                current_file, count_in_lines(
                    lines_of_file, regex_flag, rev, full_match, case_ignore, pattern
                    )
                ))
        else:
            entry = search_in_file(
                current_file, regex_flag, rev, full_match, case_ignore,
                lines_of_file, pattern, fmt
            )
            if entry:
                files_with_entry.append(current_file)
    if fmt == '{0}':
        for current_file in files_with_entry:
            print(fmt.format(current_file, ''))


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', help='pattern for search', type=str)
    parser.add_argument('files', nargs='*')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', help='count pattern in files', dest='count', action='store_true')
    group.add_argument('-l', help='names files with pattern', dest='names', action='store_true')
    group.add_argument(
        '-L', help='names files without pattern', dest='rev_names', action='store_true'
    )
    parser.add_argument('-E', help='if pattern is regex', dest='regex', action='store_true')
    parser.add_argument('-i', help='ignore case', dest='case_ignore', action='store_true')
    parser.add_argument('-v', help='rev result', dest='rev', action='store_true')
    parser.add_argument('-x', help='full match', dest='full_match', action='store_true')
    args = parser.parse_args(args_str)

    fmt = ''
    if args.names or args.rev_names:
        if args.rev_names:
            args.rev ^= 1
        fmt = '{0}'
    elif len(args.files) > 1:
        fmt = '{0}:{1}'
    else:
        fmt = '{1}'

    files = []
    if len(args.files) > 0:
        for current_file in args.files:
            files.append((current_file, open(current_file, 'r')))
    else:
        files = [('sys.stdin', sys.stdin)]
    parse_data = parse_files(files)
    search_in_files(
        parse_data, args.regex, args.rev, args.full_match, args.case_ignore,
        args.needle, args.count, fmt
    )


if __name__ == '__main__':
    main(sys.argv[1:])
