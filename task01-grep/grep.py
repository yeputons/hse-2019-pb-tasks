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
    return is_pattern_regex and bool(re.search(pattern, line)) or \
                not is_pattern_regex and pattern in line


def filter_matched_lines(lines: List[str], pattern: str, is_pattern_regex: bool) -> List[str]:
    return [line for line in lines
            if find_pattern_in_line(line, pattern, is_pattern_regex)]


def count_lines_with_pattern(lines: List[str], pattern: str, is_pattern_regex: bool) -> int:
    return len(filter_matched_lines(lines, pattern, is_pattern_regex))


def find_lines_from_grep(read_lines: List[str], pattern: str,
                         is_pattern_regex=False, is_only_count=False) -> List:
    if is_only_count:
        cnt = count_lines_with_pattern(read_lines, pattern, is_pattern_regex)
        return [cnt] if cnt else []
    return filter_matched_lines(read_lines, pattern, is_pattern_regex)


def find_lines_from_grep_files(files: str, pattern: str, is_pattern_regex=False,
                               is_only_count=False) -> List[str]:
    all_lines: List[str] = []
    for file_name in files:
        try:
            with open(file_name, 'r') as in_file:
                lines = find_lines_from_grep([line.rstrip('\n') for line in in_file.readlines()],
                                             pattern, is_pattern_regex, is_only_count)
                all_lines += ['{}{}'.format((file_name + ':') * (len(files) > 1), line)
                              for line in lines]
        except (OSError, IOError):
            all_lines += ['{}:not found'.format(file_name)]
    return all_lines


def find_lines_from_grep_stdin(pattern: str, is_pattern_regex=False,
                               is_only_count=False) -> List[str]:
    return find_lines_from_grep([line.rstrip('\n') for line in sys.stdin.readlines()],
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
