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


def test_integrate_files_grep_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_integrate_file_grep_regex_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '-c', 'needle', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_integrate_stdin_grep_regex_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-E', '-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_file_grep_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_integrate_files_grep_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-l', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_integrate_files_grep_regex_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf\n')
    (tmp_path / 'c.txt').write_text('needlejf\na needle b\nneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '-l', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nc.txt\n'


def test_integrate_files_grep_ignore_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf\n')
    (tmp_path / 'c.txt').write_text('a o a o NEEDLE LEL\na needle b\nneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', '-l', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nc.txt\n'


def test_integrate_files_grep_fullmatch_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf\n')
    (tmp_path / 'c.txt').write_text('a o a o NEEDLE LEL\na needle b\nneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-x', '-l', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'c.txt\n'


def test_integrate_files_grep_ignore_reverse_strings_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf\n')
    (tmp_path / 'c.txt').write_text('a o a o NEEDLE LEL\na needle b\nneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', '-v', '-l', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_integrate_files_grep_ignore_reverse_strings_reverse_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf\n')
    (tmp_path / 'c.txt').write_text('a o a o NEEDLE LEL\na needle b\nneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', '-v', '-L', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nc.txt\n'


def test_integrate_files_grep_fullmatch_reverse_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf\n')
    (tmp_path / 'c.txt').write_text('a o a o NEEDLE LEL\na needle b\nneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-x', '-L', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\na.txt\n'


def test_integrate_files_grep_ignore_reverse_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf\n')
    (tmp_path / 'c.txt').write_text('a o a o NEEDLE LEL\na needle b\nneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', '-L', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_integrate_files_grep_regex_reverse_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf\n')
    (tmp_path / 'c.txt').write_text('needlejf\na needle b\nneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '-L', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_integrate_files_grep_reverse_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-L', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'