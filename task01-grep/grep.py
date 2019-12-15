#!/usr/bin/env python3
from typing import List, Dict, Any
import sys
import re
import argparse


def filterr(opt: Dict[str, Any], allowed: List[str], exception: bool = False) -> Dict[str, Any]:
    formatted_opt = {}
    for one_opt in opt:
        if (one_opt in allowed) ^ exception:
            formatted_opt[one_opt] = opt[one_opt]
    return formatted_opt


def init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    output_format_group = parser.add_mutually_exclusive_group()
    output_format_group.add_argument('-c', dest='do_count', action='store_true',
                                     help='Выдает только количество строк, содержащих образец.')
    output_format_group.add_argument('-l',
                                     dest='do_only_files',
                                     action='store_true',
                                     help='Выдает только файлов, содержащих '
                                          'сопоставившиеся строки, по одному в строке.'
                                          ' Если образец найден в '
                                          'нескольких строках файла,'
                                          ' имя файла не повторяется.')
    output_format_group.add_argument('-L',
                                     dest='do_only_not_files',
                                     action='store_true',
                                     help='Выдает только имена '
                                          'файлов, НЕ содержащих '
                                          'сопоставившиеся '
                                          'строки, по одному в '
                                          'строке. Если образец '
                                          'НЕ найден в '
                                          'нескольких строках '
                                          'файла, имя файла не '
                                          'повторяется.')
    parser.add_argument('-E', dest='regex',
                        action='store_true',
                        help='Ищет регулярное выражение')
    parser.add_argument('-v', dest='do_invert', action='store_true',
                        help='Выдает все строки, за исключением содержащих образец.')
    parser.add_argument('-i', dest='ignore_case',
                        action='store_true',
                        help='Игнорирует регистр символов при сравнениях.')
    parser.add_argument('-x', dest='do_whole_line',
                        action='store_true',
                        help='Считает сопоставившимися только '
                             'строки, все символы которых '
                             'использованы при сопоставлении с '
                             'фиксированной строкой или регулярным '
                             'выражением.')
    parser.add_argument('needle', type=str, help='Строка которую необходимо найти')
    parser.add_argument('files', nargs='*', help='Список файлов, в которых нужно произвести поиск')

    return parser


def format_builder(opt: Dict[str, Any]) -> str:
    output_format = ''
    if opt['do_only_files'] or opt['do_only_not_files']:
        output_format += opt['name_of_files']
    else:
        if len(opt['files']) > 1:
            output_format += '{}:'.format(opt['name_of_files'])
        if opt['do_count']:
            output_format += '{count}'
        else:
            output_format += '{line}'
    return output_format


def config_opt(opt: Dict[str, Any]) -> None:
    opt['regex_flags'] = []
    if not opt['regex']:
        opt['needle'] = re.escape(opt['needle'])
    if opt['ignore_case']:
        opt['regex_flags'].append(re.IGNORECASE)
    opt['delayed_output'] = opt['do_count'] or opt['do_only_files'] or opt['do_only_not_files']


def finder_inline(opt: Dict[str, Any]) -> bool:
    if opt['do_whole_line']:
        search_result = bool(re.fullmatch(opt['needle'], opt['line'], *opt['regex_flags']))
    else:
        search_result = bool(re.search(opt['needle'], opt['line'], *opt['regex_flags']))
    return search_result ^ opt['do_invert']


def handler(opt: Dict[str, Any], final: bool) -> None:
    if final:
        if opt['delayed_output']:
            if opt['do_count'] or opt['do_only_files'] and opt['count'] > 0 or \
                    opt['do_only_not_files'] and opt['count'] == 0:
                print(opt['format_out'].format_map(opt))
    else:
        opt['count'] += 1
        if not opt['delayed_output']:
            print(opt['format_out'].format_map(opt))


def searcher(opt: Dict[str, Any]) -> None:
    opt['count'] = 0
    opt_for_formater = filterr(opt, ['do_only_files', 'do_only_not_files',
                                     'do_count', 'name_of_files', 'files'])
    opt['format_out'] = format_builder(opt_for_formater)
    opt_for_finder = filterr(opt, ['regex', 'needle', 'do_invert',
                                   'ignore_case', 'do_whole_line', 'regex_flags',
                                   'do_whole_line', 'line'])
    opt_for_handler = filterr(opt, ['delayed_output', 'do_only_files', 'do_only_not_files',
                                    'do_count', 'count', 'format_out', 'count'])
    for line in opt['io']:
        line = line.rstrip('\n')
        opt_for_finder['line'] = line
        opt_for_handler['line'] = line
        found = finder_inline(opt_for_finder)
        if found:
            handler(opt_for_handler, final=False)
    handler(opt_for_handler, final=True)


def search_in_files(opt: Dict[str, Any]):
    if len(opt['files']) == 0:
        opt['name_of_files'] = 'stdin'
        opt['io'] = sys.stdin
        searcher(opt)
    else:
        for file in opt['files']:
            with open(file, 'r') as io:
                opt['name_of_files'] = file
                opt['io'] = io
                searcher(opt)


def main(args: List[str]):
    parser = init_parser()
    parsed_args = parser.parse_args(args)
    opt: Dict[str, Any] = vars(parsed_args)
    config_opt(opt)
    search_in_files(opt)


if __name__ == '__main__':
    main(sys.argv[1:])
