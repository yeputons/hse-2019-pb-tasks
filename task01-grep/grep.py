#!/usr/bin/env python3
from typing import List
from typing import Iterable
from typing import Pattern
import sys
import re
import argparse


def get_pattern(pattern: str, regex: bool, ignore: bool = False) -> Pattern:
    if not regex:
        pattern = re.escape(pattern)
    if ignore:
        return re.compile(pattern, flags=re.IGNORECASE)
    return re.compile(pattern)


def search_file(pattern: Pattern[str], line: str,
                full_match: bool = False, rev: bool = False) -> bool:
    if full_match:
        return rev ^ bool(re.fullmatch(pattern, line))
    return rev ^ bool(re.search(pattern, line))


def file_to_lines(lines: Iterable) -> List[str]:
    return [line.rstrip('\n') for line in lines]


def search_global(pattern: Pattern[str], data: List[str],
                  full_match: bool = False, rev: bool = False) -> List[str]:
    return [line for line in data if search_file(pattern, line, full_match, rev)]


def formating(data: List[str], count: bool, names: bool = False,
              rev_names: bool = False, source: str = None) -> List[str]:
    if names or rev_names:
        assert source
        return [source] if rev_names ^ bool(data) else []
    if count:
        data = [str(len(data))]
    if source:
        return ['{}:{}'.format(source, line) for line in data]
    else:
        return data


def search_source(source: Iterable, pattern: Pattern[str],
                  count: bool, full_match: bool = False,
                  rev: bool = False, names: bool = False,
                  rev_names: bool = False, source_name: str = None) -> List[str]:
    res: List[str] = search_global(pattern, file_to_lines(source), full_match, rev)
    return formating(res, count, names, rev_names, source_name)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-l', dest='names', action='store_true')
    parser.add_argument('-L', dest='rev_names', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-i', dest='ignore', action='store_true')
    parser.add_argument('-v', dest='rev', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    args = parser.parse_args(args_str)

    res: List[str] = []
    pattern: Pattern[str] = get_pattern(args.needle, args.regex, args.ignore)
    if args.files:
        for file_cur in args.files:
            with open(file_cur, 'r') as file:

                source: str = file_cur if len(args.files) > 1 or \
                                          args.names or args.rev_names else None
                res += search_source(file, pattern, args.count, args.full_match,
                                     args.rev, args.names, args.rev_names,
                                     source)

    else:
        res = search_source(sys.stdin, pattern, args.count, args.full_match,
                            args.rev, args.names, args.rev_names)

    for line in res:
        print(line)


if __name__ == '__main__':
    main(sys.argv[1:])
