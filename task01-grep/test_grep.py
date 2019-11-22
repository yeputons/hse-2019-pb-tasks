#!/usr/bin/env python3
import io
import grep
import argparse


def test_print_from_file(capsys):
    grep.print_from_file(['pref needle', 'needle suf'], 'some_file.txt', 1)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle\nneedle suf\n'


def test_print_from_stdin(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.print_from_stdin(['3']) #amount of good strings
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_file_working(tmp_path, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    grep.file_working('a.txt', argparse.Namespace(needle='needl.', files=['a.txt', 'b.txt'], regex=True, count=False))
    grep.file_working('b.txt', argparse.Namespace(needle='needl.', files=['a.txt', 'b.txt'], regex=True, count=False))
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:pref needle\na.txt:needle suf\nb.txt:pref needle suf\n'


def test_stdin_working(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.stdin_working(argparse.Namespace(needle='needle', files=[], regex=False, count=False))
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_complex_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_complex_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_complex_stdin_grep_regex(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_complex_stdin_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'
