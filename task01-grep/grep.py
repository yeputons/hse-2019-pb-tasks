#!/usr/bin/env python3
"""
This script simulates GREP and can work with some flags: -E, -c, -x, -i, -l, -L, -v.
You can get more information if you run it with the flag '--help'
"""
from typing import List, Optional, Any, Tuple, Pattern
import sys
import re
import argparse
import os


def split_files_by_existence(file_names: List[str]) -> Tuple[List[Any], List[Any]]:
    """
    Gets a list of file names and exclude such files that don't exist
    :param file_names: names of files
    :return: list of the existing files
    """
    existing_files = []
    nonexistent_files = []
    for file_name in file_names:
        if os.path.isfile(file_name):
            existing_files.append(file_name)
        else:
            nonexistent_files.append(file_name)
    return existing_files, nonexistent_files


def read_files(file_names: List[str]) -> List[List[str]]:
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


def filter_line(line: str, invert_mode: bool, fullmatch_mode: bool,
                searcher: Pattern[str]) -> bool:
    """
    Check if the line matches the pattern with the flags
    :param line: the given line
    :param invert_mode: -i flag
    :param fullmatch_mode: -x flag
    :param searcher: for searching
    :return:
    """
    if not fullmatch_mode:
        matched = searcher.search(line)
    else:
        matched = searcher.fullmatch(line)
    return invert_mode ^ bool(matched)


def filter_matched_lines(lines: List[str], pattern: str, regex_mode: bool,
                         invert_mode: bool, ignore_mode: bool, fullmatch_mode: bool) -> List[str]:
    """
    Searches for lines that match pattern
    :param lines: lines to be checked
    :param pattern: pattern to be matched
    :param invert_mode: -v flag
    :param ignore_mode: -i flag
    :param fullmatch_mode: -x flag
    """
    if not regex_mode:
        pattern = re.escape(pattern)
    if ignore_mode:
        searcher = re.compile(pattern, flags=re.IGNORECASE)
    else:
        searcher = re.compile(pattern)
    return [line for line in lines if filter_line(line, invert_mode, fullmatch_mode, searcher)]


def prepare_output(lines: List[str], stream_name: Optional[str], counting_mode: bool,
                   only_files_mode: bool, only_not_files_mode: bool) -> List[str]:
    """
    Process the lines before output to satisfy the flags
    :param lines: the given lines
    :param stream_name: the name of file
    :param counting_mode: -c flag
    :param only_files_mode: -l flag
    :param only_not_files_mode: -L flag
    :return: list of the output
    """
    if only_files_mode or only_not_files_mode:
        assert stream_name
        output_lines = [stream_name] if bool(lines) ^ only_not_files_mode else []
    else:
        if stream_name:
            stream_name = f'{stream_name}:'
        else:
            stream_name = ''
        if counting_mode:
            lines = [str(len(lines))]
        output_lines = [f'{stream_name}{line}' for line in lines]
    return output_lines


def print_matched_lines(output_lines: List[str]) -> None:
    """
    Prints all the given lines
    :param output_lines: lines to be printed
    """
    for line in output_lines:
        print(line)


def parse_arguments(args_str: List[str]) -> argparse.Namespace:
    """
    Gets arguments and parses them
    :param args_str: arguments
    :return: parsed arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-v', dest='invert', action='store_true')
    parser.add_argument('-i', dest='ignore', action='store_true')
    parser.add_argument('-x', dest='fullmatch', action='store_true')
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument('-c', dest='counting', action='store_true')
    format_group.add_argument('-l', dest='only_files', action='store_true')
    format_group.add_argument('-L', dest='only_not_files', action='store_true')
    return parser.parse_args(args_str)


def main(args_str: List[str]):
    """
    :param args_str: arguments of the command line
    """
    args = parse_arguments(args_str)
    if args.files:
        stream_names, nonexistent_files = split_files_by_existence(args.files)
        all_lines = read_files(stream_names)
        for file in nonexistent_files:
            print(f'No such file: {file}', file=sys.stderr)
    else:
        all_lines = [sys.stdin.readlines()]
        stream_names = [None]

    if len(args.files) == 1 and not args.only_files and not args.only_not_files:
        stream_names = [None]

    for lines, stream_name in zip(all_lines, stream_names):
        lines = strip_lines(lines)
        matched_lines = filter_matched_lines(lines, args.pattern, args.regex,
                                             args.invert, args.ignore, args.fullmatch)
        output_lines = prepare_output(matched_lines, stream_name, args.counting,
                                      args.only_files, args.only_not_files)
        print_matched_lines(output_lines)


if __name__ == '__main__':
    main(sys.argv[1:])
