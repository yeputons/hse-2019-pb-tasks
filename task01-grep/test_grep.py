#!/usr/bin/env python3
import io
import grep
import argparse


def test_unit_files_to_strings(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('abc\n1\nbab')
    (tmp_path / 'b.txt').write_text('')
    monkeypatch.chdir(tmp_path)
    res = grep.files_to_strings(['a.txt', 'b.txt'])
    _, err = capsys.readouterr()
    assert err == ''
    assert res == [['abc', '1', 'bab'], []]


def test_unit_stdin_files_to_strings(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'abc\n1\nbab'))
    res = grep.stdin_to_strings()
    _, err = capsys.readouterr()
    assert err == ''
    assert res == [['abc', '1', 'bab']]


def test_unit_match_regex():
    r_matcher = grep.select_matcher(True, False, False, False)
    assert r_matcher('abchelloasdf', 'hello')
    assert r_matcher('hello', 'hello')
    assert not r_matcher('', 'hello')
    assert not r_matcher('ab', 'abc')
    assert r_matcher('hello', '')
    assert r_matcher('hello', '[b-y][a-z1-2]')


def test_unit_match_substr():
    sub_matcher = grep.select_matcher(False, False, False, False)
    assert sub_matcher('hello', 'hello')
    assert sub_matcher('abchelloasdf', 'hello')
    assert not sub_matcher('', 'hello')
    assert not sub_matcher('ab', 'abc')
    assert sub_matcher('hello', '')


def test_unit_print_all(capsys):
    grep.print_all('f2', ['a', 'b', 'c'], False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'f2:a\nf2:b\nf2:c\n'
    grep.print_all('f1', ['a', 'b', 'c'], True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a\nb\nc\n'


def test_unit_print_count(capsys):
    grep.print_count('f1', ['a', 'b', 'c'], False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'f1:3\n'
    grep.print_count('file', ['a', 'b', 'c'], True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_get_matched_strings(capsys):
    r_matcher = grep.select_matcher(True, False, False, False)
    sub_matcher = grep.select_matcher(False, False, False, False)
    matched_strings = grep.get_matched_strings(['hello', 'hi', '1hello1'],
                                               'hello', sub_matcher)
    _, err = capsys.readouterr()
    assert err == ''
    assert matched_strings == ['hello', '1hello1']

    matched_strings = grep.get_matched_strings(['h', 'hi', '1hello1'],
                                               'h', sub_matcher)
    _, err = capsys.readouterr()
    assert err == ''
    assert matched_strings == ['h', 'hi', '1hello1']

    matched_strings = grep.get_matched_strings(['h', 'hi', '11'],
                                               '[a-z]', r_matcher)
    _, err = capsys.readouterr()
    assert err == ''
    assert matched_strings == ['h', 'hi']


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
