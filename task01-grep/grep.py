#!/usr/bin/env python3
from typing import List, TextIO, Callable
import sys
import re
import argparse


def normal_search(needle: str, line: str, exact: bool = False) -> bool:
    if exact:
        return needle == line
    else:
        return needle in line


def regex_search(needle: str, line: str, exact: bool = False) -> bool:
    if exact:
        return bool(re.fullmatch(needle, line))
    else:
        return bool(re.search(needle, line))


def single_grep(needle: str,
                strings: List[str],
                search_function: Callable[[str, str, bool], bool],
                ignore_case: bool = False,
                exact: bool = False) -> List[str]:
    def modifier(s: str):
        if ignore_case:
            return s.lower()
        return s

    return list(
        filter(
            lambda line: search_function(modifier(needle), modifier(line),
                                         exact), strings))


def read_input(args: argparse.Namespace) -> List[List[str]]:
    def read_from_textio(file: TextIO) -> List[str]:
        return list(map(lambda line: line.rstrip('\n'), file.readlines()))

    if not args.files:
        return [read_from_textio(sys.stdin)]
    else:
        res = []
        for file in args.files:
            with open(file) as f:
                res.append(read_from_textio(f))
        return res


def print_answers(answers: List[List[str]], args: argparse.Namespace):
    if args.line_exists or args.line_not_exists:
        assert len(args.files) > 0
        for filename, answer in zip(args.files, answers):
            if (args.line_exists
                    and len(answer) > 0) or (args.line_not_exists
                                             and len(answer) == 0):
                print(filename)
    else:
        if len(answers) == 1:
            print(*answers[0], sep='\n')
        else:
            for filename, answer in zip(args.files, answers):
                for x in answer:
                    print(filename, x, sep=':')


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-i', dest='ignore_case', action='store_true')
    parser.add_argument('-v', dest='invert', action='store_true')
    parser.add_argument('-x', dest='exact', action='store_true')
    parser.add_argument('-l', dest='line_exists', action='store_true')
    parser.add_argument('-L', dest='line_not_exists', action='store_true')
    return parser


def main(args_str: List[str]):
    parser = create_parser()
    args = parser.parse_args(args_str)

    search_function_no_invert: Callable[
        [str, str, bool], bool] = regex_search if args.regex else normal_search
    search_function_invert: Callable[
        [str, str, bool], bool] = lambda *args: not search_function_no_invert(
            *args)

    search_function = search_function_invert if args.invert else search_function_no_invert

    inputs = read_input(args)

    answers = [
        single_grep(args.needle, input, search_function, args.ignore_case,
                    args.exact) for input in inputs
    ]

    if args.count:
        answers = [[str(len(x))] for x in answers]

    print_answers(answers, args)


if __name__ == '__main__':
    main(sys.argv[1:])
