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
    assert out == 'b.txt\n'

    grep.main(['-Lv', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\na.txt\n'


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
