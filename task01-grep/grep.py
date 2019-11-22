#!/usr/bin/env python3

from typing import List, Callable
import sys
import re
import argparse


def names_to_strings(filenames: List[str]) -> List[List[str]]:
    res = []
    for name in filenames:
        with open(name, 'r') as file:
            res.append([string.rstrip('\n') for string in file.readlines()])
    return res


def stdin_to_strings() -> List[List[str]]:
    return [[string.rstrip('\n') for string in sys.stdin.readlines()]]


def match_string(string: str, pattern: str) -> bool:
    return pattern in string


def match_regex(string: str, pattern: str) -> bool:
    return bool(re.search(pattern, string))


def print_lines(strings: List[str], filename: str, is_alone: bool) -> None:
    for string in strings:
        if is_alone:
            print(string)
        else:
            print(f'{filename}:{string}')


def print_count(strings: List[str], filename: str, is_alone: bool) -> None:
    if is_alone:
        print(len(strings))
    else:
        print(f'{filename}:{len(strings)}')


def find_matched(file: List[str], pattern: str, match_f: Callable[[str, str], bool]) -> List[str]:
    return list(filter(lambda string: match_f(string, pattern), file))


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='print_count', action='store_true')
    parser.add_argument('files', nargs='*')
    args = parser.parse_args(args_str)

    filenames = args.files
    files = names_to_strings(filenames)
    if not filenames:
        files = stdin_to_strings()
        filenames = ['sys.stdin']
    match_f = match_string
    if args.regex:
        match_f = match_regex

    matched_strings = [find_matched(
        file, args.pattern, match_f) for file in files]

    print_function = print_lines
    if args.print_count:
        print_function = print_count

    for matches, name in zip(matched_strings, filenames):
        print_function(matches, name, len(filenames) == 1)


if __name__ == '__main__':
    main(sys.argv[1:])
