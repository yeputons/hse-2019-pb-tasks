#!/usr/bin/env python3
import io
from argparse import Namespace
import grep


def test_unit_find_in_str():
    assert grep.find_in_str('str', 'prefstr', [])
    assert grep.find_in_str('str', 'strsuf', [])
    assert grep.find_in_str('str', 'str', [])
    assert not grep.find_in_str('str', 'std', [])
    assert not grep.find_in_str('str', 'Str', [])
    assert not grep.find_in_str('str', 'sTr', [])

    assert grep.find_in_str('str', 'str', ['regex'])
    assert grep.find_in_str('a?', 'a', ['regex'])
    assert grep.find_in_str('ab.*ef', 'abcdef', ['regex'])
    assert not grep.find_in_str('aba+', 'abcbaa', ['regex'])


def test_unit_get_matching_args():
    assert grep.get_matching_args(Namespace()) == []
    assert grep.get_matching_args(Namespace(regex=True)) == ['regex']


def test_unit_find_in_files_or_stdin(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('sssstr\nstr\ntr')
    (tmp_path / 'b.txt').write_text('st\nssssttttrrr\nsstrr')
    monkeypatch.chdir(tmp_path)
    assert grep.find_in_files_or_stdin(
        ['a.txt', 'b.txt'],
        'str',
        []) == [('a.txt', ['sssstr', 'str']), ('b.txt', ['sstrr'])]

    monkeypatch.setattr('sys.stdin', io.StringIO(
        'st\nssttr\nsstrr'))
    assert grep.find_in_files_or_stdin(
        None,
        'str',
        []) == [('stdin', ['sstrr'])]


def test_unit_to_count():
    assert grep.to_count([
        ('a', ['1', '2', '3']),
        ('b', []),
        ('c', ['1'])]) == [('a', 3), ('b', 0), ('c', 1)]


def test_unit_print_matches(capsys):
    all_matches = [('a.txt', ['abc', 'def']), ('b.txt', [])]
    grep.print_matches(all_matches, [], grep.get_output_format(len(all_matches), []))
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:abc\na.txt:def\n'

    grep.print_matches(all_matches, ['count'], grep.get_output_format(len(all_matches), ['count']))
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\nb.txt:0\n'


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
    (tmp_path / 'a.txt').write_text('prefneedle\nneedlesuf\n')
    (tmp_path / 'b.txt').write_text('theneedl\nprefneedlesuf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'b.txt', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:prefneedlesuf\na.txt:prefneedle\na.txt:needlesuf\nb.txt:prefneedlesuf\n'


def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'
