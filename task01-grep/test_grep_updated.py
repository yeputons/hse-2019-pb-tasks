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


def test_integrate_stdin_grep_xc(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf\nneedle\nneedle\nneed'))
    grep.main(['-xc', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_stdin_grep_lix_regex(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'fooooooooooo\nfo\nfoo\nFOo\nFO'))
    grep.main(['-lix', '-E', 'fo?o'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'fo\nfoo\nFOo\nFO\n'


def test_integrate_stdin_grep_xiv(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'WWWWWWOWWWWWWWW\nWOW\nwow\nwowowowoww'))
    grep.main(['-xiv', 'WOW'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'WWWWWWOWWWWWWWW\nwowowowoww\n'


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


def test_integrate_files_grep_lowercase_filenames_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('woooooooooow\nWow\nWWWWOWWWW')
    (tmp_path / 'b.txt').write_text('ababa\nababab\nbabbbb')
    (tmp_path / 'c.txt').write_text('Wow\nWow\nWow')
    monkeypatch.chdir(tmp_path)
    grep.main(['-il', 'WOW', 'a.txt', 'b.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nc.txt\n'


def test_integrate_files_grep_count_invert(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('woooooooooow\nWow\nWWWWOWWWW')
    (tmp_path / 'b.txt').write_text('ababa\nababab\nbabbbb')
    (tmp_path / 'c.txt').write_text('Wow\nWow\nWow')
    monkeypatch.chdir(tmp_path)
    grep.main(['-vc', 'Wow', 'a.txt', 'b.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\nb.txt:3\nc.txt:0\n'


def test_integrate_files_grep_invert_files_invert(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('woooooooooow\nWow\nWWWWOWWWW')
    (tmp_path / 'b.txt').write_text('ababa\nababab\nbabbbb')
    (tmp_path / 'c.txt').write_text('Wow\nWow\nWow')
    monkeypatch.chdir(tmp_path)
    grep.main(['-vL', 'Wow', 'a.txt', 'b.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'c.txt\n'


def test_needle_full_match_find():
    line = 'find something here, ffind, Find_here!'
    assert grep.find(line, 'find', False, False, True)


def test_regex_lowercase_find():
    line = 'find something here, FFFind, find f'
    assert grep.find(line, 'F*', True, True, False)
