#!/usr/bin/env python3
import io
import grep
from grep import has_needle
from grep import find_in_file


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


def test_unit_has_needle():
    s = 'abcdef'
    needles_in = ['a', 'abcdef', 'ef', '']
    needles_not_in = ['ac', 'fa', 'abcdf']
    for needle in needles_in:
        assert has_needle(s, needle, False, False, False, False)
    for needle in needles_not_in:
        assert not has_needle(s, needle, False, False, False, False)


def test_unit_has_needle_regex():
    s = 'abacaba123adacabaaaa'
    needles_in = ['[adc]', '[1]', '.', 'd?', '', 'abacaba', 'abacaba...adacaba', 'acaba{4,}']
    needles_not_in = ['e+', 'abac{2}', 'abacaba...abacaba', 'a{5,}']
    for needle in needles_in:
        assert has_needle(s, needle, True, False, False, False)
    for needle in needles_not_in:
        assert not has_needle(s, needle, True, False, False, False)


def test_unit_find_in_file():
    lines = ['abra', 'cobra', 'masla', 'kavooo', 'z z z', '123o789', 'coq', '']
    needles = ['z', 'bra', 'o', '  ']
    results = [['z z z'], ['abra', 'cobra'], ['cobra', 'kavooo', '123o789', 'coq'], []]
    for i, needle in enumerate(needles):
        out = find_in_file(lines, needle, False, False, False, False)
        assert out == results[i]


def test_unit_find_in_file_regex(capsys):
    lines = ['abra', 'cobra', 'maslo', 'kavooo', 'ms', '123o789', 'cooq', '']
    needles = ['[ao]', 'ma?s', 'o{2,}']
    results = [['abra','cobra','maslo','kavooo','123o789','cooq'], ['maslo','ms'],['kavooo','cooq']]
    for i, needle in enumerate(needles):
        out = find_in_file(lines, needle, True, False, False, False)
        assert out == results[i]
