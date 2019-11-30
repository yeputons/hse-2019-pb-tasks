#!/usr/bin/env python3
import io
import grep


def test_check_entry():
    assert not grep.check_entry('trash_needle_trash', 'needle', False, True, False, False)
    assert not grep.check_entry('trash_nedle_trash', 'needle', False, False, False, False)
    assert grep.check_entry('needle', 'ne.d.e', True, False, False, False)
    assert not grep.check_entry('needle', 'NeEdLe', False, True, True, True)


def test_get_lines_of_file(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('first line\nsecond line\nthird line')
    monkeypatch.chdir(tmp_path)
    lines = grep.get_lines_of_file(open('a.txt', 'r'))
    assert lines == ['first line', 'second line', 'third line']


def test_parse_files(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('first line\nsecond line\nthird line')
    (tmp_path / 'b.txt').write_text('FIRST LINE\nSECOND LINE\nTHIRD LINE')
    monkeypatch.chdir(tmp_path)
    lines = grep.parse_files([('a.txt', open('a.txt', 'r')), ('b.txt', open('b.txt', 'r'))])
    assert lines == [('a.txt', ['first line', 'second line', 'third line']), (
        'b.txt', ['FIRST LINE', 'SECOND LINE', 'THIRD LINE'])]


def test_search_in_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needle\nnedle\nneedle needle needle\ntrash')
    monkeypatch.chdir(tmp_path)
    grep.search_in_file('a.txt', False, False, False, False, grep.get_lines_of_file(
        open('a.txt', 'r')), 'needle', '{1}')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'needle\nneedle needle needle\n'
    grep.search_in_file('a.txt', True, False, False, False, grep.get_lines_of_file(
        open('a.txt', 'r')), 'ne.d.e', '{1}')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'needle\nneedle needle needle\n'


def test_count_in_lines():
    lines = ['needle', 'needle needle needle', 'nedle', 'trash']
    counter = grep.count_in_lines(lines, False, False, False, False, 'needle')
    assert counter == 2
    counter = grep.count_in_lines(lines, True, False, False, False, 'nee?d.e')
    assert counter == 3


def test_search_in_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('first line\nsecond line\nthird line')
    (tmp_path / 'b.txt').write_text('LINE LINE LINE\nTRRRRASH')
    monkeypatch.chdir(tmp_path)
    parse_data = grep.parse_files([('a.txt', open('a.txt', 'r')), ('b.txt', open('b.txt', 'r'))])
    grep.search_in_files(parse_data, False, False, False, True, 'line', True, '{0}:{1}')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:3\nb.txt:1\n'
    parse_data = grep.parse_files([('a.txt', open('a.txt', 'r')), ('b.txt', open('b.txt', 'r'))])
    grep.search_in_files(parse_data, False, False, False, False, 'line', False, '{0}:{1}')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:first line\na.txt:second line\na.txt:third line\n'


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