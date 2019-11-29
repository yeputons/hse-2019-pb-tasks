#!/usr/bin/env python3
from typing import List
import sys
import re
import argparse


def init_parser() -> argparse.ArgumentParser:
    """
        Инициализируем парсер
        теперь им можно пользоваться ^^
    """
    parser = argparse.ArgumentParser(
        'You can use this program for searching strings in files... If you really want it.\n'
        'To use you just need to write what you want to search, and where (file).\n'
        "If you don't input any file we will search in stdin).\n"
        '(Please make sure that you and your enter with EOF symbol)')
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*', default=[sys.stdin], type=argparse.FileType('r'))
    parser.add_argument('-E', dest='regex', action='store_true',
                        help='use needle as regular expression')
    parser.add_argument('-i', dest='ignore', action='store_true',
                        help='ignore register')
    parser.add_argument('-v', dest='invert', action='store_true',
                        help='invert result')
    parser.add_argument('-x', dest='fullmatch', action='store_true',
                        help='full match for strings')
    parser.add_argument('-c', dest='cflag', action='store_true',
                        help="count number of needle's enters")
    parser.add_argument('-l', dest='writefile', action='store_true',
                        help="print name file, where needle enters")
    parser.add_argument('-L', dest='writeinvertfile', action='store_true',
                        help="print name file, where needle doesn't enter")
    return parser


def find_in_reg(line,
                needle,
                fullmatch) -> bool:
    if fullmatch:
        return re.fullmatch(needle, line) is not None
    else:
        return re.search(needle, line) is not None


def find_in_not_reg(line,
                    needle,
                    fullmatch) -> bool:
    if fullmatch:
        return line == needle
    else:
        return needle in line


def find_in(line,
            needle,
            reg,
            ignore,
            invert,
            fullmatch) -> bool:
    if ignore:
        line = line.lower()
        needle = needle.lower()
    if reg:
        result = find_in_reg(line, needle, fullmatch)
    else:
        result = find_in_not_reg(line, needle, fullmatch)
    if invert:
        result = result is False
    return result


def add_found_needle(line: str,
                     file,
                     num: int,
                     listres: list):
    """ Добавляем в переданный список сторчку, по пути форматируя её """
    listres.append(f"{file.name + ':' if num > 1 else ''}{line}")


def collect_res(dictlistres,
                dictfiles,
                cflag: bool,
                writefile: bool,
                writeinvertfile: bool):
    """ Собираем результат (список строчек в правильном формате) """
    listres = []
    for file in dictfiles:
        if cflag:
            listres.append(f"{file.name + ':' if len(dictfiles) > 1 else ''}{len(dictlistres[file])}")
            continue
        if writefile:
            if dictfiles[file] == 'found':
                listres.append(file.name)
            continue
        if writeinvertfile:
            if dictfiles[file] == 'empty':
                listres.append(file.name)
            continue
        for line in dictlistres[file]:
            listres.append(line)
    return listres


def print_res(listres):
    for line in listres:
        print(line)


def process_data(args):
    """ Функция, в которой прописана вся логика программы """
    dictlistres = {}
    dictfiles = {}
    for file in args.files:
        linesinfile = []
        dictfiles[file] = 'empty'
        for line in file.readlines():
            line = line.rstrip('\n')
            if find_in(line,
                       args.needle,
                       args.regex,
                       args.ignore,
                       args.invert,
                       args.fullmatch):
                add_found_needle(line,
                                 file,
                                 len(args.files),
                                 linesinfile)
                dictfiles[file] = 'found'
        dictlistres[file] = linesinfile
        file.close()
    print_res(collect_res(dictlistres,
                          dictfiles,
                          args.cflag,
                          args.writefile,
                          args.writeinvertfile))


def main(args_str: List[str]):
    """
        Самая главная функция ^^, она координирут всю работу
    """
    parser = init_parser()
    args = parser.parse_args(args_str)
    process_data(args)


if __name__ == '__main__':
    main(sys.argv[1:])
