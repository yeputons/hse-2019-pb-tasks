#!/usr/bin/env python3
from typing import List, IO
import sys
import re
import argparse


def find(line: str, needle: str, regex: bool) -> bool:
    pattern = needle if regex else re.escape(needle)
    return bool(re.search(pattern, line))


def make_list(source: IO[str], needle: str, regex: bool, count_flag: bool) -> List[str]:
    raw_list = [line.rstrip('\n') for line in source]
    filter_list = [line for line in raw_list if find(line, needle, regex)]
    return [str(len(filter_list))] if count_flag else filter_list


def parse_std_in(needle: str, regex: bool, count_flag: bool) -> None:
    lines_to_print = make_list(sys.stdin, needle, regex, count_flag)
    print(*lines_to_print, sep='\n')


def parse_files(files: List[str], needle: str, regex: bool, count_flag: bool) -> None:
    for file in files:
        with open(file, 'r') as file_item:
            lines_to_print = make_list(file_item, needle, regex, count_flag)
        if len(files) == 1:
            print(*lines_to_print)
        else:
            for item in lines_to_print:
                print(f'{file}:{item}', sep='\n')


def main(args_str: List[str]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')

    args = parser.parse_args(args_str)

    if args.files:
        parse_files(args.files, args.needle, args.regex, args.count)
    else:
        parse_std_in(args.needle, args.regex, args.count)


if __name__ == '__main__':
    main(sys.argv[1:])
