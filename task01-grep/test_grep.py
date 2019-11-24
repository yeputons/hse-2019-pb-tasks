#!/usr/bin/env python3
import io
from typing import Any, Dict
import grep

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


def test_unit_parse_args():
    args = ['-E', '-c', "neeeee''eedle", 'file1', 'stdin']
    parser = grep.parser_init()
    parsed_args = parser.parse_args(args)
    corr_args = tog({'needle': "neeeee''eedle",
                     'regexE': True,
                     'do_count': True,
                     'files': ['file1', 'stdin']}, late=False)
    assert vars(parsed_args) == corr_args


def test_unit_format_builder_line():
    options = tog({'files': ['file1', 'file2', 'file_#1', 'not a file'], 'filename': 'file_#1',
                   'count': 0, 'do_count': False, 'regexE': True, 'needle': 'lalka'})
    assert grep.format_builder(options) == 'file_#1:{line}'


def test_unit_format_builder_count():
    options = tog({'files': ['file1', 'file2', 'file_#1', 'not a file'], 'filename': 'file_#1',
                   'count': 0, 'do_count': True, 'regexE': True, 'needle': 'lalka'})
    assert grep.format_builder(options) == 'file_#1:{count}'


def test_unit_finder_inline_regexe():
    options = tog({'files': ['file1', 'file2', 'file_#1', 'not a file'],
                   'filename': 'file_#1', 'count': 0,
                   'do_count': True, 'regexE': True, 'line': 'hohoho, merry christmas @_@',
                   'needle': '(ho){1,3}'})
    assert grep.finder_inline(options)
    options['line'] = 'hahahahpo'
    assert not grep.finder_inline(options)
    options['line'] = ''
    assert not grep.finder_inline(options)
    options['line'] = 'hohohohohohoho'
    assert grep.finder_inline(options)
    options['line'] = '(ho){1,3}}}}}}'
    assert grep.finder_inline(options)
    options['needle'] = '[a-z].'
    options['line'] = 'vvvvvv'
    assert grep.finder_inline(options)
    options['line'] = '1337228322'
    assert not grep.finder_inline(options)


def test_unit_finder_inline_no_regexe():
    options = tog({'files': ['file1', 'file2', 'file_#1', 'not a file'],
                   'filename': 'file_#1', 'count': 0,
                   'do_count': True, 'regexE': False, 'line': 'hohoho, merry christmas @_@',
                   'needle': '(ho){1,3}'})
    assert not grep.finder_inline(options)
    options['line'] = 'hahahahpo'
    options_old = options
    assert not grep.finder_inline(options)
    assert options == options_old

    options['line'] = ''
    assert not grep.finder_inline(options)
    options['line'] = 'hohohohohohoho'
    assert not grep.finder_inline(options)
    options['line'] = '(ho){1,3}}}}}}'
    assert grep.finder_inline(options)
    options['needle'] = '[a-z].'
    options['line'] = 'vvvvvv'
    assert not grep.finder_inline(options)
    options['line'] = '1337228322'
    assert not grep.finder_inline(options)


def test_unit_handler(capsys):
    options = tog({'files': ['file1', 'file2', 'file_#1', 'not a file'],
                   'filename': 'file_#1', 'count': 0, 'do_count': True,
                   'regexE': False, 'line': 'hohoho, merry christmas @_@',
                   'needle': '(ho){1,3}', 'format_out': 'file_#1:{count}'})
    grep.handler(options, final=False)
    assert options['count'] == 1

    options['do_count'] = False
    options['late_output'] = False
    options['regexE'] = True
    options['format_out'] = 'file_#1:{line}'
    grep.handler(options, final=False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'file_#1:hohoho, merry christmas @_@\n'


def test_unit_handler_final(capsys):
    options = tog({'files': ['file1', 'file2', 'file_#1', 'not a file'],
                   'filename': 'file_#1', 'count': 0, 'do_count': True,
                   'regexE': True, 'line': 'hohoho, merry christmas @_@', 'needle':
                   '(ho){1,3}', 'format_out': 'file_#1:{count}'})
    grep.handler(options, final=False)
    grep.handler(options, final=True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'file_#1:1\n'


def test_unit_searcher(tmp_path, monkeypatch, capsys):
    options = tog({'files': ['mafile'], 'filename': 'mafile', 'count': 0, 'do_count': False,
                   'regexE': True, 'needle': '(ho){1,3}', 'format_out': 'file_#1:{count}'})
    (tmp_path / 'mafile').write_text('hohoho!\nohohoh(\nlololol\n\n\n123\ni1oioioioho\n\n')
    monkeypatch.chdir(tmp_path)
    with open((tmp_path / 'mafile'), 'r') as my_io:
        options['io'] = my_io
        grep.searcher(options)
        out, err = capsys.readouterr()
        assert err == ''
        assert out == 'hohoho!\nohohoh(\ni1oioioioho\n'

    with open((tmp_path / 'mafile'), 'r') as my_io:
        options['io'] = my_io
        options['do_count'] = True
        options['late_output'] = True
        grep.searcher(options)
        out, err = capsys.readouterr()
        assert err == ''
        assert out == '3\n'


def test_unit_search_in_files_file_io(tmp_path, monkeypatch, capsys):
    options = tog({'files': ['mafile1', 'mafile2', 'mafile3'], 'do_count': False,
                   'regexE': True, 'needle': '(ho){1,3}', 'format_out': 'file_#1:{count}'})
    (tmp_path / 'mafile1').write_text('hohoho!\nohohoh(\nlololol\n\n\n123\ni1oioioioho\n\n')
    (tmp_path / 'mafile2').write_text('hahaah\nmahaoh\nhoahan\n123\n')
    (tmp_path / 'mafile3').write_text(
        'hohoh\n\n\n123\ni1lolipophoioho\n\n')
    monkeypatch.chdir(tmp_path)

    grep.search_in_files(options)
    out, err = capsys.readouterr()
    assert err == ''
    ans = """mafile1:hohoho!
mafile1:ohohoh(
mafile1:i1oioioioho
mafile2:hoahan
mafile3:hohoh
mafile3:i1lolipophoioho
"""
    assert out == ans


def test_unit_search_in_files_standard_io(monkeypatch, capsys):
    options = tog({'files': [], 'do_count': False,
                   'regexE': True, 'needle': 'needle?'})

    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.search_in_files(options)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_unit_main(tmp_path, monkeypatch, capsys):
    (tmp_path / 'mafile1').write_text('nyanyanyanyanyanyaneedlenyanyanya\nnyaneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '-c', 'needle', 'mafile1'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'

# integrate


def test_integrate_stdin_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_integrate_stdin_regex_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_integrate_stdin_grep_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_integrate_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'
