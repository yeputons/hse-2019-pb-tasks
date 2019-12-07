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


def search(pattern: str, line: str, search_flags: Dict) -> bool:
    answer: bool
    # regex mode
    if search_flags['regex']:
        re_flags = re.IGNORECASE if search_flags['ignore_case'] else 0
        if search_flags['full_match']:
            answer = bool(re.fullmatch(pattern, line, flags=re_flags))
        else:
            answer = bool(re.search(pattern, line, flags=re_flags))
        return not answer if search_flags['invert_ans'] else answer
    # standard mode
    if search_flags['ignore_case']:
        pattern = pattern.lower()
        line = line.lower()
    answer = pattern == line if search_flags['full_match'] else pattern in line
    return not answer if search_flags['invert_ans'] else answer


def search_in_lines(pattern: str, input_lines: List[List], search_flags: Dict) -> Dict:
    found: Dict[str, List] = {}  # {filename or '': List of lines with pattern}
    for [filename, line] in input_lines:
        if filename not in found:
            found[filename] = []
        if search(pattern, line, search_flags):
            found[filename].append(line)
    return found


def print_ans_lines(found: Dict, files: List, answer_format: str) -> None:
    for filename in files:  # filename = '' as stdin
        for line in found[filename]:
            print(answer_format.format(filename, line))


def print_ans_count(found: Dict, files: List, answer_format: str) -> None:
    for filename in files:
        print(answer_format.format(filename, len(found[filename])))


def print_ans_file_names(found: Dict, files: List, with_found: bool) -> None:
    for filename in files:
        if with_found == len(found[filename]) > 0:
            print(filename)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    # output mode keys
    parser.add_argument('-c', dest='count_task', action='store_true')
    parser.add_argument('-l', dest='only_file_names_with', action='store_true')
    parser.add_argument('-L', dest='only_file_names_without', action='store_true')
    # search mode keys
    parser.add_argument('-i', dest='ignore_case', action='store_true')
    parser.add_argument('-v', dest='invert_ans', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    args = parser.parse_args(args_str)

    input_lines: List[List] = []  # List of objs: obj = [filename or '' for stdin, line]
    if args.files:
        input_lines = read_files(args.files)
    else:
        input_lines = read_stdin()

    search_flags: Dict[str, bool] = {'ignore_case': args.ignore_case, 'invert_ans': args.invert_ans,
                                     'full_match': args.full_match, 'regex': args.regex}
    # find answer
    found = search_in_lines(args.needle, input_lines, search_flags)

    # print answer
    ans_format = '{0}:{1}' if len(args.files) > 1 else '{1}'
    if args.count_task:  # flag -c
        print_ans_count(found, args.files if args.files else [''], ans_format)

    elif args.only_file_names_with:  # flag -l
        print_ans_file_names(found, args.files, True)

    elif args.only_file_names_with:  # flag -l
        print_ans_file_names(found, args.files, False)

    else:  # print lines
        print_ans_lines(found, args.files if args.files else [''], ans_format)


if __name__ == '__main__':
    main(sys.argv[1:])
