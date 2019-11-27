#!/usr/bin/env python3
from typing import List
from typing import Callable
from typing import TextIO
import sys
import re
import argparse


def search_as_regex(needle: str, line: str) -> bool:
    return bool(re.search(needle, line))


def search_as_string(needle: str, line: str) -> bool:
    return needle in line


def parse(file: TextIO, needle: str, search_function: Callable, output: List[str]):
    for line in file:
        line = line.rstrip('\n')
        if search_function(needle, line):
            output.append(line)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str, help='string that you want to search')
    parser.add_argument('files', nargs='*', default=[sys.stdin], type=argparse.FileType('r'),
                        help='files in which you want to search')
    parser.add_argument('-E', dest='regex', action='store_true',
                        help='search as regular expression')
    parser.add_argument('-c', dest='count', action='store_true',
                        help='print the number of entries')

    args = parser.parse_args(args_str)

    search_function = search_as_string
    if args.regex:
        search_function = search_as_regex

    output: List[str] = list()

    if len(args.files) == 1:
        output = list()
        parse(args.files[0], args.needle, search_function, output)
        if args.count:
            print(len(output))
        else:
            for i in output:
                print(i)
    else:
        for file in args.files:
            output = list()
            parse(file, args.needle, search_function, output)
            if args.count:
                print(f'{file.name}: {len(output)}')
            else:
                for line in output:
                    print(f'{file.name}: {line}')

    for file in args.files:
        file.close()


if __name__ == '__main__':
    main(sys.argv[1:])
