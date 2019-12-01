#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse
from typing import TextIO


def parse(args_str: List[str]) -> argparse.Namespace:
    """разбор входных аргументов"""
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-c', dest='cnt', action='store_true')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-i', dest='ignore', action='store_true')
    parser.add_argument('-v', dest='inverse', action='store_true')
    parser.add_argument('-x', dest='fullmatch', action='store_true')
    parser.add_argument('-l', dest='ans', action='store_true')
    parser.add_argument('-L', dest='not_ans', action='store_true')
    args = parser.parse_args(args_str)
    if args.not_ans:
        args.ans = not args.ans
        args.inverse = not args.inverse
    if args.ignore and not args.regex:
        args.needle = args.needle.lower()
    return args


def print_lines(lines: List[str],
                args: argparse.Namespace, name_of_file: str = None) -> None:
    """Выводит список найденных в правильном формате,
        заданном ключами. Ключи, задающие формат вывода:
        1) -v: inverse - найденные строки считаются ненайденными,
        и наоборот
        2) -с: count - выводит количество найденных строк, если файл один или
        строки были считаны из стандартного потока ввода.
        Если файлов было несколько, то выводит сначала имя файла,
        а затем количество найденных строк в этом файле
        3) -l и -L: строчки не ввыодятся. Выводятся имена файлов,
        где есть хотя бы одна найденная строчка(-l), или где найденные строчки,
        наоборот, отсутствуют(-L). Используются только для файлов"""
    if args.ans:
        if len(lines) > 0:
            print(name_of_file)
    else:
        if args.cnt:
            print(len(lines) if len(args.files) <= 1 else f'{name_of_file}:{len(lines)}')
        else:
            for line in lines:
                print(line if len(args.files) <= 1 else f'{name_of_file}:{line}')


def find_lines(args: argparse.Namespace, input: TextIO, name_of_file: str = None) -> None:
    """Ищет все подстроки в заданном формате(строка или регулярное выражение),
        которые находятся в данном файле или стандартном потоке ввода и
        выводит их в правильном формате.
        Формат смотреть в описании функции print lines"""
    lines_find = []
    lines_unfind = []
    for line in input.readlines():
        line = line.rstrip('\n')
        if args.regex:
            if find_regex(args, line):
                lines_find.append(line)
            else:
                lines_unfind.append(line)
        else:
            if find_str(args, line):
                lines_find.append(line)
            else:
                lines_unfind.append(line)
    if args.inverse:
        print_lines(lines_unfind, args, name_of_file)
    else:
        print_lines(lines_find, args, name_of_file)


def find_regex(args: argparse.Namespace,
               line: str) -> bool:
    """Возвращает True, если нашёл подстроку, удовлетворяющую
        регулярному выражению в указанном формате
        в строке и False иначе. Ключи, опрежедяющие формат поиска:
        1) -x: fullmatch - находит строчки, полностью подходящие
        регулярному выражению
        2) -i: ignore - игнорирует регистр символов при поиске совпадений"""
    flags = 0
    reg = re.search
    if args.ignore:
        flags = re.IGNORECASE
    if args.fullmatch:
        reg = re.fullmatch
    if reg(args.needle, line, flags):
        return True
    return False


def find_str(args: argparse.Namespace, line: str) -> bool:
    """Возвращает True, если нашел подстроку в заданном формате,
        False иначе. Ключи, определяющие формат поиска:
        1) -x: fullmatch - находит только полные совпадения строк;
        2) -i:ignore - игнорирует регистр символов при поиске совпадений"""
    if args.ignore:
        line = line.lower()
    if args.fullmatch:
        return args.needle == line
    else:
        return args.needle in line


def main(args_str: List[str]):
    args = parse(args_str)
    if args.files:
        for name in args.files:
            with open(name, 'r') as in_file:
                find_lines(args, in_file, name)
    else:
        find_lines(args, sys.stdin)


if __name__ == '__main__':
    main(sys.argv[1:])
