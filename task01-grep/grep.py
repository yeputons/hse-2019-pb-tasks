#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def init_parser() -> argparse.ArgumentParser:   # Инициализируем парсер,
    parser = argparse.ArgumentParser(              # теперь им можно пользоваться ^^
        'You can use this program for searching strings in files... If you really want it.\n'
        'To use you just need to write what you want to search, and where (file).\n'
        "If you don't input any file we will search in stdin).\n"
        '(Please make sure that you and your enter with EOF symbol)')
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*', default=[sys.stdin], type=argparse.FileType('r'))
    parser.add_argument('-E', dest='regex', action='store_true',
                        help='use needle as regular expression')
    parser.add_argument('-c', dest='cflag', action='store_true',
                        help="count number of needle's enters")
    return parser


def add_found_needle(line: str, needle: str, reg: bool, file, num: int, listres: list):   # Если
    if (needle in line and not reg) or (reg and re.search(needle, line)):  # needle -подстрока line
        listres.append(f"{file.name + ':' if num > 1 else ''}{line}")  # добавляем её в список


def update_cnt_needle(line: str, needle: str, reg: bool, cnt: int) -> int:   # Обновляем счётчик
    if (needle in line and not reg) or (reg and re.search(needle, line)):     # если needle
        cnt += 1                                                             # это подстрочка line
    return cnt


def add_cnt(cnt: int, file, num: int, listres: list):  # Добавляем в список результат счёта строчек
    listres.append(f"{file.name + ':' if num > 1 else ''}{cnt}")


def print_res(listres: list):  # Выводим результат на экран
    for line in listres:  # (переданный список в правильном формате)
        print(line)


def process_data(args):  # Эта функция - своеобразный заместитель главной. Тут вся логика программы
    listres = []
    for file in args.files:
        cnt = 0
        for line in file.readlines():
            line = line.rstrip('\n')
            if args.cflag:
                cnt = update_cnt_needle(line, args.needle, args.regex, cnt)
            else:
                add_found_needle(line, args.needle, args.regex, file, len(args.files), listres)
        if args.cflag:
            add_cnt(cnt, file, len(args.files), listres)
        file.close()
    print_res(listres)


def main(args_str: List[str]):   # Самая главная функция ^^, координирует всю работу
    parser = init_parser()
    args = parser.parse_args(args_str)
    process_data(args)


if __name__ == '__main__':
    main(sys.argv[1:])