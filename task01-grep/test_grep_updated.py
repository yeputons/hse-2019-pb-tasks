#!/usr/bin/env python3
import io
import re
from typing import Any, Dict
import grep
import pytest

# trusted options generator


def tog(addition: Dict[str, Any], late: bool = True) -> Dict[str, Any]:

    options: Dict[str, Any] = {}
    options['needle'] = ''

    options['do_count'] = False
    options['do_only_files'] = False
    options['do_only_not_files'] = False

    options['do_ignore_case'] = False
    options['do_invert'] = False
    options['do_whole_line'] = False

    options['regexE'] = False

    if late:
        options['late_output'] = False
        options['regexE_flags'] = []

        options['format_out'] = ''
        options['io'] = None

        options['files'] = []
        options['filename'] = ''
        options['line'] = ''
        options['count'] = 0

    for key, val in zip(addition.keys(), addition.values()):
        options[key] = val
    if late:
        if options['do_count'] or options['do_only_files']:
            options['late_output'] = True

    return options


# unit

def test_unit_new_parser():
    args = ['-L', '-iv', '-x', "neeeee''eedle", 'file1', 'stdin']
    parser = grep.parser_init()
    parsed_args = parser.parse_args(args)
    corr_args = tog({'needle': "neeeee''eedle",
                     'do_only_not_files': True,
                     'do_ignore_case': True,
                     'do_invert': True,
                     'do_whole_line': True,
                     'files': ['file1', 'stdin']}, late=False)
    assert vars(parsed_args) == corr_args


def test_unit_format_bilder_onlyfile():
    options = tog({'files': ['file1', 'file2', 'file_#1', 'not a file'], 'filename': 'file_#1',
                   'count': 0, 'do_count': False, 'regexE': True,
                   'do_only_files': True, 'needle': 'lalka'})

    assert grep.format_builder(options) == 'file_#1'


def test_unit_options_configure_regex():
    options = tog({'files': ['file1', 'file2', 'file_#1', 'not a file'],
                   'filename': 'file_#1',
                   'count': 0, 'do_count': False, 'regexE': True,
                   'do_only_files': True, 'needle': 'lalka'})
    options['do_ignore_case'] = True
    corr_opt = options.copy()
    corr_opt['regexE_flags'] = [re.IGNORECASE]
    grep.options_configure(options)
    assert options == corr_opt


def test_unit_options_configure_simple():
    options = tog({'files': ['file1', 'file2', 'file_#1', 'not a file'], 'filename': 'file_#1',
                   'count': 0, 'do_count': False, 'regexE': False,
                   'do_only_files': True, 'needle': 'JaVaNoChKa'})
    options['do_ignore_case'] = True
    corr_opt = options.copy()
    corr_opt['regexE_flags'] = [re.IGNORECASE]
    grep.options_configure(options)
    assert options == corr_opt


def test_unit_options_configure_other():
    options = tog({'files': ['file1', 'file2', 'file_#1', 'not a file'],
                   'filename': 'file_#1', 'count': 0, 'do_count': False,
                   'regexE': False, 'do_only_not_files': True,
                   'needle': 'JaVaNoChKa'})
    options['do_invert'] = True
    corr_opt = options.copy()
    corr_opt['late_output'] = True
    grep.options_configure(options)
    assert options == corr_opt


def test_unit_finder_inline_new():
    options = tog({'files': ['file1', 'file2', 'file_#1', 'not a file'],
                   'filename': 'file_#1', 'count': 0,
                   'do_count': True, 'regexE': False, 'line': 'hohoho, merry christmas @_@',
                   'needle': '(hO){1,3}'})
    options['regexE'] = True
    options['line'] = 'hOhOhO'
    options['do_whole_line'] = False
    options['do_ignore_case'] = False

    assert grep.finder_inline(options)

    options['line'] = 'hohoho, merry christmas @_@'
    options['do_whole_line'] = True
    options['do_ignore_case'] = False

    assert not grep.finder_inline(options)

    options['do_whole_line'] = False
    options['do_ignore_case'] = True
    options['regexE_flags'] = [re.IGNORECASE]

    assert grep.finder_inline(options)

    options['do_whole_line'] = True
    options['do_ignore_case'] = True

    assert not grep.finder_inline(options)

    options['do_whole_line'] = True
    options['do_ignore_case'] = True
    options['line'] = options['line'][:6]

    assert grep.finder_inline(options)

    options['regexE'] = False
    options['regexE_flags'] = []

    options['do_whole_line'] = False
    options['do_ignore_case'] = False

    options['line'] = '(ho){1,3} ooooo'

    assert not grep.finder_inline(options)

    options['do_whole_line'] = True
    options['do_ignore_case'] = False

    assert not grep.finder_inline(options)

    options['regexE_flags'] = [re.IGNORECASE]

    options['do_whole_line'] = False
    options['do_ignore_case'] = True
    options['line'] = '(hO){1,3} ooooo'

    assert grep.finder_inline(options)

    options['do_whole_line'] = True
    options['do_ignore_case'] = True
    options['line'] = '(hO){1,3} ooooo'

    assert not grep.finder_inline(options)


def test_dict_filter_nex():
    options = tog({})
    options['regexE'] = True
    options['do_ignore_case'] = True
    options['line'] = 'my precious'
    new_dict = grep.dict_filter(
        options, ['regexE', 'line', 'do_count', 'some_trash_option'])
    corr_dict = {'regexE': True, 'line': 'my precious', 'do_count': False}
    assert new_dict == corr_dict


def test_dict_filter_ex():
    options = {}
    options['regexE'] = True
    options['do_ignore_case'] = True
    options['line'] = 'my precious'
    new_dict = grep.dict_filter(
        options, ['regexE', 'do_count', 'some_trash_option'], exclude=True)
    corr_dict = {'do_ignore_case': True, 'line': 'my precious'}
    assert new_dict == corr_dict

# integrate


def test_integrate_all_keys_print_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-livx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_integrate_all_keys_print_not_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-Livx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_integrate_all_keys_count_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-civx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:3\na.txt:0\n'


def test_integrate_new_parser_fail():
    args = ['-L', '-civ', '-x', "neeeee''eedle", 'file1', 'stdin']
    with pytest.raises(SystemExit) as parser_fail_info:
        grep.main(args)
    assert str(parser_fail_info) == "<ExceptionInfo SystemExit(2) tblen=6>"


def test_integrate_inverse(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe nEedle!\npref needle suf'))
    grep.main(['-v', 'nEedle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle\nneedle suf\npref needle suf\n'


def test_integrade_do_only_not_files_issue(tmp_path, monkeypatch, capsys):
    (tmp_path / '1.txt').write_text('pattern\npattern\npattern')
    (tmp_path / '2.txt').write_text('pattern\npattern\nnot one more :)')
    (tmp_path / '3.txt').write_text('no needles here!\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-L', 'pattern', '1.txt', '2.txt', '3.txt'])
    out, err = capsys.readouterr()
    assert err == ""
    assert out == "3.txt\n"
