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


def test_integrate_stdin_regex_grep_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-E', '-c', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_integrate_file_grep_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle?', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_integrate_file_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_integrate_file_grep_regex_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '-c', 'needle?', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


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


def test_integrate_files_grep_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needle? suf\nthe needl\npref needle? suf')
    (tmp_path / 'b.txt').write_text('needle!\nneed suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle?', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:needle? suf\na.txt:the needl\na.txt:pref needle? suf\nb.txt:needle!\n'


def test_integrate_files_grep_regex_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    (tmp_path / 'b.txt').write_text('needle!\nneed suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '-c', 'needle?', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:4\nb.txt:1\n'


def test_grep_process_lines(tmp_path, monkeypatch):
    source = tmp_path / 'name.txt'
    source.write_text('pref needle?\nneedle? suf\npref needle? suf\nneed')
    monkeypatch.chdir(tmp_path)
    with open(source, 'r') as file:
        lines = grep.process_lines(file, 'needle?', 1)
        assert lines == ['3']


def test_grep_print_lines(capsys):
    lines = ['all\ntests\nare\npassed\nsuccessfully']
    grep.print_lines(lines)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'all\ntests\nare\npassed\nsuccessfully\n'
