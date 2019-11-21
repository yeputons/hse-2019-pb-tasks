#!/usr/bin/env python3
"""
This script simulates GREP and can work with two flags: -E, -c.
You can get more information if you run it with the flag '--help'
"""
from typing import List, Optional
import sys
import re
import argparse
import os


def exclude_nonexistent_files(file_names: List[str]) -> List:
    """
    Gets a list of file names and exclude such files that don't exist
    :param file_names: names of files
    :return: list of the existing files
    """
    new_file_names = []
    for file_name in file_names:
        if os.path.isfile(file_name):
            new_file_names.append(file_name)
        else:
            print('No such file: ' + file_name, file=sys.stderr)
    return new_file_names


def read_all_lines(file_names: List[str]) -> List[List[str]]:
    """
    Gets a list of file names and return a list of all lines from them (in lists)
    :param file_names: names of files
    :return: a list of all lines
    """
    all_lines = []
    for file_name in file_names:
        with open(file_name, 'r') as input_file:
            all_lines.append(input_file.readlines())
    return all_lines


def strip_lines(lines: List[str]) -> List[str]:
    """
    Strips \n symbol
    :param lines: the lines to be stripped
    :return: list of new lines
    """
    return [line.rstrip('\n') for line in lines]


def filter_matched_lines(lines: List[str], pattern: str, regex_mode: bool) -> List[str]:
    """
    Searches for lines that match pattern
    :param lines: lines to be checked
    :param pattern: pattern to be matched
    :param regex_mode: indicates whether it's a regex expression
    """
    matched_lines = []
    searcher = re.compile(pattern)
    for line in lines:
        matched = searcher.search(line) if regex_mode else pattern in line
        if matched:
            matched_lines.append(line)
    return matched_lines


def print_matched_lines(lines: List[str], stream_name: Optional[str],
                        counting_mode_on: bool, output_format: str) -> None:
    """
    Prints all the matched lines with the format
    :param lines: lines to be printed
    :param stream_name: name of the stream we've read from
    :param counting_mode_on: indicates whether entries should be counted
    :param output_format: format to be used in printing
    """
    opt_name = stream_name + ':' if stream_name else ''
    if counting_mode_on:
        outputs = [output_format.format(name=opt_name, counting=len(lines), text='')]
    else:
        outputs = [output_format.format(name=opt_name, counting='', text=line) for line in lines]
    for output in outputs:
        print(output)


def parse_arguments(args_str: List[str]) -> argparse.Namespace:
    """
    Gets arguments from the command line and parses them
    :param args_str: arguments from the command line
    :return: parsed arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='counting', action='store_true')
    return parser.parse_args(args_str)


def main(args_str: List[str]):
    """
    :param args_str: arguments of the command line
    """
    args = parse_arguments(args_str)
    if args.files:
        stream_names = exclude_nonexistent_files(args.files)
        all_lines = read_all_lines(stream_names)
    else:
        all_lines = [sys.stdin.readlines()]
    if len(args.files) <= 1:
        stream_names = [None]

    for lines, stream_name in zip(all_lines, stream_names):
        lines = strip_lines(lines)
        matched_lines = filter_matched_lines(lines, args.pattern, args.regex)
        print_matched_lines(matched_lines, stream_name, args.counting, '{name}{counting}{text}')


if __name__ == '__main__':
    main(sys.argv[1:])
