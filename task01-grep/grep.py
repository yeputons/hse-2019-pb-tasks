#!/usr/bin/env python3
from typing import List
from typing import Callable
from typing import TextIO
import sys
import re
import argparse


# chooses search method for regular expressions depending on the flags in input
def search_string_as_regex(args: argparse.Namespace, line: str) -> bool:
    flag = 0
    if args.ignore_case:
        flag = re.IGNORECASE
    result: bool = False
    if args.full_match:
        result = bool(re.fullmatch(args.needle, line, flags=flag))
    else:
        result = bool(re.search(args.needle, line, flags=flag))
    if args.invert:
        return not result
    else:
        return result


# chooses search method for common strings depending on the flags in input
def search_string(args: argparse.Namespace, line: str) -> bool:
    if args.ignore_case:
        args.needle = args.needle.casefold()
        line = line.casefold()
    result: bool = False
    if args.full_match:
        result = args.needle == line
    else:
        result = args.needle in line
    if args.invert:
        return not result
    else:
        return result


# searches for needle in every line of the file
def parse(file: TextIO, args: argparse.Namespace, search_function: Callable, output: List[str]):
    for line in file.readlines():
        line = line.rstrip('\n')
        if search_function(args, line):
            output.append(line)


# print information about files depending on the flags in input
def print_output_for_file(args: argparse.Namespace, file: TextIO, output: List[str],
                          several_files: bool):
    if args.count:
        if several_files:
            print(f'{file.name}:', end='')
        print(len(output))
    elif args.with_entry:
        if len(output) > 1:
            print(file.name)
    elif args.without_entry:
        if len(output) == 0:
            print(file.name)
    else:
        for i in output:
            if several_files:
                print(f'{file.name}:', end='')
            print(i)


# uses library argparse to parse input
def parse_flags(args_str: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str, help='string that you want to search')
    parser.add_argument('files', nargs='*', default=[sys.stdin], type=argparse.FileType('r'),
                        help='files in which you want to search')
    parser.add_argument('-E', dest='regex', action='store_true',
                        help='search as regular expression')
    parser.add_argument('-i', dest='ignore_case', action='store_true',
                        help='ignore case of characters')
    parser.add_argument('-v', dest='invert', action='store_true',
                        help='invert the answer')
    parser.add_argument('-x', dest='full_match', action='store_true',
                        help='search for a complete string match')
    parser.add_argument('-c', dest='count', action='store_true',
                        help='print the number of entries')
    parser.add_argument('-l', dest='with_entry', action='store_true',
                        help='print names of files which contain needle')
    parser.add_argument('-L', dest='without_entry', action='store_true',
                        help="print names of files which DON'T contain needle")
    return parser.parse_args(args_str)


def main(args_str: List[str]):
    args = parse_flags(args_str)

    output: List[str] = list()

    search_function = search_string_as_regex if args.regex else search_string

    several_files = True if len(args.files) > 1 else False
    for file in args.files:
        output = list()
        parse(file, args, search_function, output)
        print_output_for_file(args, file, output, several_files)

    for file in args.files:
        file.close()


if __name__ == '__main__':
    main(sys.argv[1:])
