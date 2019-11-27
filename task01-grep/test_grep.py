#!/usr/bin/env python3
import io
import argparse
import sys
import grep


def test_format_lines_many(tmp_path, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle gref\n')
    out = grep.format_lines(argparse.Namespace(
        needle='.ref', files=['a.txt', 'b.txt'], regex=True, cnt=False),
                            ['pref needle', 'needle gref'], 'a.txt')
    _, err = capsys.readouterr()
    assert err == ''
    assert out == ['a.txt:pref needle', 'a.txt:needle gref']


def test_format_lines_many_cnt(tmp_path, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle gref\n')
    out = grep.format_lines(argparse.Namespace(
        needle='.ref', files=['a.txt', 'b.txt'], regex=True, cnt=True),
                            ['pref needle', 'needle gref'], 'a.txt')
    _, err = capsys.readouterr()
    assert err == ''
    assert out == ['a.txt:2']


def test_format_lines_one(tmp_path, capsys):
    (tmp_path / 'b.txt').write_text('pref needle\nneedle tref\ntref card\n')
    out = grep.format_lines(argparse.Namespace(
        needle='.ref', files=['b.txt'], regex=True, cnt=False),
                            ['pref needle', 'needle gref', 'tref card'], 'b.txt')
    _, err = capsys.readouterr()
    assert err == ''
    assert out == ['pref needle', 'needle gref', 'tref card']


def test_format_lines_one_cnt(tmp_path, capsys):
    (tmp_path / 'b.txt').write_text('pref needle\nneedle tref\ntref card\n')
    out = grep.format_lines(argparse.Namespace(
        needle='.ref', files=['b.txt'], regex=True, cnt=True),
                            ['pref needle', 'needle gref', 'tref card'], 'b.txt')
    _, err = capsys.readouterr()
    assert err == ''
    assert out == ['3']


def test_file_working(tmp_path, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    with open('a.txt', 'r') as f:
        grep.working(argparse.Namespace(
            needle='.ref', files=['a.txt', 'b.txt'], regex=True, cnt=False), f, 'a.txt')
    with open('b.txt', 'r') as f:
        grep.working(argparse.Namespace(
            needle='.ref', files=['a.txt', 'b.txt'], regex=True, cnt=False), f, 'b.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:pref needle\nb.txt:pref needle suf\n'


def test_stdin_working(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.working(argparse.Namespace(needle='needle', files=[], regex=False, cnt=False),
                 source=sys.stdin, filename='')
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
