#!/usr/bin/env python3
from typing import List, IO, Union
import sys
import re
import argparse


def make_flag(lowercase: bool) -> Union[int, ]:  # RegexFlag
    return re.IGNORECASE if lowercase else 0


def invert_f(invert: bool, find_bool: bool) -> bool:
    return not find_bool if invert else find_bool


def find(line: str, needle: str, regex: bool, lowercase: bool, full_match: bool) -> bool:
    pattern = needle if regex else re.escape(needle)
    return bool(re.fullmatch(pattern, line, flags=make_flag(lowercase))) if full_match \
        else bool(re.search(pattern, line, flags=make_flag(lowercase)))


def make_list(source: IO[str], needle: str, regex: bool, count_flag: bool, invert: bool,
              lowercase: bool, full_match: bool) -> List[str]:
    raw_list = [line.rstrip('\n') for line in source]
    filter_list = [line for line in raw_list if
                   invert_f(find(line, needle, regex, lowercase, full_match), invert)]
    return [str(len(filter_list))] if count_flag else filter_list


def print_list(file: str, list_: List[str], files_only: bool, invert_files: bool) -> None:
    if files_only and len(list_) != 0:
        print(f'{file}')
    elif invert_files and len(list_) == 0:
        print(f'{file}')
    elif not files_only and not invert_files:
        for item in list_:
            print(f'{file}:{item}', sep='\n')


def parse_std_in(needle: str, regex: bool, count_flag: bool, invert: bool,
                 lowercase: bool, full_match: bool) -> None:
    lines_to_print = make_list(sys.stdin, needle, regex, count_flag, invert, lowercase, full_match)
    print(*lines_to_print, sep='\n')


def parse_files(files: List[str], needle: str, regex: bool, count_flag: bool, invert: bool,
                lowercase: bool,
                full_match: bool, files_only: bool, invert_files: bool) -> None:
    for file in files:
        with open(file, 'r') as file_item:
            lines_to_print = make_list(file_item, needle, regex, count_flag, invert,
                                       lowercase, full_match)
        if len(files) == 1:
            print(*lines_to_print)
        else:
            print_list(file, lines_to_print, files_only, invert_files)


def main(args_str: List[str]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-l', dest='files_only', action='store_true')
    parser.add_argument('-L', dest='invert_files', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-i', dest='lowercase', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    parser.add_argument('-v', dest='invert', action='store_true')
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')

    args = parser.parse_args(args_str)

    if args.files:
        parse_files(args.files, args.needle, args.regex, args.count, args.invert, args.lowercase,
                    args.full_match, args.files_only, args.invert_files)
    else:
        parse_std_in(args.needle, args.regex, args.count, args.invert, args.lowercase,
                     args.full_match)


if __name__ == '__main__':
    main(sys.argv[1:])
