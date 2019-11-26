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


def detect_requested_lines(pattern: str, inp_lines: List[List[str]], need_regex: bool) -> List[List[str]]:
    def detection_func(s: str) -> bool:
        if need_regex:
            return bool(re.search(pattern, s))
        else:
            return pattern in s

    return [detect_lines_by_function(detection_func, lines_in_one) for lines_in_one in inp_lines]


def detect_lines_by_function(detection_func: Callable[[str], bool], lines: List[str]) -> List[str]:
    out = []
    for line in lines:
        if detection_func(line):
            out.append(line)
    return out


def prepare_output(detected_lines: List[List[str]], need_count: bool) -> List[List[str]]:
    if need_count:
        return [[str(len(detected_lines_in_one))]
                for detected_lines_in_one in detected_lines]
    else:
        return detected_lines


def output(file_names: List[str], out_lines: List[List[str]]):
    if len(out_lines) == 1:
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
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    args = parser.parse_args(args_str)
    inp_lines = read_input(args.files)
    detected_lines = detect_requested_lines(args.pattern, inp_lines, args.regex)
    out_lines = prepare_output(detected_lines, args.count)
    output(args.files, out_lines)


if __name__ == '__main__':
    main(sys.argv[1:])
