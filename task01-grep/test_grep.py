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
    assert out == [
        'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n']


def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_unit_stdin_count_regex(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.search_std('needle?', True, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


def test_unit_file_count_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt']
    grep.search_files(files, 'needle?', True, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


def test_unit_stdin_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.search_std('needle', True, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_unit_files_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt', 'b.txt']
    grep.search_files(files, 'needle', True, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\nb.txt:1\n'


def test_unit_stdin(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.search_std('needle', False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle\nneedle suf\npref needle suf\n'


def test_unit_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt', 'b.txt']
    grep.search_files(files, 'needle', False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == [
        'a.txt:pref needle\na.txt:needle suf\nb.txt:pref needle suf\n']


def test_unit_file_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt']
    grep.search_files(files, 'needle?', False, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_unit_files_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\n')
    (tmp_path / 'b.txt').write_text('pref needl\n')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt', 'b.txt']
    grep.search_files(files, 'needle?', False, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:the needl\nb.txt:pref needl\n'


def test_unit_stdin_regex(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.search_std('needle?', False, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'
