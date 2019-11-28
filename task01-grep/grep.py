#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def print_result(result):  # выводит результат
    for line in result:
        if line is not None:
            print(line)


def format_lines(result, name_file, args_presence, args_absent):
    # форматирует строки в вид имя файла : результат, если есть ключи -l и -L в вид: имя файла
    if args_presence:
        if int(result) > 0:
            return f'{name_file}'
    elif args_absent:
        if not int(result):
            return f'{name_file}'
    else:
        return f'{name_file}:{result}'


def find_all_lines(args_needle, lines, args_regex, args_ignore, args_full, args_reverse):
    """ если нет ключа -E, применит re.escape и будет работать с ней также,
    как и с регулярным выражением,
    если есть ключ -x, будет искать с помощью re.fullmatch,
    если нет, то с помощью re.search,
    если есть ключ -i, будет искать с аргументом re.IGNORECASE,
    если есть ключ -v, будет найденные строки делать не найденными и наооборот """
    if not args_regex:
        args_needle = re.escape(args_needle)
    if args_full:
        if args_reverse:
            return [line for line in lines
                    if not re.fullmatch(args_needle, line, re.IGNORECASE * args_ignore)]
        else:
            return [line for line in lines
                    if re.fullmatch(args_needle, line, re.IGNORECASE * args_ignore)]
    else:
        if args_reverse:
            return [line for line in lines
                    if not re.search(args_needle, line, re.IGNORECASE * args_ignore)]
        else:
            return [line for line in lines
                    if re.search(args_needle, line, re.IGNORECASE * args_ignore)]


def calculate_result(name_file, args_needle, args_regex, args_count, args_ignore, args_full,
                     args_reverse, args_presence, args_absent, count_files, lines):
    # вызывает функцию find_all_lines, чтобы найти все подстроки,
    # затем, если есть ключи -c, -l, -L, считает сколько подстрок,
    # потом, если ввод с нескольких файлов форматирует строки в нужный формат
    result = find_all_lines(args_needle, lines, args_regex, args_ignore, args_full, args_reverse)
    if args_count or args_presence or args_absent:
        result = [str(len(result))]
    if count_files > 1:
        result = [format_lines(line, name_file, args_presence, args_absent) for line in result]
    return result


def parse_args(args_str):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*', type=str)
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-i', dest='ignore', action='store_true')
    parser.add_argument('-v', dest='reverse', action='store_true')
    parser.add_argument('-x', dest='full', action='store_true')
    parser.add_argument('-l', dest='presence', action='store_true')
    parser.add_argument('-L', dest='absent', action='store_true')
    return parser.parse_args(args_str)


def print_grep(args_needle, args_regex, args_count, args_ignore, args_full,
               args_reverse, args_presence, args_absent, in_file, size, file):
    # вызывает функцию calculate_result, чтобы отфильтровать нужные строчки
    # и затем вызывает функцию print_result, чтобы вывести их
    lines = [line.rstrip('\n') for line in in_file]
    print_result(calculate_result(file, args_needle, args_regex, args_count, args_ignore,
                                  args_full, args_reverse, args_presence, args_absent, size, lines))


def main(args_str: List[str]):
    args = parse_args(args_str)
    if not args.files:
        print_grep(args.needle, args.regex, args.count, args.ignore, args.full, args.reverse,
                   args.presence, args.absent, sys.stdin.readlines(), len(args.files), '')
    else:
        for file in args.files:
            with open(file, 'r') as in_file:
                print_grep(args.needle, args.regex, args.count, args.ignore,
                           args.full, args.reverse, args.presence, args.absent,
                           in_file.readlines(), len(args.files), file)


if __name__ == '__main__':
    main(sys.argv[1:])
