#!/usr/bin/env python3
from typing import List
from pathlib import Path
import sys
import re
import argparse


def print_for_lines(line: str,
                    is_countable: bool, counter: int):
    if is_countable:
        print(counter)
        return
    print(line)


def print_for_files(is_countable: bool, file_name: str,
                    count: int, string: List[str], files_len: int):
    if is_countable:
        print(file_name + ':' + str(count))
    elif not is_countable and not files_len == 1:
        for needle in string:
            print(file_name + ':' + needle)
    else:
        for needle in string:
            print(needle)


def for_files_with_file_names(files: List[str], pattern: str, is_countable: bool):
    for file_name in files:
        my_path = Path.cwd()
        file = my_path.joinpath(file_name)
        count = 0
        if file.exists() and file.is_file():
            with file.open() as in_file:
                string = []
                count = 0
                for line in in_file:
                    line = line.rstrip('\n')
                    if re.search(pattern, line):
                        count += 1
                        string.append(line)
            print_for_files(is_countable, file_name, count, string, len(files))
        else:
            print(f'Error: file {file_name} is not opened.')


def for_stdin(pattern: str, is_countable: bool):
    counter = 0
    if is_countable:
        for line in sys.stdin.readlines():
            line = line.rstrip('\n')
            if re.search(pattern, line):
                counter += 1
        print_for_lines('', is_countable, counter)
    else:
        for line in sys.stdin.readlines():
            line = line.rstrip('\n')
            if re.search(pattern, line):
                print_for_lines(line, False, 0)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='is_regex', action='store_true')
    parser.add_argument('-c', dest='is_countable', action='store_true')
    args = parser.parse_args(args_str)

    pattern = args.pattern if args.is_regex else re.escape(args.pattern)
    if args.files:
        for_files_with_file_names(args.files, pattern, args.is_countable)
    else:
        for_stdin(pattern, args.is_countable)


if __name__ == 'main':
    main(sys.argv[1:])
