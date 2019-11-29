#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def parse_lines(lines):
    result = []
    for line in lines:
        line = line.rstrip('\n')
        result.append(line)
    return result



def match_string(needle=str, line=str, regex=bool):
    if regex:
        return bool(re.search(needle, line))
    else:
        return (needle in line)


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


def filter_lines(lines=dict, needle=str, regex=bool):
    result = dict()
    for file in lines:
        filtered_file = []
        for line in lines[file]:
            assert(type(line) == str)
            if match_string(needle, line, regex):
                filtered_file.append(line)
        result[file] = filtered_file
    return result


def count_lines(lines=dict, needle=str, regex=bool):
    result = dict()
    result = filter_lines(lines, needle, regex)
    for file in result:
        result[file] = [len(result[file])]
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
    args = parser.parse_args(args_str)
    lines = dict()
    filtered_lines = dict()
    if args.files:
        lines = read_files(args.files)
    else:
        lines = read_stdin()
    if args.count:
        result = count_lines(lines, args.needle, args.regex)
        print_answer(result)
    else:
        filtered_lines = filter_lines(lines, args.needle, args.regex)
        print_answer(filtered_lines)



if __name__ == '__main__':
    main(sys.argv[1:])
