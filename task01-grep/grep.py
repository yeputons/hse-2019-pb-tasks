#!/usr/bin/env python3
import sys
import re
import argparse
from typing import List, Iterable


def print_result(result: Iterable) -> None:  # выводит результат
    for line in result:
        if line is not None:
            print(line)


def format_lines(result: str, name_file: str, args_presence: bool, args_absent: bool):
    # форматирует строки в вид имя файла : результат, если есть ключи -l и -L в вид: имя файла
    # int(result) с ключами -l и -L, так как result = [str(len(result))]
    if args_presence:
        if int(result) > 0:
            return f'{name_file}'
        else:
            return None
    elif args_absent:
        if not int(result):
            return f'{name_file}'
        else:
            return None
    else:
        return f'{name_file}:{result}'


def find_all_lines(args_needle: str, lines: List[str],
                   args_regex: bool, args_ignore: bool, args_full: bool,
                   args_reverse: bool) -> List[str]:
    """если есть ключ -x, будет искать с помощью re.fullmatch,
    если нет, то с помощью re.search,
    если есть ключ -i, будет искать с аргументом re.IGNORECASE
    если есть ключ -v, будет найденные строки делать не найденными и наооборот
    если нет ключа -E, применит re.escape и будет работать с ней также,
    как и с регулярным выражением,
    потом вызовет функцию, кооторая проверяет ключи: -x, -i, -v """
    if not args_regex:
        args_needle = re.escape(args_needle)
    if args_full:
        search = re.fullmatch
    else:
        search = re.search
    if args_reverse:
        return [line for line in lines
                if not search(args_needle, line, re.IGNORECASE * args_ignore)]
    else:
        return [line for line in lines
                if search(args_needle, line, re.IGNORECASE * args_ignore)]


def calculate_result(name_file: str, args_needle: str, args_regex: bool,
                     args_count: bool, args_ignore: bool,
                     args_full: bool, args_reverse: bool,
                     args_presence: bool,
                     args_absent: bool, count_files: int, lines: List[str]) -> List[str]:
    # вызывает функцию find_all_lines, чтобы найти все подстроки,
    # затем, если есть ключи -c, -l, -L, считает сколько подстрок,
    # потом, если ввод с нескольких файлов форматирует строки в нужный формат
    result = find_all_lines(args_needle, lines, args_regex, args_ignore, args_full, args_reverse)
    if args_count or args_presence or args_absent:
        result = [str(len(result))]
    if count_files > 1:
        result = [format_lines(line, name_file, args_presence, args_absent) for line in result]
    return result


def parse_args(args_str: List[str]) -> argparse.Namespace:
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


def print_grep(args_needle: str, args_regex: bool,
               args_count: bool, args_ignore: bool, args_full: bool,
               args_reverse: bool, args_presence: bool, args_absent: bool, read_lines: List[str],
               size: int, file: str) -> None:
    # вызывает функцию calculate_result, чтобы отфильтровать нужные строчки
    # и затем вызывает функцию print_result, чтобы вывести их
    lines = [line.rstrip('\n') for line in read_lines]
    print_result(calculate_result(file, args_needle, args_regex, args_count, args_ignore,
                                  args_full, args_reverse, args_presence, args_absent, size, lines))


def main(args_str: List[str]) -> None:
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
