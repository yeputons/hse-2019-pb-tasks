#!/usr/bin/env python3

from typing import List
from typing import Dict

import sys
import re
import argparse

REGEX = 'regex'
IGNORE_CASE = 'ignore_case'
INVERTED = 'invert_result'


def match(needle: str, line: str, flags: Dict[str, bool]) -> bool:
    ignoring_case = flags.get(
        IGNORE_CASE) is not None and flags.get(IGNORE_CASE)
    if flags.get(REGEX) is not None and flags.get(REGEX):
        return re.search(needle, line, flags=re.IGNORECASE if ignoring_case else 0) is not None
    if ignoring_case:
        return needle.lower() in line.lower()
    return needle in line


def preproccesing(data: List[str]) -> List[str]:
    return [line.rstrip('\n') for line in data]


def search_needle_in_src(needle: str, source: List[str],
                         flags: Dict[str, bool]) -> List[str]:

    inverted = flags.get(INVERTED) is not None and flags.get(INVERTED)
    appearances = []
    for line in source:
        matches = match(needle, line, flags)
        if (matches and not inverted) or (not matches and inverted):
            appearances.append(line)
    return appearances


def print_search_result(res: Dict[str, List[str]],
                        count: bool = False):
    for key, value in res.items():
        source: str = key+':' if len(res) > 1 else ''
        if count:
            print(f'{source}{len(value)}')
            continue
        for line in value:
            print(f'{source}{line}')


def main(arg_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        dest='count_mode',
                        action='store_true',
                        help='count the number of appereance of needle')
    parser.add_argument('-E',
                        dest='regex_mode',
                        action='store_true',
                        help='perceive a needle as a regex')
    parser.add_argument('-i',
                        dest='ignore_case',
                        action='store_true',
                        help='ignoring case of a needle')
    parser.add_argument('-v',
                        dest='invert_result',
                        action='store_true',
                        help='invert a result i.e. all found lines turn out not found')
    parser.add_argument('needle',
                        type=str,
                        nargs=1,
                        help='a string(or a regex) to search for')
    parser.add_argument('files',
                        nargs='*',
                        help='a sources where to search (default: stdin)')
    args = parser.parse_args(arg_str)
    res: Dict[str, List[str]] = {}
    search_flags: Dict[str, bool] = {
        REGEX: args.regex_mode,
        IGNORE_CASE: args.ignore_case,
        INVERTED: args.invert_result
    }
    if args.files:
        for file in args.files:
            with open(file, 'r') as input_stream:
                res[file] = search_needle_in_src(
                    args.needle[0],
                    preproccesing(input_stream.readlines()),
                    search_flags
                )

    else:
        res['stdin'] = search_needle_in_src(
            args.needle[0],
            preproccesing(sys.stdin.readlines()),
            search_flags
        )
    print_search_result(res, args.count_mode)


if __name__ == '__main__':
    main(sys.argv[1:])
