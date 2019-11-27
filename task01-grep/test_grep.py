#!/usr/bin/env python3
import io
from typing import List
import grep


def test_integrate_stdin_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\npref needle? suf\nthank you OHneedHELP'))
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


def test_search_append():
    lines: List[str] = ['victor', 'love and piece']
    grep.search_append('win', 'wins', lines)
    assert lines.pop() == 'wins'
    grep.search_append('win', 'wns', lines)
    assert lines.pop() == 'love and piece'
    grep.search_append('v*y', 'victory', lines)
    assert lines.pop() == 'victory'
    grep.search_append('v*y', 'victoru', lines)
    assert lines.pop() == 'victor'


def test_print_file(capsys):  # DODODODOODODODODODODO
    lines: List[str] = ['thank you', 'a lot', 'thanks']
    file_name = 'hello, Olga:'

    grep.print_file(1, 1, file_name, lines)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'hello, Olga:3\n'

    grep.print_file(1, 0, file_name, lines)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'hello, Olga:thank you\nhello, Olga:a lot\nhello, Olga:thanks\n'

    grep.print_file(0, 1, file_name, lines)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'

    grep.print_file(0, 0, file_name, lines)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'thank you\na lot\nthanks\n'


def test_print_stdio(capsys):
    lines: List[str] = ['dead', 'line', 'deadline']
    grep.print_stdio(1, lines)
    out, err = capsys.readouterr()
    assert out == '3\n'
    assert err == ''
    grep.print_stdio(0, lines)
    out, err = capsys.readouterr()
    assert out == 'dead\nline\ndeadline\n'
    assert err == ''


def test_search_right_string_file():
    lines = ['ahaha', 'win', 'victory', 'ha']
    res = []
    for line in lines:
        grep.search_append('ha', line, res)
    assert res == ['ahaha', 'ha']

    lines = ['ahaha', 'win', 'victory', 'ha']
    res = []
    for line in lines:
        grep.search_append('no', line, res)
    assert res == []


def test_search_right_string_stdin():
    lines = ['lalaalla', 'win', 'nope', 'lllllla']
    res = []
    for line in lines:
        grep.search_append('la', line, res)
    assert res == ['lalaalla', 'lllllla']

    lines = ['lalaalla', 'win', 'nope', 'lllllla']
    res = []
    for line in lines:
        grep.search_append('grep', line, res)
    assert res == []
