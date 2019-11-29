#!/usr/bin/env python3
import io
import grep


def test_search_needle_in_line():
    assert grep.search_needle_in_line('test?', 'tes', True)
    assert not grep.search_needle_in_line('test?', 'tst', True)
    assert not grep.search_needle_in_line('tes?', 'test', False)
    assert grep.search_needle_in_line('tes?', 'tes?to', False)


def helper(check, capsys):
    out, err = capsys.readouterr()
    assert err == ''
    assert out == check


def test_print_asked_string(capsys):
    grep.print_asked_string([], True, '')
    helper('0\n', capsys)
    grep.print_asked_string([1, 2, 3, 4, 5], True, '')
    helper('5\n', capsys)


def test_find_in_file(tmp_path, capsys):
    (tmp_path / 'a.txt').write_text(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    with open(tmp_path / 'a.txt', 'r') as file:
        grep.find_in_file(file, 'needle?', True, False)
        helper('pref needle?\nneedle? suf\nthe needl\npref needle? suf\n', capsys)


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