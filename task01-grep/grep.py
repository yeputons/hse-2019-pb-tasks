#!/usr/bin/python
# -*- coding: UTF-8 -*-

from typing import List
import sys
import re
import argparse
import os.path


def chose_type_of_search(regex: bool, full: bool, line: str, needle: str):
    if regex:
        return re.search(needle, line)
    if full:
        return re.fullmatch(needle, line)
    else:
        return needle in line


def print_answer(ifcount: bool, answer: List, count: str):
    answer = answer.rstrip('\n')
    count = count.rstrip('\n')
    if ifcount:
        print(count)
    else:
        print(answer)


def run_all(regex: bool, full: bool, ifcount: bool, inv: bool, amount_of_files: int, needle: str, name_of_file: str):
    count = 0
    countstr = ''
    answer = ''
    answerinv = ''
    countinv = 0
    countinvstr = ''
    if amount_of_files == 0:
        source = sys.stdin
    else:
        source = open(name_of_file, 'r')
    for line in source.readlines():
        line = line.rstrip('\n')
        if chose_type_of_search(regex, full, line, needle):
            count += 1
            if source == 'sys.stdin' or amount_of_files == 1 or amount_of_files == 0:
                answer += line + '\n'
            else:
                answer += name_of_file + ':' + line + '\n'
                countstr = name_of_file + ':'
    countstr += str(count)
    print_answer(ifcount, answer, countstr)



def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-x', dest='full', action='store_true')
    parser.add_argument('-v', dest='inv', action='store_true')
    namespace = parser.parse_args(args_str)
    for file in namespace.files:
        if not os.path.isfile(file):
            print(f'File {file} does not exist')
            namespace.files.remove(file)
    if not len(namespace.files):
        run_all(namespace.regex,namespace.full, namespace.count,namespace.inv , 0, namespace.needle, '')
    else:
        for file in namespace.files:
            run_all(namespace.regex, namespace.full, namespace.count,namespace.inv , len(namespace.files), namespace.needle, file)



if __name__ == '__main__':
    main(sys.argv[1:])
#    print(namespace)
