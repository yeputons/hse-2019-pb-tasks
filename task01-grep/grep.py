#!/usr/bin/env python3
from typing import List, TextIO, Callable
import sys
import re
import io
import argparse


def normal_search(needle: str, line: str) -> bool:
    return needle in line


def regex_search(needle: str, line: str) -> bool:
    return bool(re.search(needle, line))


def single_grep(needle: str, strings: List[str],
                search_function: Callable[[str, str], bool]) -> List[str]:
    return list(filter(lambda line: search_function(needle, line), strings))


def read_input(args: argparse.Namespace) -> List[List[str]]:
    def read_from_textio(file: TextIO) -> List[str]:
        return list(map(lambda line: line.rstrip('\n'), file.readlines()))

    if __debug__:
        assert read_from_textio(io.StringIO('')) == []
        assert read_from_textio(io.StringIO('hi')) == ['hi']
        assert read_from_textio(io.StringIO('hi\n')) == ['hi']
        assert read_from_textio(io.StringIO('hi\n\n')) == ['hi', '']
        assert read_from_textio(
            io.StringIO(
                'pref needle?\nneedle? suf\nthe needl\npref needle? suf')) == [
                    'pref needle?', 'needle? suf', 'the needl', 'pref needle? suf'
                ]

    if not args.files:
        return [read_from_textio(sys.stdin)]
    else:
        res = []
        for file in args.files:
            with open(file) as f:
                res.append(read_from_textio(f))
        return res


def print_answers(answers: List[List[str]], args: argparse.Namespace):
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
    return parser


def main(args_str: List[str]):
    parser = create_parser()
    args = parser.parse_args(args_str)

    search_function = regex_search if args.regex else normal_search

    inputs = read_input(args)

    answers = [
        single_grep(args.needle, input, search_function) for input in inputs
    ]

    if args.count:
        answers = [[str(len(x))] for x in answers]

    print_answers(answers, args)


if __name__ == '__main__':
    main(sys.argv[1:])
