#!/usr/bin/env python3
from typing import List, TextIO, Callable
import sys
import re
import argparse


def regex_search(needle: str, line: str, exact: bool = False, ignore_case: bool = False) -> bool:
    expr = re.compile(needle, re.IGNORECASE if ignore_case else 0)
    if exact:
        return bool(expr.fullmatch(line))
    else:
        return bool(expr.search(line))


def single_grep(needle: str,
                strings: List[str],
                search_function: Callable[[str, str, bool], bool],
                regex: bool = False,
                ignore_case: bool = False,
                exact: bool = False) -> List[str]:
    if not regex:
        needle = re.escape(needle)

    return list(
        filter(
            lambda line: search_function(needle, line,
                                         exact, ignore_case), strings))


def read_input(files: List[str]) -> List[List[str]]:
    def read_from_textio(file: TextIO) -> List[str]:
        return list(map(lambda line: line.rstrip('\n'), file.readlines()))

    if not files:
        return [read_from_textio(sys.stdin)]
    else:
        res = []
        for file in files:
            with open(file) as f:
                res.append(read_from_textio(f))
        return res


def print_answers(answers: List[List[str]], args: argparse.Namespace):
    if args.line_exists or args.line_not_exists:
        assert len(args.files) > 0
        assert not (args.line_exists and args.line_not_exists)
        for filename, answer in zip(args.files, answers):
            if args.line_exists ^ (len(answer) > 0) == 0:
                print(filename)
    else:
        if len(answers) == 1:
            if len(answers[0]) > 0:
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

    regex_search_invert: Callable[
        [str, str, bool], bool] = lambda *args: not regex_search(*args)

    search_function = regex_search_invert if args.invert else regex_search

    inputs = read_input(args.files)

    answers = [
        single_grep(args.needle, input, search_function, args.regex, args.ignore_case,
                    args.exact) for input in inputs
    ]

    if args.count:
        answers = [[str(len(x))] for x in answers]

    print_answers(answers, args)


if __name__ == '__main__':
    main(sys.argv[1:])
