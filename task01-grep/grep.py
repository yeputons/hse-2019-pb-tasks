#!/usr/bin/env python3
from typing import List, TextIO, Callable
import sys
import re
import argparse


def read_input(file_names: List[str]) -> List[List[str]]:
    if not file_names:
        return [split_into_lines(sys.stdin)]
    else:
        return [split_into_lines_file(file_name)
                for file_name in file_names]


def split_into_lines_file(file_name: str) -> List[str]:
    with open(file_name, 'r') as in_file:
        return split_into_lines(in_file)


def split_into_lines(input_stream: TextIO) -> List[str]:
    return [line.rstrip('\n') for line in input_stream.readlines()]


def get_detection_func(pattern: str, need_regex: bool = False,
                       ignore_register: bool = False, invert_detection: bool = False,
                       need_full_match: bool = False) -> Callable[[str], bool]:
    regex_pattern = pattern if need_regex else re.escape(pattern)
    if ignore_register:
        compiled_regex_pattern = re.compile(regex_pattern, re.IGNORECASE)
    else:
        compiled_regex_pattern = re.compile(regex_pattern)
    regex_detect_function = re.fullmatch if need_full_match else re.search

    def detection_func(s: str) -> bool:
        return bool(regex_detect_function(compiled_regex_pattern, s)) ^ invert_detection

    return detection_func


def detect_requested_lines(detection_func: Callable[[str], bool],
                           inp_lines: List[List[str]]) -> List[List[str]]:
    return [detect_lines_by_function(detection_func, lines_in_one) for lines_in_one in inp_lines]


def detect_lines_by_function(detection_func: Callable[[str], bool], lines: List[str]) -> List[str]:
    out = []
    for line in lines:
        if detection_func(line):
            out.append(line)
    return out


def prepare_output(detected_lines: List[List[str]], need_count: bool = False) -> List[List[str]]:
    if need_count:
        return [[str(len(detected_lines_in_one))]
                for detected_lines_in_one in detected_lines]
    else:
        return detected_lines


def output(file_names: List[str], out_lines: List[List[str]],
           need_detected_file_names: bool = False,
           need_undetected_file_names: bool = False):
    if need_detected_file_names or need_undetected_file_names:
        for out_lines_file in zip(out_lines, file_names):
            if bool(out_lines_file[0]) ^ need_undetected_file_names:
                print(out_lines_file[1])
    elif len(out_lines) == 1:
        for out_line in out_lines[0]:
            print(out_line)
    else:
        for out_lines_file in zip(out_lines, file_names):
            for detected_line in out_lines_file[0]:
                print(f'{out_lines_file[1]}:{detected_line}')


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    output_method = parser.add_mutually_exclusive_group(required=False)
    output_method.add_argument('-c', dest='count', action='store_true')
    output_method.add_argument('-l', dest='detected_file_names', action='store_true')
    output_method.add_argument('-L', dest='undetected_file_names', action='store_true')
    parser.add_argument('-i', dest='ignore_register', action='store_true')
    parser.add_argument('-v', dest='invert', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    args = parser.parse_args(args_str)
    inp_lines = read_input(args.files)
    detection_func = get_detection_func(args.pattern, args.regex, args.ignore_register,
                                        args.invert, args.full_match)
    detected_lines = detect_requested_lines(detection_func, inp_lines)
    out_lines = prepare_output(detected_lines, args.count)
    output(args.files, out_lines, args.detected_file_names, args.undetected_file_names)


if __name__ == '__main__':
    main(sys.argv[1:])
