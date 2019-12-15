#!/usr/bin/env python3
from typing import List, IO
import sys
import re
import argparse


def match(line: str, needle: str, *, regex: bool, low: bool, full_match: bool, inv: bool) -> bool:
    flags = re.IGNORECASE if low else 0
    pattern = needle if regex else re.escape(needle)
    res = bool(re.fullmatch(pattern, line, flags=flags)) if full_match \
        else bool(re.search(pattern, line, flags=flags))
    return not res if inv else res


def form_the_list(source: IO[str], needle: str, *, regex: bool, count: bool, inv: bool,
                  low: bool, full_match: bool) -> List[str]:
    raw_list = [line.rstrip('\n') for line in source]
    filter_list = [line for line in raw_list
                   if match(line, needle, regex=regex, low=low, full_match=full_match, inv=inv)]
    return [str(len(filter_list))] if count else filter_list


def formatted_output(file: str, list_: List[str], *, files_only: bool, invert_files: bool) -> None:
    if files_only and list_ or invert_files and not list_:
        print(file, sep='\n')
    elif not files_only and not invert_files:
        for item in list_:
            print(f'{file}:{item}', sep='\n')


def parse_std_in(needle: str, *, regex: bool, count: bool, inv: bool,
                 low: bool, full_match: bool) -> None:
    lines_to_print = form_the_list(sys.stdin, needle, regex=regex, count=count,
                                   inv=inv, low=low, full_match=full_match)
    if lines_to_print:
        print(*lines_to_print, sep='\n')


def parse_files(files: List[str], needle: str, *, regex: bool, count: bool, inv: bool, low: bool,
                full_match: bool, files_only: bool, invert_files: bool) -> None:
    for file in files:
        with open(file, 'r') as file_item:
            lines_to_print = form_the_list(file_item, needle, regex=regex, count=count,
                                           inv=inv, low=low, full_match=full_match)
        if len(files) == 1 and lines_to_print and not files_only:
            print(*lines_to_print, sep='\n')
        else:
            formatted_output(file, lines_to_print, files_only=files_only, invert_files=invert_files)


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
        parse_files(args.files, args.needle, regex=args.regex, count=args.count, inv=args.invert,
                    low=args.lowercase, full_match=args.full_match, files_only=args.files_only,
                    invert_files=args.invert_files)
    else:
        parse_std_in(args.needle, regex=args.regex, count=args.count, inv=args.invert,
                     low=args.lowercase, full_match=args.full_match)


if __name__ == '__main__':
    main(sys.argv[1:])
