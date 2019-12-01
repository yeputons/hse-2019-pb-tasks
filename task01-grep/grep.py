#!/usr/bin/env python3
from typing import List, Dict
import sys
import re
import argparse

fl_dict_type = Dict[str, List[str]]


def does_line_match(line: str, regex: bool, needle: str) -> bool:
    if regex:
        return bool(re.search(needle, line))
    else:
        return needle in line


def search_needle_in_file_line_dict(file_line_dict: fl_dict_type,
                                    needle: str, regex: bool) -> fl_dict_type:
    matching_elements: fl_dict_type = {}
    for file in file_line_dict:
        matching_elements[file] = []
        for line in file_line_dict[file]:
            if does_line_match(line, regex, needle):
                matching_elements[file].append(line)
    return matching_elements


def lines_to_numbers(file_line_dict: fl_dict_type) -> fl_dict_type:
    for file in file_line_dict:
        file_line_dict[file] = [str(len(file_line_dict[file]))]
    return file_line_dict


# My escaped characters:
# &&f - filename
# &&l - line
def print_format(output_line: str, filename: str, line: str) -> None:
    print(output_line.format(line=line, filename=filename))


def print_output_dict(output: fl_dict_type, output_format: str) -> None:
    is_any_output = False
    for file in output:
        for line in output[file]:
            print_format(output_format, file, line)
            is_any_output = True
    if not is_any_output:
        print()


def read_files(files: List['str']) -> fl_dict_type:
    file_line_dict: fl_dict_type = {}
    for file in files:
        file_line_dict[file] = []
        with open(file, 'r') as input_file:
            for line in input_file.readlines():
                file_line_dict[file].append(line.rstrip('\n'))
    return file_line_dict


def read_stdin() -> fl_dict_type:
    file_line_dict: fl_dict_type = {'': []}
    for line in sys.stdin.readlines():
        file_line_dict[''].append(line.rstrip('\n'))
    return file_line_dict


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='output_count', action='store_true')
    args = parser.parse_args(args_str)

    file_line_dict = read_files(args.files) if args.files else read_stdin()

    matching_elements = search_needle_in_file_line_dict(file_line_dict, args.needle, args.regex)
    if args.output_count:
        lines_to_numbers(matching_elements)

    output_line = '{line}'
    if len(args.files) > 1:
        output_line = '{filename}:{line}'

    print_output_dict(matching_elements, output_line)


if __name__ == '__main__':
    main(sys.argv[1:])
