#!/usr/bin/env python3
import io
import grep


def test_count(monkeypatch):
    lines = ['needle', 'ndl', 'pref', 'needleneedle', 'suf', 'needle needle']
    regex = 1
    pattern = 'needle'
    counter = grep.count(lines, regex, pattern)
    assert counter == 3
    pattern = 'n?dl?'
    counter = grep.count(lines, regex, pattern)
    assert counter == 4


def test_search_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the nendle\npref needle suf\nneedlen\n')
    monkeypatch.chdir(tmp_path)
    name = 'a.txt'
    check = 0
    regex = 0
    lines = grep.file_to_lines(name)
    pattern = 'needle'
    grep.search_file(name, check, regex, lines, pattern)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\nneedlen\n'
    regex = 1
    pattern = 'ne.dle'
    grep.search_file(name, check, regex, lines, pattern)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'the nendle\npref needle suf\nneedlen\n'


def test_file_to_lines(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('a\naaa\naaaaa\n')
    monkeypatch.chdir(tmp_path)
    file = 'a.txt'
    lines = grep.file_to_lines(file)
    assert lines == ['a', 'aaa', 'aaaaa']


def test_files_to_lines(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('a\naaa\naaaaa\n')
    (tmp_path / 'b.txt').write_text('bbbbb\nbbb\nb\n')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt', 'b.txt']
    lines = grep.files_to_lines(files)
    assert lines == [('a.txt', ['a', 'aaa', 'aaaaa']), ('b.txt', ['bbbbb', 'bbb', 'b'])]


def test_search_global(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref\nneedle\nsuf\n')
    (tmp_path / 'b.txt').write_text('neddle\nb\nneedle needle\n')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt', 'b.txt']
    regex = 0
    pattern = 'needle'
    count_check = 0
    grep.search_global(files, regex, pattern, count_check)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:needle\nb.txt:needle needle\n'

    count_check = 1
    grep.search_global(files, regex, pattern, count_check)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:1\nb.txt:1\n'

    regex = 1
    pattern = 'ne.dle'
    count_check = 0
    grep.search_global(files, regex, pattern, count_check)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:needle\nb.txt:neddle\nb.txt:needle needle\n'

    regex = 1
    pattern = 'ne.dle'
    count_check = 1
    grep.search_global(files, regex, pattern, count_check)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:1\nb.txt:2\n'


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