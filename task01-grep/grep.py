#!/usr/bin/env python3
from typing import List, IO
import sys
import re
import argparse


def find(line: str, needle: str, regex: bool) -> bool:
    if regex:
        return bool(re.search(needle, line))
    pattern = re.escape(needle)
    return bool(re.search(pattern, line))


def make_list(source: IO[str], needle: str, regex: bool, count_flag: bool) -> List[str]:
    raw_list = [line.rstrip('\n') for line in source if find(line, needle, regex)]
    filter_list = [str(len(raw_list))] if count_flag else raw_list
    return filter_list


def parse_std_in(needle: str, regex: bool, count_flag: bool) -> None:
    to_print_list = make_list(sys.stdin, needle, regex, count_flag)
    print(*to_print_list, sep='\n')


def parse_files(files: List[str], needle: str, regex: bool, count_flag: bool) -> None:
    for file in files:
        with open(file, 'r') as file_item:
            to_print_list = make_list(file_item, needle, regex, count_flag)
        if len(files) == 1:
            print(*to_print_list, sep='\n')
        else:
            for item in to_print_list:
                print(f'{file}:{item}', sep='\n')


def main(args_str: List[str]):
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
