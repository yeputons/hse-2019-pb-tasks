#!/usr/bin/env python3
from typing import List
from typing import Tuple
from typing import Dict
import sys
import re
import argparse


def find(line: str, needle: str, flags: Dict[str, bool]) -> bool:
    if flags['regex']:
        if flags['igncase']:
            if flags['fullmatch']:
                result = re.fullmatch(needle, line, flags=re.IGNORECASE)
            else:
                result = re.search(needle, line, flags=re.IGNORECASE)
        else:
            if flags['fullmatch']:
                result = re.fullmatch(needle, line)
            else:
                result = re.search(needle, line)
        return bool(result)
    else:
        if flags['igncase']:
            needle = needle.lower()
            line = line.lower()
        return needle == line if flags['fullmatch'] else needle in line


def get_lines_with_needle(lines: List[str], needle: str, flags: Dict[str, bool]) -> List[str]:
    lines_with_needle = []
    for line in lines:
        is_find = find(line, needle, flags)
        if not is_find and flags['rev'] or is_find and not flags['rev']:
            lines_with_needle.append(line)
    return lines_with_needle


def print_lines(files_and_lines: List[Tuple[str, List[str]]], form_s: str, flags: Dict[str, bool]):
    for file, lines in files_and_lines:

        if flags['bad_file_names']:
            if not lines:
                print(file)
            continue

        if flags['good_file_names']:
            if lines:
                print(file)
            continue

        if flags['count']:
            print(form_s.format(file, len(lines)))
        else:
            for line in lines:
                print(form_s.format(file, line))


def read_from_stdin() -> List[str]:
    lines = []
    for line in sys.stdin.readlines():
        lines.append(line.rstrip('\n'))
    return lines


def read_from_file(file_name: str) -> List[str]:
    lines = []
    with open(file_name, 'r') as in_file:
        for line in in_file.readlines():
            lines.append(line.rstrip('\n'))
    return lines


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-i', dest='igncase', action='store_true')
    parser.add_argument('-v', dest='rev', action='store_true')
    parser.add_argument('-x', dest='fullmatch', action='store_true')
    parser.add_argument('-l', dest='good_file_names', action='store_true')
    parser.add_argument('-L', dest='bad_file_names', action='store_true')
    args = parser.parse_args(args_str)

    flags = {
        'count': args.count,
        'regex': args.regex,
        'igncase': args.igncase,
        'rev': args.rev,
        'fullmatch': args.fullmatch,
        'good_file_names': args.good_file_names,
        'bad_file_names': args.bad_file_names
    }

    format_str = '{}:{}' if len(args.files) > 1 else '{1}'
    files_and_lines_with_needle = []
    if args.files:
        for file_name in args.files:
            lines = read_from_file(file_name)
            lines_with_needle = get_lines_with_needle(lines, args.needle, flags)
            files_and_lines_with_needle.append((file_name, lines_with_needle))
    else:
        lines = read_from_stdin()
        lines_with_needle = get_lines_with_needle(lines, args.needle, flags)
        files_and_lines_with_needle.append(('', lines_with_needle))

    print_lines(files_and_lines_with_needle, format_str, flags)


if __name__ == '__main__':
    main(sys.argv[1:])
