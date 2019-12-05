#!/usr/bin/env python3
from typing import Tuple, List, TextIO
import sys
import re
import argparse


MATCHING_ARGS = ('regex', 'full_match', 'ignore_case', 'inverse')
OUTPUT_ARGS = ('count', 'files_with_matches', 'files_without_matches')


def find_in_str(pattern: str, s: str, matching_args: List[str]) -> bool:
    result: bool
    if 'regex' in matching_args:
        flags = re.IGNORECASE if 'ignore_case' in matching_args else 0
        if 'full_match' in matching_args:
            result = bool(re.fullmatch(pattern, s, flags=flags))
        else:
            result = bool(re.search(pattern, s, flags=flags))
    else:
        if 'ignore_case' in matching_args:
            pattern = pattern.lower()
            s = s.lower()
        if 'full_match' in matching_args:
            result = pattern == s
        else:
            result = pattern in s
    if 'inverse' in matching_args:
        result = not result
    return result


def get_matching_args(args: argparse.Namespace) -> List[str]:
    return [arg for arg, value in vars(args).items() if (arg in MATCHING_ARGS) and value]


def get_output_args(args: argparse.Namespace) -> List[str]:
    return [arg for arg, value in vars(args).items() if (arg in OUTPUT_ARGS) and value]


def find_in_files_or_stdin(  # find in files or in stdin if files empty
        files: List[str],
        pattern: str,
        matching_args: List[str]) -> List[Tuple[str, List[str]]]:
    
    def find_in_file(
            file: TextIO,
            pattern: str,
            matching_args: List[str]
            ) -> List[str]:
        lines = map(lambda line: line.rstrip('\n'), file)
        return list(filter(lambda line: find_in_str(pattern, line, matching_args), lines))


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


def get_output_format(matches_len: int, output_args: List[str]) -> str:
    if 'files_with_matches' in output_args or 'files_without_matches' in output_args:
        return '{0}'
    elif matches_len == 1:
        return '{1}'
    else:
        return '{0}:{1}'


def print_matches(
        all_matches: List[Tuple[str, List[str]]],
        output_args: List[str],
        output_format: str) -> None:

    if 'files_with_matches' in output_args or 'files_without_matches' in output_args:
        all_matches = list(filter(
            lambda matches: matches[1] if 'files_with_matches' in output_args else not matches[1],
            all_matches))
        for filename, matches in all_matches:
            print(output_format.format(filename))
    elif 'count' in output_args:
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
    parser.add_argument('-v', dest='inverse', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-l', dest='files_with_matches', action='store_true')
    parser.add_argument('-L', dest='files_without_matches', action='store_true')
    args = parser.parse_args(args_str)

    matches = find_in_files_or_stdin(args.files, args.needle, get_matching_args(args))
    output_args = get_output_args(args)
    output_format = get_output_format(len(matches), output_args)
    print_matches(matches, output_args, output_format)


if __name__ == '__main__':
    main(sys.argv[1:])
