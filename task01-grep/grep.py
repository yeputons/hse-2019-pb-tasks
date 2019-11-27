#!/usr/bin/env python3
import re
import sys
import argparse


def print_data(lines: list, args: argparse.Namespace) -> None:
    """
    This function gets strings for printing answer. If we have flag -c
    then function will print count of strings, otherwise
    strings will be printed.
    """
    for element in lines:
        if args.count:
            element['lines'] = [len(element['lines'])]

        if args.name_with_str:
            if element['lines']:
                element['lines'] = [element['name']]
            else:
                element['lines'] = []

        if args.name_without_str:
            if not element['lines']:
                element['lines'] = [element['name']]
            else:
                element['lines'] = []

    for element in lines:
        for line in element['lines']:
            if len(lines) > 1 and not args.name_with_str and not args.name_without_str:
                print(element['name'], end=':')
            print(line)


def take_strings(name_file: str) -> list:
    """
    This function loads strings from standard output or file.
    If name_file is empty then there is our data in standard output.
    Otherwise there is our data in the file.
    Function returns list of strings.
    """
    if name_file == '':
        set_of_lines = sys.stdin.readlines()
    else:
        with open(name_file, 'r') as file:
            set_of_lines = file.readlines()

    return set_of_lines


def search(args: argparse.Namespace) -> list:
    """
    Function uses the names of files for getting data from them.
    After that function search correct strings. If args.regex is true
    that function use library 're'. Otherwise standard operator 'in' will be used.
    """
    if not args.files:
        args.files.append('')

    find_strings = []
    for name_file in args.files:
        box_of_strings = {'name': name_file, 'lines': []}
        for line in take_strings(name_file):
            line = line.rstrip('\n')
            if args.regex:
                if re.search(args.substring, line):
                    box_of_strings['lines'].append(line)
            else:
                if args.substring in line:
                    box_of_strings['lines'].append(line)
        find_strings.append(box_of_strings)

    return find_strings


def make_parameters(argv: list) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('substring', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-l', dest='name_with_str', action='store_true')
    parser.add_argument('-L', dest='name_without_str', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    args = parser.parse_args(argv)

    return args


def main(argv: list) -> None:
    """
    Main logic of the program
    is described in this function
    """
    args = make_parameters(argv)

    lines = search(args)
    print_data(lines, args)


if __name__ == '__main__':
    main(sys.argv[1:])
