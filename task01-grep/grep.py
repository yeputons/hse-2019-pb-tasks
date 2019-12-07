#!/usr/bin/env python3
from typing import List, Dict
import sys
import re
import argparse


def read_files(files: List) -> List:
    res = []
    for file in files:
        with open(file, 'r') as in_file:
            for line in in_file.readlines():
                res.append([file, line.rstrip('\n')])
    return res


def read_stdin() -> List:
    return [['', line.rstrip('\n')] for line in sys.stdin.readlines()]


def search(pattern: str, line: str, regex: bool) -> bool:
    return bool(re.search(pattern, line)) if regex else pattern in line


def search_in_lines(pattern: str, input_lines: List[List], regex: bool) -> Dict:
    found: Dict[str, List] = {}  # {filename or '': List of lines with pattern}
    for [filename, line] in input_lines:
        if filename not in found:
            found[filename] = []
        if search(pattern, line, regex):
            found[filename].append(line)
    return found


def print_ans_lines(found: Dict, files: List, answer_format: str) -> None:
    for filename in files:  # filename = '' as stdin
        for line in found[filename]:
            print(answer_format.format(filename, line))


def print_ans_count(found: Dict, files: List, answer_format: str) -> None:
    for filename in files:
        print(answer_format.format(filename, len(found[filename])))


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='count_task', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    args = parser.parse_args(args_str)

    input_lines: List[List] = []  # List of objs: obj = [filename or '' for stdin, line]
    if args.files:
        input_lines = read_files(args.files)
    else:
        input_lines = read_stdin()

    # find answer
    found = search_in_lines(args.needle, input_lines, args.regex)

    # print answer
    ans_format = '{0}:{1}' if len(args.files) > 1 else '{1}'
    if args.count_task:  # flag -c
        print_ans_count(found, args.files if args.files else [''], ans_format)
    else:  # print lines
        print_ans_lines(found, args.files if args.files else [''], ans_format)


if __name__ == '__main__':
    main(sys.argv[1:])
