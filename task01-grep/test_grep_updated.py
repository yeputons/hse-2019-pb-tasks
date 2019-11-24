#!/usr/bin/env python3
import io
import grep


def test_integrate_stdin_invert(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle?\nno'))
    grep.main(['-v', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'the needl\nno\n'


def test_integrate_stdin_invert_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nnEEdle suf\nthe needl\npref needle?\nno'))
    grep.main(['-v', '-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_stdin_invert_igncase(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'needle\nnEEdle suf\nthe needl\npref needle?\nno'))
    grep.main(['-v', '-i', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'the needl\nno\n'


def test_integrate_stdin_invert_regex(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'needle\nnEEdl\nneedl\nhey'))
    grep.main(['-v', '-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'nEEdl\nhey\n'


def test_integrate_stdin_igncase(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'needle\nnEEdle suf\nthe needl\npref needle?\nno'))
    grep.main(['-i', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'needle\nnEEdle suf\npref needle?\n'


def test_integrate_stdin_igncase_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'needle\nnEEdle suf\nthe needl\npref needle?\nno'))
    grep.main(['-i', '-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_stdin_igncase_regex(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'needle\nnEEdl\nneedl\nhey'))
    grep.main(['-i', '-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'needle\nnEEdl\nneedl\n'


def test_integrate_stdin_fullmatch(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'needle\nnEEdle suf\nthe needl\npref needle?\nno'))
    grep.main(['-x', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'needle\n'


def test_integrate_stdin_fullmatch_invert(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'needle\nnEEdle suf\nthe needl\npref needle?\nno'))
    grep.main(['-x', '-v', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'nEEdle suf\nthe needl\npref needle?\nno\n'


def test_integrate_files_invert(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-v', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:the needl\n'


def test_integrate_files_match(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-l', 'needle', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nb.txt\n'


def test_integrate_files_no_match(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-L', 'needle', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_integrate_files_no_match_invert(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-L', '-v', 'needle', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_integrate_files_fullmatch_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needle\nno\nyes\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-x', '-c', 'needle', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:1\nb.txt:0\n'


def test_integrate_files_fullmatch_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needle\nno\nyes\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('needl\npref suf\nneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-x', '-E', 'needle?', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:needle\nb.txt:needl\nb.txt:needle\n'
