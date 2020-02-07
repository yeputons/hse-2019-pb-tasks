#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def substr_search(needle: str, line: str, flags: bool, full_match: bool) -> bool:
    if flags:
        needle = needle.lower()
        line = line.lower()

    if full_match:
        return needle == line

    return needle in line


def parse_lines(lines: list) -> list:
    result = []
    for line in lines:
        line = line.rstrip('\n')
        result.append(line)
    return result


def match_string(needle: str, line: str, regex: bool,
                 ignore_case: bool, reverse: bool, full_match: bool) -> bool:
    if regex:
        if full_match:
            return bool(re.fullmatch(needle, line,
                                     flags=re.IGNORECASE if ignore_case else 0)) ^ reverse
        return bool(re.search(needle, line, flags=re.IGNORECASE if ignore_case else 0)) ^ reverse
    else:
        return substr_search(needle, line, flags=ignore_case, full_match=full_match) ^ reverse


def read_files(files: list) -> dict:
    lines = dict()
    for file in files:
        with open(file, 'r') as in_file:
            lines[file] = parse_lines(in_file.readlines())
    return lines


def read_stdin() -> dict:
    lines = dict()
    lines[''] = parse_lines(sys.stdin.readlines())
    return lines


def filter_lines(lines: dict, needle: str, regex: bool,
                 ignore_case: bool, reverse: bool, full_match: bool) -> dict:
    result = dict()
    for file in lines:
        filtered_file = []
        for line in lines[file]:
            if match_string(needle, line, regex, ignore_case, reverse, full_match):
                filtered_file.append(line)
        result[file] = filtered_file
    return result


def print_answer_count(filtered_lines: dict) -> None:
    for file in filtered_lines:
        if len(filtered_lines) == 1:
            print(len(filtered_lines[file]))
        else:
            print(f'{file}:{len(filtered_lines[file])}')


def print_answer_files_only(filtered_lines: dict, reverse_files_only: bool) -> None:
    for file in filtered_lines:
        if bool(len(filtered_lines[file])) ^ reverse_files_only:
            print(file)


def print_answer_default(filtered_lines: dict) -> None:
    for file in filtered_lines:
        for line in filtered_lines[file]:
            if len(filtered_lines) == 1:
                print(line)
            else:
                print(f'{file}:{line}')


def print_answer(filtered_lines: dict, count_flag: bool,
                 files_only: bool, reverse_files_only: bool) -> None:
    if count_flag:
        print_answer_count(filtered_lines)
    elif files_only or reverse_files_only:
        print_answer_files_only(filtered_lines, reverse_files_only)
    else:
        print_answer_default(filtered_lines)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-i', dest='ignore_case', action='store_true')
    parser.add_argument('-v', dest='reverse', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    parser.add_argument('-l', dest='files_only', action='store_true')
    parser.add_argument('-L', dest='reverse_files_only', action='store_true')

    args = parser.parse_args(args_str)

    if args.files:
        lines = read_files(args.files)
    else:
        lines = read_stdin()

    filtered_lines = filter_lines(lines, args.needle, args.regex, args.ignore_case, args.reverse,
                                  args.full_match)
    print_answer(filtered_lines, args.count, args.files_only, args.reverse_files_only)


if __name__ == '__main__':
    main(sys.argv[1:])
