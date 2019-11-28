#!/usr/bin/env python3
import io
from argparse import Namespace

import grep


def test_print_result(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    grep.print_result(['b.txt:1', 'a.txt:2'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_print_result_first(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    grep.print_result(['b.txt:aba'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:aba\n'


def test_print_result_first_second(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    grep.print_result(['1'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_format_lines():
    assert grep.format_lines('a', 'a.txt') == 'a.txt:a'
    assert grep.format_lines('2', 'a.txt') == 'a.txt:2'


def test_find_all_lines():
    lines = ['aba', 'bcd', 'banana']
    assert grep.find_all_lines('a', lines, False) == ['aba', 'banana']
    assert grep.find_all_lines('b', lines, False) == ['aba', 'bcd', 'banana']
    assert grep.find_all_lines('a*b', lines, True) == ['aba', 'bcd', 'banana']
    assert grep.find_all_lines('a*b', lines, False) == []
    assert grep.find_all_lines('abc', lines, False) == []


def test_calculate_result():
    assert grep.calculate_result('a.txt', 'a', False, False, 1, ['abc']) == ['abc']
    assert grep.calculate_result('a.txt', 'a', False, True, 1, ['abc']) == ['1']
    assert grep.calculate_result('a.txt', 'a', True, True, 1, ['abc']) == ['1']
    assert grep.calculate_result('a.txt', 'a', True, False, 1, ['abc']) == ['abc']
    assert grep.calculate_result('a.txt', 'a', False, False, 2, ['abc']) == ['a.txt:abc']
    assert grep.calculate_result('a.txt', 'a', False, True, 2, ['abc']) == ['a.txt:1']
    assert grep.calculate_result('a.txt', 'a', True, True, 2, ['abc']) == ['a.txt:1']
    assert grep.calculate_result('a.txt', 'a', True, False, 2, ['abc']) == ['a.txt:abc']
    assert grep.calculate_result('', 'a', False, False, 0, ['abc']) == ['abc']
    assert grep.calculate_result('', 'a', False, True, 0, ['abc']) == ['1']
    assert grep.calculate_result('', 'a', True, True, 0, ['abc']) == ['1']
    assert grep.calculate_result('', 'a', True, False, 0, ['abc']) == ['abc']


def test_parse_args():
    assert grep.parse_args(['-c', 'a', 'a.txt', 'b,txt']) == Namespace(
        count=True, files=['a.txt', 'b,txt'], needle='a', regex=False)
    assert grep.parse_args(['a', 'a.txt', 'b,txt']) == Namespace(
        count=False, files=['a.txt', 'b,txt'], needle='a', regex=False)
    assert grep.parse_args(['-E', 'a', 'a.txt', 'b,txt']) == Namespace(
        count=False, files=['a.txt', 'b,txt'], needle='a', regex=True)
    assert grep.parse_args(['-E', '-c', 'a', 'a.txt', 'b,txt']) == Namespace(
        count=True, files=['a.txt', 'b,txt'], needle='a', regex=True)
    assert grep.parse_args(['-c', 'a']) == Namespace(
        count=True, files=[], needle='a', regex=False)
    assert grep.parse_args(['a']) == Namespace(
        count=False, files=[], needle='a', regex=False)
    assert grep.parse_args(['-E', 'a']) == Namespace(
        count=False, files=[], needle='a', regex=True)
    assert grep.parse_args(['-E', '-c', 'a']) == Namespace(
        count=True, files=[], needle='a', regex=True)


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
    (tmp_path / 'a.txt').write_text('pref needle'
                                    '\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_integrate_files_grep_count_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_integrate_file_grep_count_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_integrate_stdin_grep_count_regex(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', '-E', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_the_same_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt', 'b.txt', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\nb.txt:1\nb.txt:1\na.txt:2\n'


def test_integrate_file_grep_empty_out(tmp_path, monkeypatch, capsys):
    (tmp_path / 'first.txt').write_text("what's\nwrong\nwith\nyou?\n")
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'wro*ng?s+', 'first.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_format_lines_1(capsys):
    result = 'a'
    name_file = 'a.txt'
    lines = grep.format_lines(result, name_file)
    out, err = capsys.readouterr()
    assert lines == 'a.txt:a'
    assert out == ''
    assert err == ''


def test_format_lines_2(capsys):
    result = 'a', 'bfg'
    name_file = 'a.txt'
    lines = grep.format_lines(result, name_file)
    out, err = capsys.readouterr()
    assert lines == "a.txt:('a', 'bfg')"
    assert out == ''
    assert err == ''
