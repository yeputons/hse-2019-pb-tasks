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
    parser.add_argument('-i', dest='ignore_case', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    parser.add_argument('-v', dest='inverse_answer', action='store_true')
    parser.add_argument('-l', dest='only_files', action='store_true')
    parser.add_argument('-L', dest='inverse_only_files', action='store_true')

    args = parser.parse_args(args_str)

    return args


def compile_pattern(pattern: str, is_pattern_regex=False, ignore_case=False):
    if not is_pattern_regex:
        pattern = re.escape(pattern)
    return re.compile(pattern, flags=re.IGNORECASE) if ignore_case else re.compile(pattern)


def find_pattern_in_line(line: str, pattern: str, full_match=False) -> bool:
    if full_match:
        return bool(re.fullmatch(pattern, line))
    return bool(re.search(pattern, line))


def filter_matched_lines(lines: List[str], pattern, full_match=False,
                         inverse_answer=False) -> List[str]:
    return [line for line in lines
            if inverse_answer ^ find_pattern_in_line(line, pattern, full_match)]


def grep_from_lines(read_lines: List[str], pattern, is_only_count=False,
                    full_match=False, inverse_answer=False) -> List:
    filtered_lines = filter_matched_lines(read_lines, pattern, full_match, inverse_answer)
    if is_only_count:
        cnt = len(filtered_lines)
        return [cnt] if cnt or inverse_answer else []
    return filtered_lines


def strip_lines(lines: List[str]) -> List[str]:
    return [line.rstrip() for line in lines]


def find_lines_from_grep_files(files: str, pattern, is_only_count=False, full_match=False,
                               inverse_answer=False, only_files=False,
                               inverse_only_files=False) -> List[str]:
    filtered_lines: List[str] = []
    for file_name in files:
        try:
            with open(file_name, 'r') as in_file:
                lines = grep_from_lines(strip_lines(in_file.readlines()),
                                        pattern, is_only_count, full_match, inverse_answer)
                if only_files:
                    if lines:
                        filtered_lines += ['{}'.format(file_name)]
                elif inverse_only_files:
                    if not lines or lines == ['0'] and is_only_count:
                        filtered_lines += ['{}'.format(file_name)]
                else:
                    filtered_lines += ['{}{}'.format((file_name + ':') if len(files) > 1 else '',
                                                     line) for line in lines]
        except (OSError, IOError):
            print('{}:not found'.format(file_name), file=sys.stderr)
    return filtered_lines


def find_lines_from_grep_stdin(pattern, is_only_count=False, full_match=False,
                               inverse_answer=False) -> List[str]:
    return grep_from_lines(strip_lines(sys.stdin.readlines()),
                           pattern, is_only_count, full_match, inverse_answer)


def main(args_str: List[str]):
    args = parse_args(args_str)

    pattern = compile_pattern(args.pattern, args.regex, args.ignore_case)
    if args.files:
        lines = find_lines_from_grep_files(args.files, pattern, args.count,
                                           args.full_match, args.inverse_answer,
                                           args.only_files, args.inverse_only_files)
    else:
        lines = find_lines_from_grep_stdin(pattern, args.count, args.full_match,
                                           args.inverse_answer)

    for line in lines:
        print(line)


if __name__ == '__main__':
    main(sys.argv[1:])
