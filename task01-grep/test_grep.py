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


def test_making_list_files(tmp_path, monkeypatch):
    needle = 'needle'
    p = tmp_path / 'a.txt'
    p.write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    with p.open() as f:
        lines = grep.making_list(needle, f)
        assert lines == ['pref needle suf']


def test_making_list_in_stdin():
    output = io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    needle = 'needle'
    lines = grep.making_list(needle, output)
    assert lines == ['pref needle?', 'needle? suf', 'pref needle? suf']


def test_search_in_file_one_file(tmp_path, monkeypatch, capsys):
    needle = 'needle'
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt']
    counting = 0
    grep.search_in_file(files, needle, counting)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'
    counting = 1
    grep.search_in_file(files, needle, counting)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_search_in_file_many_files(tmp_path, monkeypatch, capsys):
    needle = 'needle'
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt', 'b.txt']
    counting = 0
    grep.search_in_file(files, needle, counting)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:pref needle\na.txt:needle suf\nb.txt:pref needle suf\n'
    counting = 1
    grep.search_in_file(files, needle, counting)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\nb.txt:1\n'


def test_search_in_stdin(monkeypatch, capsys):
    needle = 'needle'
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    counting = 0
    grep.search_in_stdin(needle, counting)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    counting = 1
    grep.search_in_stdin(needle, counting)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'
