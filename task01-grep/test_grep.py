#!/usr/bin/env python3
import io
import sys
import re
import grep


# --------------------------------INTEGRATE-----------------------------------------------

# stdin


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


def test_integrate_stdin_grep_count_regex(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-E', '-c', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


# one FILE

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


def test_integrate_file_grep_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle?', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'the needl\npref needle suf\n'


def test_integrate_file_grep_count_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'needle?', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


# many FILES

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
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle?', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:the needl\nb.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_integrate_files_grep_regex_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '-c', 'needle?', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:2\na.txt:2\n'


# --------------------------------------------UNIT------------------------------------------


def test_unit_parse_args():
    ans = grep.parse_args(['-E', 'needle?', 'b.txt', 'a.txt'])
    assert ans.regex is True
    assert ans.count is False
    assert ans.pattern == 'needle?'
    assert ans.files == ['b.txt', 'a.txt']


def test_strip_lines_from_file(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('one\ntwo\n')
    monkeypatch.chdir(tmp_path)
    with open('a.txt', 'r') as file:
        assert grep.strip_lines(file) == ['one', 'two']


def test_strip_lines_from_stdin(monkeypatch):
    monkeypatch.setattr('sys.stdin', io.StringIO('one\ntwo\n'))
    assert grep.strip_lines(sys.stdin) == ['one', 'two']


# def test_filter_lines_by_re():
#     lines = ['kek', 'lol ke', 'lol']
#     pattern = re.compile('ke?')
#     assert grep.filter_lines_by_re(lines, pattern) == ['kek', 'lol ke']
#
#
# def test_filter_blocks():
#     blocks = [['lol ke', 'lol'], ['kek']]
#     pattern = re.compile('ke?')
#     assert grep.filter_blocks(blocks, pattern) == [['lol ke'], ['kek']]


def test_map_blocks():
    blocks = [['lol ke', 'lol'], ['kek']]
    assert grep.map_blocks(blocks) == [['2'], ['1']]


def test_add_filename_prefix_to_lines():
    lines = ['boomer', 'or not']
    source = 'ok,'
    assert grep.add_filename_prefix_to_lines((lines, source)) == ['ok,:boomer', 'ok,:or not']


def test_print_blocks(capsys):
    blocks = [['a', 'x'], ['b']]
    grep.print_blocks(blocks)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a\nx\nb\n'