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


def find_in_reg(line: str,
                needle: str,
                fullmatch: bool) -> bool:
    if fullmatch:
        return re.fullmatch(needle, line) is not None
    else:
        return re.search(needle, line) is not None


def find_in_not_reg(line: str,
                    needle: str,
                    fullmatch: bool) -> bool:
    if fullmatch:
        return line == needle
    else:
        return needle in line


def find_in(line: str,
            needle: str,
            reg: bool,
            ignore: bool,
            invert: bool,
            fullmatch) -> bool:
    linetemp = line
    needletemp = needle
    if ignore:
        linetemp = line.lower()
        needletemp = needle.lower()
    if reg:
        result = find_in_reg(linetemp, needletemp, fullmatch)
    else:
        result = find_in_not_reg(linetemp, needletemp, fullmatch)
    if invert:
        return not result
    return result


def add_format_line(line: str,
                    file,
                    num: int,
                    listres: List[str]):
    """ Добавляем в переданный список строчку, по пути форматируя её """
    listres.append(f"{file.name + ':' if num > 1 else ''}{line}")


def collect_res(dictlistres: dict,
                dictfiles: dict,
                cflag: bool,
                writefile: bool,
                writeinvertfile: bool):
    """ Собираем результат (список строчек в правильном формате) """
    listres = []
    for file in dictfiles:
        if cflag:
            add_format_line(str(len(dictlistres[file])),
                            file,
                            len(dictfiles),
                            listres)
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


def print_res(listres: List[str]):
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
                add_format_line(line,
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
