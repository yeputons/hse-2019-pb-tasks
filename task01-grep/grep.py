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
    # make regex out of standard mode pattern
    if not search_flags['regex']:
        pattern = re.escape(pattern)
    # regex mode
    re_flags = re.IGNORECASE if search_flags['ignore_case'] else 0
    if search_flags['full_match']:
        answer = bool(re.fullmatch(pattern, line, flags=re_flags))
    else:
        answer = bool(re.search(pattern, line, flags=re_flags))
    return not answer if search_flags['invert_ans'] else answer


def search_in_lines(pattern: str, input_lines: List[List], search_flags: Dict) -> Dict:
    found: Dict[str, List] = {}  # {filename or '': List of lines with pattern}
    for [filename, line] in input_lines:
        if filename not in found:
            found[filename] = []
        if search(pattern, line, search_flags):
            found[filename].append(line)
    return found


def print_answer(found: Dict, files: List, output_flags: Dict) -> None:
    ans_format = '{0}:{1}' if len(files) > 1 else '{1}'
    if output_flags['count_task']:  # flag -c
        print_ans_count(found, ans_format)

    elif output_flags['only_file_names_with']:  # flag -l
        print_ans_file_names(found, True)

    elif output_flags['only_file_names_without']:  # flag -L
        print_ans_file_names(found, False)

    else:  # print lines
        print_ans_lines(found, ans_format)


def print_ans_lines(found: Dict, answer_format: str) -> None:
    for filename in found:
        for line in found[filename]:
            print(answer_format.format(filename, line))


def print_ans_count(found: Dict, answer_format: str) -> None:
    for filename in found:
        print(answer_format.format(filename, len(found[filename])))


def print_ans_file_names(found: Dict, with_found: bool) -> None:
    for filename in found:
        if with_found == (len(found[filename]) > 0):
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
    output_flags: Dict[str, bool] = {'count_task': args.count_task,
                                     'only_file_names_with': args.only_file_names_with,
                                     'only_file_names_without': args.only_file_names_without}
    print_answer(found, args.files, output_flags)


if __name__ == '__main__':
    main(sys.argv[1:])
