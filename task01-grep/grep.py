#!/usr/bin/env python3
from typing import List, Dict, Any
import sys
import re
import argparse


def dict_filter(options: Dict[str, Any], allowed: List[str],
                exclude: bool = False) -> Dict[str, Any]:

    # take dict and list and include/exclude only elements of dict mentioned in list
    new_options = {}
    for opt in options:
        if (opt in allowed) ^ exclude:
            new_options[opt] = options[opt]
            # xor here and further
    return new_options


def parser_init() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Search needle in each file.',
                                     epilog='When file option is not specified, '
                                            'read standard input\n'
                                            '                            Meow.')

    output_format_group = parser.add_mutually_exclusive_group()

    output_format_group.add_argument('-c',
                                     dest='do_count',
                                     action='store_true',
                                     help='print only the count of needle matches')

    output_format_group.add_argument('-l',
                                     dest='do_only_files',
                                     action='store_true',
                                     help='print only names of files where the needle was found')

    output_format_group.add_argument('-L',
                                     dest='do_only_not_files',
                                     action='store_true',
                                     help='print only names of files '
                                          'where the needle was NOT found')

    parser.add_argument('-i',
                        dest='do_ignore_case',
                        action='store_true',
                        help='ingore case')

    parser.add_argument('-v',
                        dest='do_invert',
                        action='store_true',
                        help='select only non-matching lines')

    parser.add_argument('-x',
                        dest='do_whole_line',
                        action='store_true',
                        help='match only whole lines')

    parser.add_argument('-E',
                        dest='regexE',
                        action='store_true',
                        help='needle is a regular expression')

    parser.add_argument('needle',
                        type=str,
                        help='needle to search in files')

    parser.add_argument('files',
                        nargs='*',
                        help='list of files for searching needle')

    return parser


def format_builder(options: Dict[str, Any]) -> str:
    # here format of output can be modified (in case of adding of additional flags)
    output_format = ''
    if options['do_only_files'] or options['do_only_not_files']:
        output_format += options['filename']
    else:
        if len(options['files']) > 1:
            output_format += '{}:'.format(options['filename'])

        if options['do_count']:
            output_format += '{count}'
        else:
            output_format += '{line}'
    return output_format


def options_configure(options: Dict[str, Any]) -> None:
    # here options are configured according to arguments
    if not options['regexE']:
        options['needle'] = re.escape(options['needle'])

    options['regexE_flags'] = []
    if options['do_ignore_case']:
        options['regexE_flags'].append(re.IGNORECASE)

    options['late_output'] = options['do_count'] or \
        options['do_only_files'] or \
        options['do_only_not_files']


def finder_inline(options: Dict[str, Any]) -> bool:
    # actually looks for needle in a haystack

    if options['do_whole_line']:
        search_result = bool(re.fullmatch(
            options['needle'], options['line'], *options['regexE_flags']))
    else:
        search_result = bool(
            re.search(options['needle'], options['line'], *options['regexE_flags']))

    return search_result ^ options['do_invert']


def handler(options: Dict[str, Any], final: bool) -> None:
    # do something in case if match found (e.g. increase count, print, etc)

    if final:
        if options['late_output']:
            # search a reason (according to arguments)
            # to make final output

            if options['do_count'] or \
                    options['do_only_files'] and options['count'] > 0 or \
                    options['do_only_not_files'] and options['count'] == 0:
                print(options['format_out'].format_map(options))
    else:
        options['count'] += 1
        if not options['late_output']:
            print(options['format_out'].format_map(options))


def searcher(options: Dict[str, Any]) -> None:
    # search needle
    options['count'] = 0
    options_for_formatter = dict_filter(
        options, ['do_count', 'do_only_files', 'do_only_not_files', 'filename', 'files'])
    options['format_out'] = format_builder(options_for_formatter)
    options_for_finder = dict_filter(options, ['regexE', 'do_whole_line', 'regexE_flags',
                                               'needle', 'do_ignore_case', 'do_invert',
                                               'do_whole_line', 'line'])
    options_for_handler = dict_filter(options, ['late_output', 'do_count', 'count', 'format_out',
                                                'count', 'do_only_files', 'do_only_not_files'])

    for line in options['io']:
        line = line.rstrip('\n')
        options_for_finder['line'] = line
        options_for_handler['line'] = line
        found = finder_inline(options_for_finder)

        if found:
            handler(options_for_handler, final=False)

    handler(options_for_handler, final=True)


def search_in_files(options: Dict[str, Any]):
    # look for needle in all files given
    if len(options['files']) == 0:
        options['filename'] = '(standard input)'
        options['io'] = sys.stdin

        searcher(options)

    else:
        for filename in options['files']:
            with open(filename, 'r') as io:
                options['filename'] = filename
                options['io'] = io

                searcher(options)


def main(args: List[str]):
    parser = parser_init()
    parsed_args = parser.parse_args(args)

    options: Dict[str, Any] = vars(parsed_args)
    options_configure(options)  # configure options so not filtered

    search_in_files(options)


if __name__ == '__main__':
    main(sys.argv[1:])
