#!/usr/bin/env python3
import io
import argparse
import grep


def test_integrate_stdin_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_to_find():
    assert grep.find('ahhhe', 'h*i?', True)
    assert grep.find('colouuuur', 'colou*r', True)
    assert not grep.find('color', 'colou+r', True)
    assert not grep.find('ahhhe', 'h*i?', False)
    assert grep.find('sd', '', False)
    assert grep.find('sdfsdassdf', 'as', False)


def test_print_result(capsys):
    grep.print_result('sleep.txt', 2, 'sleepsleepsleeeeeep')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'sleep.txt:sleepsleepsleeeeeep\n'
    grep.print_result('sleep.txt', 1, 'should I go to sleep?')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'should I go to sleep?\n'
    grep.print_result('notsleep.txt', 1, 'yes, i should, but i havent done my English hw yet')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'yes, i should, but i havent done my English hw yet\n'


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


def test_counter(tmp_path, monkeypatch, capsys):
    args = argparse.Namespace(regex=False, files=[], needle='needle', count=True)
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    with open('a.txt', 'r') as in_file:
        grep.counter(in_file, args, 'a.txt')
        out, err = capsys.readouterr()
        assert err == ''
        assert out == '2\n'
    (tmp_path / 'b.txt').write_text('')
    monkeypatch.chdir(tmp_path)
    with open('b.txt', 'r') as in_file:
        grep.counter(in_file, args, 'b.txt')
        out, err = capsys.readouterr()
        assert err == ''
        assert out == '0\n'


def test_string_finder(tmp_path, monkeypatch, capsys):
    args = argparse.Namespace(regex=False, files=['a.txt'], needle='needle', count=False)
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    with open('a.txt', 'r') as in_file:
        grep.string_finder(in_file, args, 'a.txt')
        out, err = capsys.readouterr()
        assert err == ''
        assert out == 'pref needle\nneedle suf\n'
    (tmp_path / 'b.txt').write_text('')
    monkeypatch.chdir(tmp_path)
    with open('b.txt', 'r') as in_file:
        grep.string_finder(in_file, args, 'b.txt')
        out, err = capsys.readouterr()
        assert err == ''
        assert out == ''
    (tmp_path / 'c.txt').write_text('pref needle\nwhy suf\n')
    monkeypatch.chdir(tmp_path)
    with open('c.txt', 'r') as in_file:
        grep.string_finder(in_file, args, 'c.txt')
        out, err = capsys.readouterr()
        assert err == ''
        assert out == 'pref needle\n'


def test_finder(tmp_path, monkeypatch, capsys):
    args = argparse.Namespace(regex=False, files=['a.txt'], needle='needle', count=False)
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    with open('a.txt', 'r') as in_file:
        grep.finder(in_file, args, 'a.txt')
        out, err = capsys.readouterr()
        assert err == ''
        assert out == 'pref needle\nneedle suf\n'
    args = argparse.Namespace(regex=False, files=['a.txt'], needle='needle', count=True)
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    with open('a.txt', 'r') as in_file:
        grep.finder(in_file, args, 'a.txt')
        out, err = capsys.readouterr()
        assert err == ''
        assert out == '2\n'
