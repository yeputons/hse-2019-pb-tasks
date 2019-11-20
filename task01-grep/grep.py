#!/usr/bin/env python3
import re
import sys
from argparse import ArgumentParser, Namespace
from functools import partial
from typing import List, Tuple, Iterable, Callable

MatchFunc = Callable[[str], bool]
SearchResult = Tuple[str, List[str]]
SearchFunc = Callable[[MatchFunc], List[SearchResult]]
PrintFunc = Callable[[str, SearchResult], None]


def print_count(fmt: str, found: SearchResult) -> None:
    name, lines = found
    print(fmt.format(fmt, name=name, line=len(lines)))


def print_lines(fmt: str, found: SearchResult) -> None:
    name, lines = found
    for line in lines:
        print(fmt.format(name=name, line=line.rstrip('\n')))


def match_regex(needle: str, line: str) -> bool:
    return re.search(needle, line) is not None


def match_fulltext(needle: str, line: str) -> bool:
    return needle in line


def search(name: str, inp: Iterable[str], matcher: MatchFunc) -> SearchResult:
    return name, list(filter(matcher, inp))


def search_stdin(matcher: MatchFunc) -> List[SearchResult]:
    return [search('', sys.stdin, matcher)]


def search_files(files: List[str], matcher: MatchFunc) -> List[SearchResult]:
    search_results = []
    for file in files:
        with open(file) as f:
            search_results.append(search(file, f, matcher))
    return search_results


def get_match_func(args: Namespace) -> MatchFunc:
    # Пайчарм не понимает partial
    # noinspection PyTypeChecker
    return partial(match_regex if args.regex else match_fulltext, args.needle)


def get_search_func(args: Namespace) -> SearchFunc:
    func: SearchFunc
    if args.files:
        # Если написать это односточным ифом, то пайчарму хорошо
        # (или, скорее, он не српавляется, и не даёт ворнига), а mypy плохо
        # Если написать так, то mypy хорошо, а пайчарму плохо...
        # noinspection PyTypeChecker
        func = partial(search_files, args.files)
    else:
        func = search_stdin
    return func


def get_format(args: Namespace) -> str:
    if len(args.files) > 1:
        return '{name}:{line}'
    else:
        return '{line}'


def get_print_func(args: Namespace) -> PrintFunc:
    return print_count if args.count else print_lines


def main(args_str: List[str]) -> None:
    parser = ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    args: Namespace = parser.parse_args(args_str)

    match_func: MatchFunc = get_match_func(args)
    search_func: SearchFunc = get_search_func(args)
    fmt: str = get_format(args)
    print_func: PrintFunc = get_print_func(args)

    search_results: List[SearchResult] = search_func(match_func)
    for line in search_results:
        print_func(fmt, line)


if __name__ == '__main__':
    main(sys.argv[1:])
