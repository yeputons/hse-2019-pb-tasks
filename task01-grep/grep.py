#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def print_result(result):  # выводит результат
    for line in result:
        print(line)


def format_lines(result, name_file):  # форматирует строки в вид имя файла : результат
    return f'{name_file}:{result}'


def find_all_lines(args_needle, lines, args_regex):
    # возвращает все строки, в которых присутсвует строка или регулярное выражение
    if args_regex:
        return [line for line in lines if re.search(args_needle, line)]
    else:
        return [line for line in lines if args_needle in line]


def calculate_result(name_file, args_needle, args_regex, args_count, count_files, lines):
    # совмещает функции: поиск подстрок и форматирования строк в нужный формат
    result = find_all_lines(args_needle, lines, args_regex)
    if args_count:
        result = [str(len(result))]
    if count_files > 1:
        result = [format_lines(line, name_file) for line in result]
    return result


def parse_args(args_str):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*', type=str)
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    return parser.parse_args(args_str)


def print_grep(args_needle, args_regex, args_count, in_file, size, file):
    # вызывает функцию print и calculate
    lines = [line.rstrip('\n') for line in in_file]
    print_result(calculate_result(file, args_needle, args_regex, args_count, size, lines))


def main(args_str: List[str]):
    args = parse_args(args_str)
    if not args.files:
        print_grep(args.needle, args.regex, args.count, sys.stdin.readlines(), len(args.files), '')
    else:
        for file in args.files:
            with open(file, 'r') as in_file:
                print_grep(args.needle, args.regex, args.count,
                           in_file.readlines(), len(args.files), file)


if __name__ == '__main__':
    main(sys.argv[1:])
