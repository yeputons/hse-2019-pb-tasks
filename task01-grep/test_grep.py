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

# UNIT TESTS START


def test_print_in_files_one(capsys):    # FILES = 1
    file = 'a.txt'
    line = 'found'
    files = 1
    grep.print_in_files(files, file, line)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:found\n'


def test_print_in_files_zero(capsys):    # FILES = 0
    file = 'a.txt'
    line = 'found'
    files = 0
    grep.print_in_files(files, file, line)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'found\n'


def test_working_with_one_file(tmp_path, monkeypatch, capsys):    # NOT COUNT
    pattern = 'needle'
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt']
    count = False
    grep.working_with_files(files, pattern, count)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_working_with_one_file_count(tmp_path, monkeypatch, capsys):    # COUNT
    pattern = 'needle'
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt']
    count = True
    grep.working_with_files(files, pattern, count)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_working_with_many_files(tmp_path, monkeypatch, capsys):    # NOT COUNT
    pattern = 'needle'
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt', 'b.txt']
    count = False
    grep.working_with_files(files, pattern, count)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:pref needle\na.txt:needle suf\nb.txt:pref needle suf\n'


def test_working_with_many_files_count(tmp_path, monkeypatch, capsys):    # COUNT
    needle = 'needle'
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt', 'b.txt']
    count = True
    grep.working_with_files(files, needle, count)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\nb.txt:1\n'


def test_working_with_stdin(monkeypatch, capsys):    # NOT COUNT
    needle = 'needle'
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    count = False
    grep.working_with_stdin(needle, count)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_working_with_stdin_count(monkeypatch, capsys):    # COUNT
    needle = 'needle'
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    count = True
    grep.working_with_stdin(needle, count)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


# UNIT TESTS END
