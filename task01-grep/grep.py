#!/usr/bin/env python3
import re
import sys
from argparse import ArgumentParser, Namespace
from functools import partial
from typing import List, Tuple, Iterable, Callable, Pattern
MatchFunc = Callable[[str], bool]
SearchResult = Tuple[str, List[str]]
SearchFunc = Callable[[MatchFunc], List[SearchResult]]
PrintFunc = Callable[[str, SearchResult], None]
FileFilter = Callable[[SearchResult], bool]


def print_files(fmt: str,
                found: SearchResult) -> None:
    name, lines = found
    print(fmt.format(fmt, name=name, line=len(lines)))


def print_lines(fmt: str, found: SearchResult) -> None:
    name, lines = found
    for line in lines:
        print(fmt.format(name=name, line=line.rstrip('\n')))


def match_regex(needle: Pattern, strict: bool, line: str) -> bool:
    line = line.rstrip('\n')
    return bool(re.fullmatch(needle, line) if strict else re.search(needle, line))


def match_fulltext(needle: str, ignore_case: bool, strict: bool, line: str) -> bool:
    if ignore_case:
        needle, line = needle.lower(), line.lower()
    line = line.rstrip('\n')
    if strict:
        return needle == line
    else:
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


def get_regex_match_func(args: Namespace) -> MatchFunc:
    pattern = re.compile(args.needle, re.IGNORECASE if args.ignore_case else 0)
    # noinspection PyTypeChecker
    return partial(match_regex, pattern, args.strict)


def get_fulltext_match_func(args: Namespace) -> MatchFunc:
    # noinspection PyTypeChecker
    return partial(match_fulltext, args.needle, args.ignore_case, args.strict)


def inverse_match(func: MatchFunc, x: str) -> bool:
    return not func(x)


def get_match_func(args: Namespace) -> MatchFunc:
    # Пайчарм не понимает partial
    # noinspection PyTypeChecker
    func = (get_regex_match_func if args.regex else get_fulltext_match_func)(args)
    if args.invert:
        # noinspection PyTypeChecker
        func = partial(inverse_match, func)
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


def all_files(found: SearchResult) -> bool:  # pylint: disable=unused-argument
    return True


def non_empty(found: SearchResult) -> bool:
    return len(found[1]) > 0


def empty_only(found: SearchResult) -> bool:
    return len(found[1]) == 0


def get_file_filter(args: Namespace) -> FileFilter:
    if args.list_found:
        return non_empty
    if args.list_empty:
        return empty_only
    return all_files


def get_format(args: Namespace) -> str:
    if args.list_found or args.list_empty:
        return '{name}'
    if len(args.files) > 1:
        return '{name}:{line}'
    else:
        return '{line}'


def get_print_func(args: Namespace) -> PrintFunc:
    if args.count or args.list_found or args.list_empty:
        return print_files
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
