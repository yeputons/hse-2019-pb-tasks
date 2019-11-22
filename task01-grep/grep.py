#!/usr/bin/python
# -*- coding: UTF-8 -*-

from typing import List
import sys
import re
import argparse


def file_regex_search(namespace, line, i):
    if re.search(namespace.needle, line):
        if len(namespace.files) == 1:
            print(f'{line}')
        else:
            print(f'{namespace.files[i]}:{line}')


def file_search(namespace, line, i):
    if namespace.needle in line:
        if len(namespace.files) == 1:
            print(f'{line}')
        else:
            print(f'{namespace.files[i]}:{line}')


def print_file_count(namespace, count, i):
    if len(namespace.files) == 1:
        print(f'{count}')
    else:
        print(f'{namespace.files[i]}:{count}')


def stdio_regex_search(namespace, line):
    if re.search(namespace.needle, line):
        print(f'{line}')


def stdio_search(namespace, line):
    if namespace.needle in line:
        print(f'{line}')


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    namespace = parser.parse_args(args_str)
    if namespace.files:
        for i in range(len(namespace.files)):
            try:
                in_file = open(namespace.files[i], 'r')
            except IOError:
                print(f'Could not open {namespace.files[i]}!')
                del namespace.files[i]
                continue
            with in_file:
                count = 0
                for line in in_file.readlines():
                    line = line.rstrip('\n')
                    if namespace.regex and not namespace.count:
                        file_regex_search(namespace, line, i)
                    if namespace.regex and namespace.count:
                        if re.search(namespace.needle, line):
                            count += 1
                    if not namespace.regex and not namespace.count:
                        file_search(namespace, line, i)
                    if not namespace.regex and namespace.count:
                        if re.search(namespace.needle, line):
                            count += 1
                if namespace.count:
                    print_file_count(namespace, count, i)
    else:
        count = 0
        for line in sys.stdin.readlines():
            line = line.rstrip('\n')
            if namespace.regex and not namespace.count:
                stdio_regex_search(namespace, line)
            if not namespace.regex and not namespace.count:
                stdio_search(namespace, line)
            if not namespace.regex and namespace.count:
                if namespace.needle in line:
                    count += 1
            if namespace.regex and namespace.count:
                if re.search(namespace.needle, line):
                    count += 1
        if namespace.count:
            print(f'{count}')


if __name__ == '__main__':
    main(sys.argv[1:])
#    print(namespace)
