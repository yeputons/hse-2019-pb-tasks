#!/usr/bin/env python3
from typing import List, IO, Union
import sys
import re
import argparse


def match(line: str, needle: str, *, regex: bool, lowercase: bool,
          full_match: bool, invert: bool) -> bool:
    flags = re.IGNORECASE if lowercase else 0
    pattern = needle if regex else re.escape(needle)
    res = bool(re.fullmatch(pattern, line, flags=flags)) if full_match \
        else bool(re.search(pattern, line, flags=flags))
    return not res if invert else res


def get_matching_lines(source: IO[str], needle: str, *, regex: bool, invert: bool,
                       lowercase: bool, full_match: bool) -> List[str]:
    raw_list = [line.rstrip('\n') for line in source]
    filter_list = [line for line in raw_list if
                   match(line, needle, regex=regex, lowercase=lowercase,
                         full_match=full_match, invert=invert)]
    return filter_list


def formatted_output(count_files: int, file: Union[str, None], list_: List[str], *,
                     files_only: bool, invert_files: bool, count: bool) -> None:
    format_ = len(list_) if count else list_
    if not files_only and not invert_files:
        if format_:
            if file is None or count_files == 1:
                print(format_, sep='\n') if type(format_) == int else print(*format_, sep='\n')
            else:
                if type(format_) == int:
                    print(f'{file}:{format_}', sep='\n')
                else:
                    for item in format_:
                        print(f'{file}:{item}', sep='\n')
    else:
        if files_only and format_ or invert_files and not format_:
            print(file, sep='\n')


def parse_std_in(needle: str, *, regex: bool, count: bool, invert: bool,
                 lowercase: bool, full_match: bool) -> None:
    lines_to_print = get_matching_lines(sys.stdin, needle, regex=regex, invert=invert,
                                        lowercase=lowercase, full_match=full_match)
    formatted_output(0, None, lines_to_print, files_only=False, invert_files=False, count=count)


def parse_files(files: List[str], needle: str, *, regex: bool, count: bool, invert: bool,
                lowercase: bool, full_match: bool, files_only: bool, invert_files: bool) -> None:
    count_files = len(files)
    for file in files:
        with open(file, 'r') as file_item:
            lines_to_print = get_matching_lines(file_item, needle, regex=regex, invert=invert,
                                                lowercase=lowercase, full_match=full_match)
            formatted_output(count_files, file, lines_to_print, files_only=files_only,
                             invert_files=invert_files, count=count)


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
        parse_files(args.files, args.needle, regex=args.regex, count=args.count, invert=args.invert,
                    lowercase=args.lowercase, full_match=args.full_match,
                    files_only=args.files_only, invert_files=args.invert_files)
    else:
        parse_std_in(args.needle, regex=args.regex, count=args.count, invert=args.invert,
                     lowercase=args.lowercase, full_match=args.full_match)


if __name__ == '__main__':
    main(sys.argv[1:])
