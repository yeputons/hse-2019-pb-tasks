#!/usr/bin/env python3
import io
import sys
import grep


def test_integrate_stdin_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_integrate_stdin_grep__regex(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_integrate_stdin_grep__regex_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-c', '-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


def test_integrate_stdin_grep__count(monkeypatch, capsys):
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


def test_integrate_file_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


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


def test_integrate_file_grep__regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\npref needle? suf\nsuf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle?', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_integrate_file_grep__regex_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\npref needle? suf\nsuf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'needle?', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


def test_integrate_files_grep__regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\nfriend')
    (tmp_path / 'b.txt').write_text('the needl\npref needle? suf\nsuf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle?', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:the needl\nb.txt:pref needle? suf\n' \
                  'a.txt:pref needle?\na.txt:needle? suf\na.txt:the needl\n'


def test_integrate_files_grep__regex_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\nfriend')
    (tmp_path / 'b.txt').write_text('the needl\npref needle? suf\nsuf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'needle?', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:2\na.txt:3\n'


def test_unit_find_regex__true():
    args = grep.parse(['-E', 'needle?'])
    ans = grep.find_regex(args, 'the needl')
    assert ans


def test_unit_find_regex__false():
    args = grep.parse(['-E', 'needle?'])
    ans = grep.find_regex(args, 'homework')
    assert not ans


def test_unit_find_str__true():
    args = grep.parse(['needle'])
    ans = grep.find_regex(args, 'pref needle')
    assert ans


def test_unit_find_str__false():
    args = grep.parse(['needle'])
    ans = grep.find_regex(args, 'homework')
    assert not ans


def test_unit_print_file__lines(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\nfriend')
    monkeypatch.chdir(tmp_path)
    args = grep.parse(['-E', 'needle?', 'a.txt'])
    grep.print_lines(['pref needle?', 'needle? suf', 'the needl',
                      'pref needle? suf'], args, 'a.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_unit_print_files__lines(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\nfriend')
    (tmp_path / 'b.txt').write_text('the needle\npref needle? suf\nsuf')
    monkeypatch.chdir(tmp_path)
    args = grep.parse(['-E', 'needle?', 'b.txt', 'a.txt'])
    grep.print_lines(['the needl', 'pref needle? suf'], args, 'b.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:the needl\nb.txt:pref needle? suf\n'


def test_unit_print_file__count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\nfriend')
    monkeypatch.chdir(tmp_path)
    args = grep.parse(['-c', '-E', 'needle?', 'a.txt'])
    grep.print_lines(['pref needle?', 'needle? suf',
                      'the needl', 'pref needle? suf'], args, 'a.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


def test_unit_print_files__count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\nfriend')
    (tmp_path / 'b.txt').write_text('the needle\npref needle? suf\nsuf')
    monkeypatch.chdir(tmp_path)
    args = grep.parse(['-c', '-E', 'needle?', 'b.txt', 'a.txt'])
    grep.print_lines(['the needl', 'pref needle? suf'], args, 'b.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:2\n'


def test_unit_find_lines__regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\nfriend')
    (tmp_path / 'b.txt').write_text('the needl\npref needle? suf\nsuf')
    monkeypatch.chdir(tmp_path)
    args = grep.parse(['-E', 'needle?', 'b.txt', 'a.txt'])
    with open('b.txt', 'r') as in_file:
        grep.find_lines(args, in_file, 'b.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:the needl\nb.txt:pref needle? suf\n'


def test_unit_find_lines__str(tmp_path, monkeypatch, capsys):
    (tmp_path / 'b.txt').write_text('the needle\npref needle? suf\nsuf')
    monkeypatch.chdir(tmp_path)
    args = grep.parse(['needle', 'b.txt'])
    with open('b.txt', 'r') as in_file:
        grep.find_lines(args, in_file, 'b.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'the needle\npref needle? suf\n'


def test_unit_find_lines__count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    args = grep.parse(['-c', '-E', 'needle?'])
    grep.find_lines(args, sys.stdin)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'
