#!/usr/bin/env python3

import io
import grep


def test_names_to_strings(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('ouou\noiio')
    (tmp_path / 'b.txt').write_text('')
    monkeypatch.chdir(tmp_path)
    tested_function = grep.names_to_strings(['a.txt', 'b.txt'])
    _, err = capsys.readouterr()
    assert err == ''
    assert tested_function == [['ouou', 'oiio'], []]


def test_stdin_files_to_strings(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'ouou\noiio'))
    tested_function = grep.stdin_to_strings()
    _, err = capsys.readouterr()
    assert err == ''
    assert tested_function == [['ouou', 'oiio']]


def test_match_string():
    assert grep.match_string('iwanttodie', 'die')
    assert grep.match_string('yuyewuoda', 'wu')
    assert grep.match_string('', '')
    assert not grep.match_string('8780000', '788')
    assert not grep.match_string('8', '788')
    assert not grep.match_string('too', 'tootoo')


def test_match_regex():
    assert grep.match_regex('io', '')
    assert grep.match_regex('io', '[a-q][b-z]')
    assert grep.match_regex('8', '[0-9]')
    assert not grep.match_regex('trytofind', '[0-9]')
    assert not grep.match_regex('800', '[a-u]')


def test_print_lines(capsys):
    grep.print_lines(['l1', 'l2'], 'iamtheonlyone', True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'l1\nl2\n'

    grep.print_lines(['line1', 'line2'], 'iamoneoffiles', False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'iamoneoffiles:line1\niamoneoffiles:line2\n'


def test_print_count(capsys):
    grep.print_count(['7', '8'], 'alone', True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'

    grep.print_count(['7', '8'], 'notalone', False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'notalone:2\n'


def test_find_matched(capsys):
    matched_strings = grep.find_matched(['oi', 'io', '90'],
                                        'o', grep.match_string)
    _, err = capsys.readouterr()
    assert err == ''
    assert matched_strings == ['oi', 'io']

    matched_strings = grep.find_matched(['7', '0', 'aoao'],
                                        '[0-9]', grep.match_regex)
    _, err = capsys.readouterr()
    assert err == ''
    assert matched_strings == ['7', '0']


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
