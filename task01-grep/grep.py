#!/usr/bin/env python3
""" analog GREP to work with some flags """
from typing import List
import sys
import re
import argparse


def init_arguments(args_str: List[str]) -> argparse.Namespace:
    """initializaton of input arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-i', dest='ignore', action='store_true')
    parser.add_argument('-v', dest='invert', action='store_true')
    parser.add_argument('-x', dest='match', action='store_true')
    parser.add_argument('-l', dest='file_with_str', action='store_true')
    parser.add_argument('-L', dest='file_without_str', action='store_true')

    args = parser.parse_args(args_str)
    return args


def translate_str_to_re(pattern: str, is_regular: bool) -> str:
    """translate str to regular expression and return it"""
    return re.escape(pattern) if not is_regular else pattern


def filter_list(pattern: str, list_: List[str]) -> List[str]:
    """find pattern in words of list and return list comprehension of them"""
    return [word for word in list_ if re.search(pattern, word)]


def strip(lines: List[str]) -> List[str]:
    """delete '\n' in list and return it"""
    return [line.rstrip('\n') for line in lines]


def process_flag_c(result: List[str]) -> List[str]:
    """process flag '-c' and return changed list"""
    return [str(len(result))]


def work_with_files(files: List[str], pattern: str, flags: dict) -> None:
    """branch to work with files"""
    for file in files:
        with open(file, 'r') as input_file:
            word_list = input_file.readlines()
            result = full_processing_result(word_list, pattern, flags)
            print_grep_results(result, file + ':' if len(files) > 1 else '')


def work_with_stdin(pattern: str, flags: dict) -> None:
    """branch to work with stdin"""
    word_list = sys.stdin.readlines()
    result = full_processing_result(word_list, pattern, flags)
    # это не дублирование,а вызов основной функции
    print_grep_results(result, '')
    # так проще для 2 итерации


def full_processing_result(word_list: List[str], pattern: str, flags: dict) -> List[str]:
    """full processing one file or stdin with returned result"""
    result = strip(word_list)
    result = filter_list(pattern, result)
    if flags['c']:
        result = process_flag_c(result)
    return result


def print_grep_results(result: List[str], output_format: str) -> None:
    """print results in necessary format"""
    for word in result:
        print(f'{output_format}{word}')


def main(args_str: List[str]):
    """main function"""
    args = init_arguments(args_str)

    pattern = translate_str_to_re(args.pattern, args.regex)

    flags = {'c': args.count, 'i': args.ignore, 'v': args.invert,
             'x': args.match, 'l': args.file_with_str, 'L': args.file_without_str}

    if args.files:
        work_with_files(args.files, pattern, flags)
    else:
        work_with_stdin(pattern, flags)


if __name__ == '__main__':
    main(sys.argv[1:])
