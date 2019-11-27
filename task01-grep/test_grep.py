#!/usr/bin/env python3
import io
import grep


# unit tests
def test_unit_search_as_regex_ok():
    assert grep.search_as_regex('123*', 'onetwothree1j12jj123sd')


def test_unit_search_as_regex_false():
    assert not grep.search_as_regex('needle', 'needl')


def test_unit_search_as_regex():
    assert grep.search_as_regex('qt?qt', 'qqt')


def test_unit_search_as_regex_multiple():
    assert grep.search_as_regex('a*', 'aaaaaaaaaaaaa')


def test_unit_search_as_string_ok():
    assert grep.search_as_string('qwe', 'Hello qwe')


def test_unit_search_as_string_not_regex():
    assert not grep.search_as_string('qwe?', 'Hello qwe')


def test_unit_search_as_string():
    assert grep.search_as_string('a*', 'Hello a*')


def test_unit_parse(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    file = open('a.txt', 'r')
    output = list()
    grep.parse(file, 'needle', grep.search_as_string, output)
    assert output == ['pref needle suf']


def test_unit_parse_empty(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    file = open('a.txt', 'r')
    output = list()
    grep.parse(file, 'needlee', grep.search_as_string, output)
    assert output == []


def test_unit_parse_regex(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf\nneedy')
    monkeypatch.chdir(tmp_path)
    file = open('a.txt', 'r')
    output = list()
    grep.parse(file, 'needle?', grep.search_as_regex, output)
    assert output == ['the needl', 'pref needle suf']


# integrate tests
def test_integrate_stdin_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_integrate_stdin_grep_different_flags(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-c', '-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


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


def test_integrate_stdin_count_zero(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', 'needlestr'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '0\n'


def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_integrate_file_grep_empty(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle?', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_integrate_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt: pref needle suf\na.txt: pref needle\na.txt: needle suf\n'


def test_integrate_files_grep_empty_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('There is nothing')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt: pref needle suf\n'


def test_integrate_files_grep_same_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt: pref needle\na.txt: needle suf\na.txt: pref needle\na.txt: needle suf\n'


def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt: 1\na.txt: 2\n'


def test_integrate_files_grep_count_empty(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'the', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt: 1\na.txt: 0\n'


def test_integrate_files_grep_count_same_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'a.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt: 2\na.txt: 2\n'
