#!/usr/bin/env python3

from typing import List
from typing import Dict

import sys
import re
import argparse


def match(needle: str, line: str, regex: bool) -> bool:
    if regex:
        return re.search(needle, line) is not None
    return needle in line


def preproccesing(data: List[str]) -> List[str]:
    return [line.rstrip('\n') for line in data]


def search_needle_in_src(needle: str, source: List[str],
                         regex: bool = False) -> List[str]:

    appearances = []
    for line in source:
        if match(needle, line, regex):
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
    parser.add_argument('needle',
                        type=str,
                        nargs=1,
                        help='a string(or a regex) to search for')
    parser.add_argument('files',
                        nargs='*',
                        help='a sources where to search (default: stdin)')
    args = parser.parse_args(arg_str)
    res: Dict[str, List[str]] = {}
    if args.files:
        for file in args.files:
            with open(file, 'r') as input_stream:
                res[file] = search_needle_in_src(
                    args.needle[0],
                    preproccesing(input_stream.readlines()),
                    args.regex_mode
                )

    else:
        res['stdin'] = search_needle_in_src(
            args.needle[0],
            preproccesing(sys.stdin.readlines()),
            args.regex_mode
        )
    print_search_result(res, args.count_mode)


if __name__ == '__main__':
    main(sys.argv[1:])
