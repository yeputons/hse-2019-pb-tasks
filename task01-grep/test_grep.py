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
        assert has_needle(s, needle, False)
    for needle in needles_not_in:
        assert not has_needle(s, needle, False)


def test_unit_has_needle_regex():
    s = 'abacaba123adacabaaaa'
    needles_in = ['[adc]', '[1]', '.', 'd?', '', 'abacaba', 'abacaba...adacaba', 'acaba{4,}']
    needles_not_in = ['e+', 'abac{2}', 'abacaba...abacaba', 'a{5,}']
    for needle in needles_in:
        assert has_needle(s, needle, True)
    for needle in needles_not_in:
        assert not has_needle(s, needle, True)


def test_unit_find_in_file(capsys):
    lines = ['abra', 'cobra', 'masla', 'kavooo', 'z z z', '123o789', 'coq', '']
    needles = ['z', 'bra', 'o', '  ']
    results = ['q:z z z\n', 'q:abra\nq:cobra\n', 'q:cobra\nq:kavooo\nq:123o789\nq:coq\n', '']
    for i, needle in enumerate(needles):
        find_in_file(lines, needle, False, 'q:', False)
        out, err = capsys.readouterr()
        assert err == ''
        assert out == results[i]


def test_unit_find_in_file_count(capsys):
    lines = ['abram', 'cobram', 'maslom', 'kavooo', 'z z zq', '123o789', 'coq', '']
    needles = ['am', 'ram', 'o', '  ', 'q']
    results = ['2\n', '2\n', '5\n', '0\n', '2\n']
    for i, needle in enumerate(needles):
        find_in_file(lines, needle, False, '', True)
        out, err = capsys.readouterr()
        assert err == ''
        assert out == results[i]


def test_unit_find_in_file_regex(capsys):
    lines = ['abra', 'cobra', 'maslo', 'kavooo', 'ms', '123o789', 'cooq', '']
    needles = ['[ao]', 'ma?s', 'o{2,}']
    results = ['abra\ncobra\nmaslo\nkavooo\n123o789\ncooq\n', 'maslo\nms\n', 'kavooo\ncooq\n']
    for i, needle in enumerate(needles):
        find_in_file(lines, needle, True, '', False)
        out, err = capsys.readouterr()
        assert err == ''
        assert out == results[i]


def test_unit_find_in_file_regex_count(capsys):
    lines = ['abra', 'cobra', 'maslo', 'kavooo', 'ms', '123o789', 'cooq', '', 'cq']
    needles = ['', 'kavo+', 'co?q', 'o{3}', '[a-c]o?[a-s]']
    results = ['9\n', '1\n', '1\n', '1\n', '5\n']
    for i, needle in enumerate(needles):
        find_in_file(lines, needle, True, '', True)
        out, err = capsys.readouterr()
        assert err == ''
        assert out == results[i]
