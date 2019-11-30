#!/usr/bin/env python3
import re
import sys
from argparse import ArgumentParser, Namespace
from functools import partial
from typing import List, Tuple, Iterable, Callable, Pattern, IO
MatchFunc = Callable[[str], bool]
SearchResult = Tuple[str, List[str]]
SearchFunc = Callable[[MatchFunc], List[SearchResult]]
PrintFunc = Callable[[str, SearchResult], None]
FileFilter = Callable[[SearchResult], bool]


def print_matched_count(fmt: str,
                        found: SearchResult) -> None:
    name, lines = found
    print(fmt.format(fmt, name=name, line=len(lines)))


def print_lines(fmt: str, found: SearchResult) -> None:
    name, lines = found
    for line in lines:
        print(fmt.format(name=name, line=line.rstrip('\n')))


def match(needle: Pattern, strict: bool, line: str) -> bool:
    if strict:
        re_match = re.fullmatch(needle, line)
    else:
        re_match = re.search(needle, line)
    return bool(re_match)


def search(name: str, inp: Iterable[str], matcher: MatchFunc) -> SearchResult:
    return name, [line for line in inp if matcher(line.rstrip('\n'))]


def search_stdin(matcher: MatchFunc) -> List[SearchResult]:
    return [search('', sys.stdin, matcher)]


def search_files(files: List[str], matcher: MatchFunc) -> List[SearchResult]:
    def mask_file(file_stream: IO) -> Iterable[str]:
        for line in file_stream:
            yield line
    search_results = []
    for file in files:
        with open(file) as f:
            search_results.append(search(file, mask_file(f), matcher))
    return search_results


def invert_match(func: MatchFunc, x: str) -> bool:
    return not func(x)


def get_match_func(args: Namespace) -> MatchFunc:
    needle = args.needle
    if not args.regex:
        needle = re.escape(needle)
    pattern = re.compile(needle, re.IGNORECASE if args.ignore_case else 0)
    func = partial(match, pattern, args.strict)
    if args.invert:
        func = partial(invert_match, func)
    # noinspection PyTypeChecker
    return func


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


def get_file_filter(args: Namespace) -> FileFilter:
    if args.list_found:
        return lambda found: len(found[1]) > 0
    if args.list_empty:
        return lambda found: len(found[1]) == 0
    return lambda found: True


def get_format(args: Namespace) -> str:
    if args.list_found or args.list_empty:
        return '{name}'
    if len(args.files) > 1:
        return '{name}:{line}'
    else:
        return '{line}'


def get_print_func(args: Namespace) -> PrintFunc:
    if args.count or args.list_found or args.list_empty:
        return print_matched_count
    else:
        return print_lines


def main(args_str: List[str]) -> None:
    parser = ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-i', dest='ignore_case', action='store_true')
    parser.add_argument('-v', dest='invert', action='store_true')
    parser.add_argument('-x', dest='strict', action='store_true')
    parser.add_argument('-l', dest='list_found', action='store_true')
    parser.add_argument('-L', dest='list_empty', action='store_true')
    args: Namespace = parser.parse_args(args_str)

    match_func: MatchFunc = get_match_func(args)
    search_func: SearchFunc = get_search_func(args)
    file_filter: FileFilter = get_file_filter(args)
    fmt: str = get_format(args)
    print_func: PrintFunc = get_print_func(args)

    search_results: List[SearchResult] = search_func(match_func)
    for line in search_results:
        if file_filter(line):
            print_func(fmt, line)


if __name__ == '__main__':
    main(sys.argv[1:])
