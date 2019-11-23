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


def test_print_file_with_counter(capsys):
    grep.print_for_files(True, 'a.txt', 3, [], 2)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:3\n'


def test_print_file_without_counter(capsys):
    grep.print_for_files(2, 'a.txt', 'abc', False, 0)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:abc\n'


def test_print_line_without_counter(capsys):
    grep.print_for_lines('abc', False, 0)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'abc\n'


def test_print_result_line_with_counter(capsys):
    grep.print_for_lines('abc', True, 1)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_for_files_with_file_names_error(capsys):
    grep.for_files_with_file_names(['a.txt', 'b.txt'], 'pattern', True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Error: file a.txt is not opened.\nError: file b.txt is not opened.\n'


def test_for_files_with_file_names_with_counter(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.for_files_with_file_names(['a.txt', 'b.txt'], 'needle', True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:1\nb.txt:1\n'
