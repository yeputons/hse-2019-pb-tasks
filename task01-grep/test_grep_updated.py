#!/usr/bin/env python3
import grep


def test_integrate_files_grep_filenames_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)

    grep.main(['-l', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\na.txt\n'


def test_integrate_files_grep_invert(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)

    grep.main(['-v', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:the needl\n'


def test_integrate_files_grep_filenames_only_invert(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)

    grep.main(['-L', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''

    grep.main(['-Lv', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_integrate_files_grep_ignore_case(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref neEdle\nneedLe suf\n')
    (tmp_path / 'b.txt').write_text('the neeDl\npref nEedle suf')
    monkeypatch.chdir(tmp_path)

    grep.main(['-i', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref nEedle suf\na.txt:pref neEdle\na.txt:needLe suf\n'

    grep.main(['-iE', 'LE\\b', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref nEedle suf\na.txt:pref neEdle\na.txt:needLe suf\n'


def test_integrate_files_grep_full_match(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)

    grep.main(['-x', 'needle suf', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:needle suf\n'

    grep.main(['-xEv', '\\w+ \\w+', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\n'


def test_create_output_line():
    func = grep.create_output_line
    assert func(files=False, only_filenames=False) == '{line}'
    assert func(files=True, only_filenames=False) == '{filename}:{line}'
    assert func(files=False, only_filenames=True) == '{filename}'
    assert func(files=True, only_filenames=True) == '{filename}'


def test_does_line_match():
    func = grep.does_line_match
    line = '\t line inline (line) \\i\\n\\l\\i\\n\\e \t\n\n line'
    assert func(line, regex=False, needle='line')
    assert not func(line, regex=False, needle='LINE')
    assert func(line, regex=False, needle='LINE', ignore_case=True)
    assert not func(line, regex=False, needle='wax')
    assert func(line, regex=False, needle='\\l\\i\\n\\e')
    assert not func(line, regex=False, needle='line', full_match=True)
    assert func("full", regex=False, needle='FULL', ignore_case=True)
    assert func(line, regex=True, needle='l*e')
    assert not func(line, regex=True, needle='(l.?e)')
    assert func(line, regex=True, needle='(L.*E)', ignore_case=True)
    assert func('full', regex=True, needle='ful*l', full_match=True)
    assert func('', regex=False, needle='')
