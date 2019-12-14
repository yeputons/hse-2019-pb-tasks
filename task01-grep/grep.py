#!/usr/bin/env python3
from typing import List, Iterable, Tuple
from typing import Iterator, Pattern, Callable


import sys
import re
import argparse


def rstrip_lines(lines: Iterable[str]) -> List[str]:
    return [line.rstrip('\n') for line in lines]


def compile_pattern(pattern: str, regex_flag: bool, ignore_case: bool) -> Pattern:
    if not regex_flag:
        pattern = re.escape(pattern)
    flags = re.I if ignore_case else 0
    return re.compile(pattern, flags=flags)


def get_find_function(re_pattern: Pattern,
                      full_match: bool, invert: bool) -> Callable[[str], bool]:
    find = re.fullmatch if full_match else re.search
    return lambda line: bool(find(pattern=re_pattern, string=line)) ^ invert


def filter_blocks(blocks: List[List[str]], find: Callable[[str], bool]) -> List[List[str]]:
    return [list(filter(find, lines)) for lines in blocks]


def count_lines(blocks: List[List[str]]) -> List[List[str]]:
    return [[str(len(lines))] for lines in blocks]


def add_filename_prefix(lines_source_tuple: Tuple[List[str], str]) -> List[str]:
    lines, source = lines_source_tuple
    return [f'{source}:{line}' for line in lines]


def print_file_name_only(blocks_and_sources_list: Iterator[Tuple[List[str], str]],
                         file_name_only: bool) -> None:
    for lines_source_tuple in blocks_and_sources_list:
        lines, source = lines_source_tuple
        if file_name_only ^ (len(lines) <= 0):
            print(source)


def print_blocks(blocks: List[List[str]]) -> None:
    for lines in blocks:
        for line in lines:
            print(line)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-l', dest='file_name_only', action='store_true')
    parser.add_argument('-L', dest='invert_file_name_only', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-i', dest='ignore_case', action='store_true')
    parser.add_argument('-v', dest='invert', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    args = parser.parse_args(args_str)

    blocks: List[List[str]] = []
    for file_name in args.files:
        with open(file_name, 'r') as file:
            blocks.append(rstrip_lines(file))
    if not args.files:
        blocks.append(rstrip_lines(sys.stdin))

    sources: List[str] = args.files
    if not sources:
        sources = ['_stdin_']

    re_pattern = compile_pattern(args.pattern, args.regex, args.ignore_case)
    find = get_find_function(re_pattern, args.full_match, args.invert)
    blocks = filter_blocks(blocks, find)

    if args.count:
        blocks = count_lines(blocks)
    if len(sources) > 1:
        blocks = list(map(add_filename_prefix, zip(blocks, sources)))

    if args.file_name_only or args.invert_file_name_only:
        print_file_name_only(zip(blocks, sources), args.file_name_only)
    else:
        print_blocks(blocks)


if __name__ == '__main__':
    main(sys.argv[1:])
