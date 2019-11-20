#!/usr/bin/env python3
from typing import List, Tuple
from argparse import Namespace
import io
import re
from functools import partial
import grep


# UNIT #


# Следующие два в своей работе print_name используют. Что с этим лучше всего делать? Замокать?
def test_unit_print_files(capsys):
    grep.print_files('{line}', ('NOT_PRINTED', ['a', 'b', 'c', 'd']))
    grep.print_files('{name}:{line}', ('PRINTED', []))
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\nPRINTED:0\n'


def test_unit_print_lines(capsys):
    grep.print_lines('{line}', ('NOT_PRINTED', ['a', 'b', 'c', 'd']))
    grep.print_lines('{name}:{line}', ('PRINTED', ['1', '2']))
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a\nb\nc\nd\nPRINTED:1\nPRINTED:2\n'


def test_unit_regexp_mach():
    tests: List[Tuple[str, str, bool]] = [
        ('cyhm', 'cyhm', True),
        ('cyhm', 'cyh', False),
        ('cyhm?', 'cyhm', True),
        ('cyhm?', 'cyhm?', True),
        ('cyhm?', 'cyh', True),
        ('cyhm+', 'cyhmmmmmm', True),
        ('cyh', 'cyhm', True)
    ]
    for pattern, data, answer in tests:
        assert grep.match_regex(re.compile(pattern), False, data) == answer


def test_unit_fulltext():
    tests: List[Tuple[str, str, bool]] = [
        ('cyhm', 'cyhm', True),
        ('cyhm', 'cyh', False),
        ('cyhm?', 'cyhm', False),
        ('cyhm?', 'cyhm?', True),
        ('cyhm?', 'cyh', False),
        ('cyhm+', 'cyhmmmmmm', False),
        ('cyh', 'cyhm', True)
    ]
    for pattern, data, answer in tests:
        assert grep.match_fulltext(pattern, False, False, data) == answer


def test_unit_search():
    test_str = 'Can you hear me?\nAbsolutely\n'

    assert grep.search('test', io.StringIO(test_str), lambda x: 'me' in x) \
        == ('test', ['Can you hear me?\n'])
    assert grep.search('test', io.StringIO(test_str), lambda x: re.search('m?e', x) is not None) \
        == ('test', ['Can you hear me?\n', 'Absolutely\n'])


def test_unit_search_stdin(monkeypatch):
    test_str = 'Can you hear me?\nAbsolutely\n'
    monkeypatch.setattr('sys.stdin', io.StringIO(test_str))

    assert grep.search_stdin(lambda x: 'me' in x) \
        == [('', ['Can you hear me?\n'])]

    monkeypatch.setattr('sys.stdin', io.StringIO(test_str))

    assert grep.search_stdin(lambda x: re.search('m?e', x) is not None) \
        == [('', ['Can you hear me?\n', 'Absolutely\n'])]


def test_unit_search_files(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('Can you hear me?\nAbsolutely\n')
    monkeypatch.chdir(tmp_path)

    assert grep.search_files(['a.txt'], lambda x: 'me' in x) \
        == [('a.txt', ['Can you hear me?\n'])]
    assert grep.search_files(['a.txt'], lambda x: re.search('m?e', x) is not None) \
        == [('a.txt', ['Can you hear me?\n', 'Absolutely\n'])]


def test_get_match_func():
    needle = 'm?e'
    args_fulltext = Namespace(regex=False, needle=needle, ignore_case=False, invert=False,
                              strict=False)
    # Whitebox testing: Оно всегда будет partial.

    matcher_fulltext: partial = grep.get_match_func(args_fulltext)  # type: ignore
    # pylint: disable=no-member
    assert matcher_fulltext.func is grep.match_fulltext
    # pylint: disable=no-member
    assert matcher_fulltext.args == (needle, False, False)
    # pylint: disable=no-member
    assert matcher_fulltext.keywords == {}

    args_regex = Namespace(regex=True, needle='m?e', ignore_case=False, invert=False,
                           strict=False)
    matcher_regex: partial = grep.get_match_func(args_regex)  # type: ignore
    # pylint: disable=no-member
    assert matcher_regex.func is grep.match_regex
    # pylint: disable=no-member
    assert matcher_regex.args[0].pattern == needle
    assert matcher_regex.args[1] is False
    # pylint: disable=no-member
    assert matcher_regex.keywords == {}


def test_get_search_func():
    args_stdin = Namespace(files=[])
    search_stdin = grep.get_search_func(args_stdin)
    # pylint: disable=comparison-with-callable
    assert search_stdin == grep.search_stdin

    args_files = Namespace(files=['a', 'b'])
    search_files: partial = grep.get_search_func(args_files)  # type: ignore
    # pylint: disable=comparison-with-callable
    assert search_files.func == grep.search_files
    # pylint: disable=no-member
    assert search_files.args == (['a', 'b'],)
    # pylint: disable=no-member
    assert search_files.keywords == {}


def test_get_format():
    assert grep.get_format(Namespace(files=[], list_found=False, list_empty=False)) == '{line}'
    assert grep.get_format(Namespace(files=['a'], list_found=False, list_empty=False)) == '{line}'
    assert grep.get_format(Namespace(files=['a', 'b'],
                                     list_found=False, list_empty=False)) == '{name}:{line}'


# INTEGRATION #


def test_integrate_multifile_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:pref needle suf\na.txt:pref needle suf\n'


# GIVEN #


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
