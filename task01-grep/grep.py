#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def parse_args(args_str: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    args = parser.parse_args(args_str)

    return args


def find_pattern_in_line(line: str, pattern: str, is_pattern_regex: bool) -> bool:
    return re.search(re.compile(pattern) if is_pattern_regex else re.escape(pattern), line)


def filter_matched_lines(lines: List[str], pattern: str, is_pattern_regex: bool) -> List[str]:
    return [line for line in lines
            if find_pattern_in_line(line, pattern, is_pattern_regex)]


def grep_from_lines(read_lines: List[str], pattern: str,
                    is_pattern_regex=False, is_only_count=False) -> List:
    filtered_lines = filter_matched_lines(read_lines, pattern, is_pattern_regex)
    if is_only_count:
        cnt = len(filtered_lines)
        return [cnt] if cnt else []
    return filtered_lines


def find_lines_from_grep_files(files: str, pattern: str, is_pattern_regex=False,
                               is_only_count=False) -> List[str]:
    filtered_lines: List[str] = []
    for file_name in files:
        try:
            with open(file_name, 'r') as in_file:
                lines = grep_from_lines(in_file.read().split('\n'),
                                        pattern, is_pattern_regex, is_only_count)
                filtered_lines += ['{}{}'.format((file_name + ':') if len(files) > 1 else '', line)
                                   for line in lines]
        except (OSError, IOError):
            print('{}:not found'.format(file_name), file=sys.stderr)
    return filtered_lines


def find_lines_from_grep_stdin(pattern: str, is_pattern_regex=False,
                               is_only_count=False) -> List[str]:
    return grep_from_lines(sys.stdin.read().split('\n'),
                           pattern, is_pattern_regex, is_only_count)


def main(args_str: List[str]):
    args = parse_args(args_str)

    if args.files:
        lines = find_lines_from_grep_files(args.files, args.pattern, args.regex, args.count)
    else:
        lines = find_lines_from_grep_stdin(args.pattern, args.regex, args.count)

    for line in lines:
        print(line)


if __name__ == '__main__':
    main(sys.argv[1:])
