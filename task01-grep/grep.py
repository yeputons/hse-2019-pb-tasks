#!/usr/bin/env python3
from typing import Tuple, List, TextIO
import sys
import re
import argparse


def find_in_str(pattern: str, s: str, matching_args: List[str]) -> bool:
    if 'regex' in matching_args:
        flags = re.IGNORECASE if 'ignore case' in matching_args else 0
        if 'full match' in matching_args:
            return bool(re.fullmatch(pattern, s, flags=flags))
        else:
            return bool(re.search(pattern, s, flags=flags))
    else:
        if 'ignore case' in matching_args:
            pattern = pattern.lower()
            s = s.lower()
        if 'full match' in matching_args:
            return pattern == s
        else:
            return pattern in s


def get_matching_args(args: argparse.Namespace) -> List[str]:
    matching_args = []
    if args.regex:
        matching_args.append('regex')
    if args.ignore_case:
        matching_args.append('ignore case')
    if args.full_match:
        matching_args.append('full match')
    return matching_args


def find_in_file(
        file: TextIO,
        pattern: str,
        matching_args: List[str]
        ) -> List[str]:

    lines = map(lambda line: line.rstrip('\n'), file)
    return [line for line in lines if find_in_str(pattern, line, matching_args)]


def find_in_files_or_stdin(  # find in files or in stdin if files empty
        files: List[str],
        pattern: str,
        matching_args: List[str]) -> List[Tuple[str, List[str]]]:

    matches = []

    if files:
        for filename in files:
            with open(filename, 'r') as file:
                matches.append((filename, find_in_file(file, pattern, matching_args)))
    else:
        matches = [('stdin', find_in_file(sys.stdin, pattern, matching_args))]

    return matches


def to_count(matches: List[Tuple[str, List[str]]]) -> List[Tuple[str, int]]:
    return [(filename, len(lines)) for filename, lines in matches]


def print_matches(all_matches: List[Tuple[str, List[str]]], print_count: bool) -> None:
    output_format = '{1}' if len(all_matches) == 1 else '{0}:{1}'

    if print_count:
        all_matches_cnt = to_count(all_matches)
        for filename, cnt in all_matches_cnt:
            print(output_format.format(filename, cnt))
    else:
        for filename, matches in all_matches:
            for match in matches:
                print(output_format.format(filename, match))


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-i', dest='ignore_case', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    args = parser.parse_args(args_str)

    matches = find_in_files_or_stdin(args.files, args.needle, get_matching_args(args))
    print_matches(matches, args.count)


if __name__ == '__main__':
    main(sys.argv[1:])
