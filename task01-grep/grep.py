#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def format_lines(filename, line):
    return f'{filename}:{line}'


def print_result(result):
    for line in result:
        print(line)


def match_pattern(is_regex, pattern, line):
    if is_regex:
        return re.search(pattern, line)
    else:
        return pattern in line


def filter_lines(is_regex, pattern, lines):
    return [line for line in lines if match_pattern(is_regex, pattern, line)]


def grep_lines(lines, filename, pattern, is_regex, counting_mode):
    result = filter_lines(is_regex, pattern, lines)
    if counting_mode:
        result = [str(len(result))]
    if filename:
        result = [format_lines(filename, line) for line in result]
    return result


def strip_lines(file):
    return [line.rstrip('\n') for line in file]


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    args = parser.parse_args(args_str)
    if not args.files:
        lines = strip_lines(sys.stdin.readlines())
        print_result(grep_lines(lines, '', args.needle, args.regex, args.count))
    else:
        for filename in args.files:
            with open(filename, 'r') as in_file:
                lines = strip_lines(in_file.readlines())
                print_result(grep_lines(lines, filename if len(args.files) > 1 else None,
                                        args.needle, args.regex, args.count))


if __name__ == '__main__':
    main(sys.argv[1:])
