#!/usr/bin/python

from typing import List
from typing import TextIO
import sys
import re
import argparse
import os.path


def what_to_return(lines: List[str], name_of_file: str, onefile: bool, onlyfiles: bool,
                   reverseof: bool, count: bool):
    if onlyfiles or reverseof:
        if (onlyfiles and len(lines) > 0) or (reverseof and len(lines) == 0):
            print(name_of_file)
    else:
        if count:
            print_count(len(lines), name_of_file, onefile)
        else:
            print_result(lines, name_of_file, onefile)


def choosing_type_of_search(regex: bool, full: bool, caseignore: bool,
                            needle: str, line: str) -> bool:
    if caseignore and not regex:
        line = line.lower()
        needle = needle.lower()
    if regex:
        if full:
            return bool(re.fullmatch(needle, line,
                                     re.IGNORECASE if caseignore else not re.IGNORECASE))
        return bool(re.search(needle, line,
                              re.IGNORECASE if caseignore else not re.IGNORECASE))
    elif full:
        return bool(needle == line)
    else:
        return bool(needle in line)


def print_result(lines: List[str], name_of_file: str, onefile: bool):
    for line in lines:
        if onefile:
            print(line)
        else:
            print(name_of_file + ':' + line)


def print_count(count: int, name_of_file: str, onefile: bool):
    if onefile:
        print(str(count))
    else:
        print(name_of_file + ':' + str(count))


def run_all(source: TextIO, regex: bool, count: bool, full: bool,
            inversion: bool, caseignore: bool, onlyfiles: bool,
            reverseof: bool, onefile: bool, needle: str, name_of_file: str):
    correct_lines = []
    inversion_lines = []
    for line in source.readlines():
        line = line.rstrip('\n')
        if choosing_type_of_search(regex, full, caseignore, needle, line):
            correct_lines.append(line)
        else:
            inversion_lines.append(line)
    if inversion:
        what_to_return(inversion_lines, name_of_file, onefile, onlyfiles, reverseof, count)
    else:
        what_to_return(correct_lines, name_of_file, onefile, onlyfiles, reverseof, count)


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-x', dest='full', action='store_true')
    parser.add_argument('-v', dest='inversion', action='store_true')
    parser.add_argument('-i', dest='caseignore', action='store_true')
    parser.add_argument('-l', dest='onlyfiles', action='store_true')
    parser.add_argument('-L', dest='reverseof', action='store_true')
    namespace = parser.parse_args(args_str)
    for file in namespace.files:
        if not os.path.isfile(file):
            print(f'File {file} does not exist')
            namespace.files.remove(file)
    onefile = False
    if len(namespace.files) <= 1:
        onefile = True
    if len(namespace.files) == 0:
        run_all(sys.stdin, namespace.regex, namespace.count, namespace.full,
                namespace.inversion, namespace.caseignore,
                namespace.onlyfiles, namespace.reverseof, onefile,
                namespace.needle, 'sys.stdin')
    else:
        for file in namespace.files:
            with open(file, 'r') as in_file:
                run_all(in_file, namespace.regex, namespace.count, namespace.full,
                        namespace.inversion, namespace.caseignore,
                        namespace.onlyfiles, namespace.reverseof, onefile,
                        namespace.needle, file)


if __name__ == '__main__':
    main(sys.argv[1:])
