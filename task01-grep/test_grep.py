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
    assert grep.format_lines('a', 'a.txt', False, False) == 'a.txt:a'
    assert grep.format_lines('2', 'a.txt', False, False) == 'a.txt:2'
    assert grep.format_lines('2', 'a.txt', True, False) == 'a.txt'


def test_find_all_lines():
    lines = ['aba', 'bcd', 'banana']
    assert grep.find_all_lines('a', lines, False, False, False, False) == ['aba', 'banana']
    assert grep.find_all_lines('b', lines, False, False, False, False) == ['aba', 'bcd', 'banana']
    assert grep.find_all_lines('a*b', lines, True, False, False, False) == ['aba', 'bcd', 'banana']
    assert grep.find_all_lines('a*b', lines, False, False, False, False) == []
    assert grep.find_all_lines('abc', lines, False, False, False, False) == []
    assert grep.find_all_lines('A', lines, True, True, False, False) == ['aba', 'banana']
    assert grep.find_all_lines('aba', lines, True, True, True, False) == ['aba']
    assert grep.find_all_lines('a', lines, True, True, False, True) == ['bcd']
    assert grep.find_all_lines('a', lines, True, True, True, True) == ['aba', 'bcd', 'banana']


def test_calculate_result():
    assert grep.calculate_result('a.txt', 'a', False, False, False, False,
                                 False, False, False, 1, ['abc']) == ['abc']
    assert grep.calculate_result('a.txt', 'a', False, True, False, False,
                                 False, False, False, 1, ['abc']) == ['1']
    assert grep.calculate_result('a.txt', 'a', True, True, False, False,
                                 False, False, False, 1, ['abc']) == ['1']
    assert grep.calculate_result('a.txt', 'a', True, False, False, False,
                                 False, False, False, 1, ['abc']) == ['abc']
    assert grep.calculate_result('a.txt', 'a', False, False, False, False,
                                 False, False, False, 2, ['abc']) == ['a.txt:abc']
    assert grep.calculate_result('a.txt', 'a', False, True, False, False, False,
                                 False, False, 2, ['abc']) == ['a.txt:1']
    assert grep.calculate_result('a.txt', 'a', True, True, False, False, False,
                                 False, False, 2, ['abc']) == ['a.txt:1']
    assert grep.calculate_result('a.txt', 'a', True, False, False, False,
                                 False, False, False, 2, ['abc']) == ['a.txt:abc']
    assert grep.calculate_result('', 'a', False, False, 0, False, False,
                                 False, False, False, ['abc']) == ['abc']
    assert grep.calculate_result('', 'a', False, True, 0, False, False,
                                 False, False, False, ['abc']) == ['1']
    assert grep.calculate_result('', 'a', True, True, 0, False, False,
                                 False, False, False, ['abc']) == ['1']
    assert grep.calculate_result('', 'a', True, False, 0, False, False,
                                 False, False, False, ['abc']) == ['abc']
    assert grep.calculate_result('', 'a', True, False, 0, True, True,
                                 True, True, False, ['abc']) == ['1']


def test_parse_args():
    assert grep.parse_args(['-c', 'a', 'a.txt', 'b,txt']) == Namespace(absent=False,
                                                                       count=True,
                                                                       files=['a.txt', 'b,txt'],
                                                                       full=False,
                                                                       ignore=False,
                                                                       needle='a',
                                                                       presence=False,
                                                                       regex=False,
                                                                       reverse=False)
    assert grep.parse_args(['-c', 'a']) == Namespace(absent=False,
                                                     count=True, files=[],
                                                     full=False, ignore=False,
                                                     needle='a',
                                                     presence=False, regex=False,
                                                     reverse=False)
    assert grep.parse_args(['a']) == Namespace(absent=False,
                                               count=False, files=[],
                                               full=False, ignore=False,
                                               needle='a', presence=False,
                                               regex=False, reverse=False)
    assert grep.parse_args(['-E', 'a']) == Namespace(absent=False, count=False,
                                                     files=[], full=False,
                                                     ignore=False,
                                                     needle='a', presence=False,
                                                     regex=True, reverse=False)
    assert grep.parse_args(['-E', '-c', 'a']) == Namespace(absent=False, count=True,
                                                           files=[], full=False,
                                                           ignore=False,
                                                           needle='a', presence=False,
                                                           regex=True, reverse=False)
    assert grep.parse_args(['-E', '-l', '-x', '-i', '-v', '-c', 'a']) == Namespace(absent=False,
                                                                                   count=True,
                                                                                   files=[],
                                                                                   full=True,
                                                                                   ignore=True,
                                                                                   needle='a',
                                                                                   presence=True,
                                                                                   regex=True,
                                                                                   reverse=True)
    assert grep.parse_args(['-E', '-L', '-x', '-i', '-v', '-c', 'a']) == Namespace(absent=True,
                                                                                   count=True,
                                                                                   files=[],
                                                                                   full=True,
                                                                                   ignore=True,
                                                                                   needle='a',
                                                                                   presence=False,
                                                                                   regex=True,
                                                                                   reverse=True)
    assert grep.parse_args(['-E', '-c', '-x', '-i', '-v', 'a']) == Namespace(absent=False,
                                                                             count=True,
                                                                             files=[],
                                                                             full=True,
                                                                             ignore=True,
                                                                             needle='a',
                                                                             presence=False,
                                                                             regex=True,
                                                                             reverse=True)


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
