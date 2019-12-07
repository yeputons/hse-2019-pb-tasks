#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def search_substring(needle: str, line: str, ignore_case: bool, full_match: bool) -> bool:
    if ignore_case:
        needle = needle.lower()
        line = line.lower()

    if full_match:
        return needle == line

    return needle in line


def parse_lines(lines: list) -> list:
    result = [line.rstrip('\n') for line in lines]
    return result


def match_string(needle: str, line: str, regex: bool,
                 ignore_case: bool, reverse: bool, full_match: bool) -> bool:
    if regex:
        if full_match:
            result = bool(re.fullmatch(needle, line, flags=re.IGNORECASE * ignore_case))
        else:
            result = bool(re.search(needle, line, flags=re.IGNORECASE * ignore_case))
    else:
        result = search_substring(needle, line, ignore_case=ignore_case, full_match=full_match)
    return result ^ reverse


def read_files(files: list) -> dict:
    lines = {}
    for file in files:
        with open(file, 'r') as in_file:
            lines[file] = parse_lines(in_file.readlines())
    return lines


def read_stdin() -> dict:
    lines = {}
    lines[''] = parse_lines(sys.stdin.readlines())
    return lines


def filter_lines(unfiltered_lists: dict, needle: str, regex: bool, ignore_case: bool, reverse: bool,
                 full_match: bool, reverse_files: bool) -> dict:
    result = {}
    for lines_list in unfiltered_lists:
        filtered_list = [line for line in unfiltered_lists[lines_list]
                         if match_string(needle, line, regex, ignore_case, reverse, full_match)]
        result[lines_list] = filtered_list
    return result


def count_lines(lines: dict) -> dict:
    result = {}
    for file in lines:
        result[file] = [len(lines[file])]
    return result


def format_answer(filtered_lines: dict, mute_files: bool, reverse_files: bool):
    selected_files = [file for file in filtered_lines]
    result = ''
    for file in selected_files:
        if mute_files:
            result += (file + '\n') * ((filtered_lines[file] != []) ^ reverse_files)
        else:
            for line in filtered_lines[file]:
                if len(filtered_lines) == 1:
                    result += str(line) + '\n'
                else:
                    result += f'{file}:{line}\n'
    return result[:-1]


def print_answer(answer: str):
    print(answer)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-i', dest='ignore_case', action='store_true')
    parser.add_argument('-v', dest='reverse', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    parser.add_argument('-l', dest='mute_files', action='store_true')
    parser.add_argument('-L', dest='reverse_files', action='store_true')
    args = parser.parse_args(args_str)
    if args.reverse_files:
        args.mute_files = 1
    if args.files:
        lines = read_files(args.files)
    else:
        lines = read_stdin()
    filtered_lines = filter_lines(lines, args.needle, args.regex, args.ignore_case,
                                  args.reverse, args.full_match, args.reverse_files)
    if args.count:
        filtered_lines = count_lines(filtered_lines)
    print_answer(format_answer(filtered_lines, args.mute_files, args.reverse_files))


if __name__ == '__main__':
    main(sys.argv[1:])
