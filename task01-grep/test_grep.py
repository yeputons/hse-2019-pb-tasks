#!/usr/bin/env python3
import io
import pytest
import grep
from grep import get_lines
from grep import read_files
from grep import filter_lines
from grep import count_lines
from grep import print_output
from grep import print_counter


def test_get_lines():
    lines = ['Food', 'sleep', '']
    assert get_lines(lines) == lines


def test_read_files_empty(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('')
    monkeypatch.chdir(tmp_path)
    assert read_files('a.txt') == []


def test_read_files_not_empty(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('Ah sacré papa,\nDis-moi où es-tu caché?')
    monkeypatch.chdir(tmp_path)
    assert read_files('a.txt') == ['Ah sacré papa,', 'Dis-moi où es-tu caché?']


def test_filter_lines_regex():
    lines = ['Jingle', 'Bells', 'Jungle']
    assert filter_lines(lines, r'J\d?', 1) == ['Jingle', 'Jungle']


def test_filter_lines_not_regex():
    lines = ['Jingle', 'Bells', 'Jungle']
    assert filter_lines(lines, 'Ju', 0) == ['Jungle']


def test_count_lines():
    lines = ['Jingle', 'Bells', 'Jungle']
    assert count_lines(lines) == 3


def test_count_lines_empty():
    lines = []
    assert count_lines(lines) == 0


def test_print_output_one_file(capsys):
    lines = ['Jingle', 'Bells', 'Jungle']
    print_output(lines, 0, 'a.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Jingle\nBells\nJungle\n'


def test_print_output_more_files(capsys):
    lines = ['Jingle', 'Bells', 'Jungle']
    print_output(lines, 1, 'a.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:Jingle\na.txt:Bells\na.txt:Jungle\n'


def test_print_counter_one_file(capsys):
    print_counter(3, 0, 'a.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_print_counter_many_files(capsys):
    print_counter(3, 1, 'a.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:3\n'


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


def test_integrate_stdin_grep_count_empty(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        '\n\n\n'))
    grep.main(['-c', ''])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_stdin_regex_grep_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pirozhok\nIf pir\npi day\nI dont like lines without any meaning\nchipseki!'))
    grep.main(['-c', '-E', '.. '])
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


def test_integrate_file_regex_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'pre.', 'a.txt'])
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
    (tmp_path / 'a.txt').write_text('Sotto il sole, sotto il sole\nDi Riccione, di Riccione\n')
    (tmp_path / 'b.txt').write_text('Quasi quasi mi pento\nE non ci penso più, e non ci penso più')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'to', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:1\n'


def test_integrate_files_grep_count_empty(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('')
    (tmp_path / 'b.txt').write_text('')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:0\na.txt:0\n'


def test_integrate_files_grep_regex_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('Promise me a place\nIn your house of memories')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', ' . ', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_file_not_exist():
    with pytest.raises(SystemExit):
        grep.main(['-c', '-E', ' . ', 'a.txt'])