#!/usr/bin/env python3

import io
import grep

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


def test_integrate_file_grep_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle\n'


def test_integrate_files_grep_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\n')
    (tmp_path / 'b.txt').write_text('the needle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:pref needle\nb.txt:the needle\n'


def test_integrate_file_grep_regex_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\n'


def test_integrate_files_grep_regex_failed(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\n')
    (tmp_path / 'b.txt').write_text('the needl\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:pref needle\n'


def test_regular_expression_check():
    if grep.regular_expression_check('mem', 'memory', True, '', False) == 1:
        print("Test of regular_expression_check is OK")
    else:
        print("Test of regular_expression_check FAILED")


def test_second_regular_expression_check():
    if grep.regular_expression_check('mem', 'memory', False, '', False) == 0:
        print("Test of regular_expression_check is OK")
    else:
        print("Test of regular_expression_check FAILED")


def test_third_regular_expression_check(capsys):
    grep.regular_expression_check('m*m', 'memory', False, 'some.txt', True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'some.txt:memory\n'


def test_which_keys_included():
    if grep.which_keys_included(False, False, 'mem', 'memory', '', False) == 1:
        print("Test of regular_expression_check is OK")
    else:
        print("Test of regular_expression_check FAILED")


def test_2_which_keys_included():
    if grep.which_keys_included(True, True, 'm*mm', 'memory', 'mem', False) == 1:
        print("Test of regular_expression_check is OK")
    else:
        print("Test of regular_expression_check FAILED")


def test_print_format(capsys):
    grep.print_format('some.txt', 'mem', True,
                      False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'some.txt:mem\n'


def test_2_print_format(capsys):
    grep.print_format('some.txt', 'mem', True,
                      True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
