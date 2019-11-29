#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def substr_search(needle=str, line=str, flags=bool, full_match=bool):
    if flags:
        needle = needle.lower()
        line = line.lower()

    if full_match:
        return needle == line

    return needle in line



def parse_lines(lines):
    result = []
    for line in lines:
        line = line.rstrip('\n')
        result.append(line)
    return result



def match_string(needle=str, line=str, regex=bool, ignore_case=bool, reverse=bool, full_match=bool):
    flags = False
    if ignore_case:
        flags = re.IGNORECASE
    if regex:
        if (full_match):
            return bool(re.fullmatch(needle, line, flags=flags)) ^ reverse
        return bool(re.search(needle, line, flags=flags)) ^ reverse
    else:
        return substr_search(needle, line, flags=flags, full_match=full_match) ^ reverse


def read_files(files):
    lines = dict()
    for file in files:
        with open(file, 'r') as in_file:
            lines[file] = parse_lines(in_file.readlines())
    return lines


def read_stdin():
    lines = dict()
    lines[''] = parse_lines(sys.stdin.readlines())
    return lines


def filter_lines(lines=dict, needle=str, regex=bool, ignore_case=bool, reverse=bool, full_match=bool):
    result = dict()
    for file in lines:
        filtered_file = []
        for line in lines[file]:
            if match_string(needle, line, regex, ignore_case, reverse, full_match):
                filtered_file.append(line)
        result[file] = filtered_file
    return result


def count_lines(lines=dict):
    result = dict()
    for file in lines:
        result[file] = [len(lines[file])]
    return result


def print_answer(filtered_lines):
    for file in filtered_lines:
        for line in filtered_lines[file]:
            if (len(filtered_lines) == 1):
                print(line)
            else:
                print(f'{file}:{line}')


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

    lines = dict()
    filtered_lines = dict()
    if args.files:
        lines = read_files(args.files)
    else:
        lines = read_stdin()

    filtered_lines = filter_lines(lines, args.needle, args.regex, args.ignore_case, args.reverse, args.full_match)
    if args.count:
        filtered_lines = count_lines(filtered_lines)
    print_answer(filtered_lines)



if __name__ == '__main__':
    main(sys.argv[1:])
