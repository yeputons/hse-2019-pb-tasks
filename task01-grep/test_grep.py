#!/usr/bin/env python3
import io
import sys
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


def test_integrate_stdin_regex_grep_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-E', '-c', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


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


def test_integrate_files_regex_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_parser_init():
    parser = grep.init_parser()
    assert parser is not None


def test_add_found_needle():
    listtest = []
    grep.add_found_needle('Are you sleeping?', 'sleeping?', False, sys.stdin, 1, listtest)
    assert listtest == ['Are you sleeping?']


def test_add_found_regex_needle():
    listtest = []
    grep.add_found_needle('Are you sleeping?', 'sleep?', True, sys.stdin, 1, listtest)
    assert listtest == ['Are you sleeping?']


def test_update_cnt_needle():
    cnt = 0
    cnt = grep.update_cnt_needle('sleep', 'ee', False, cnt)
    assert cnt == 1


def test_update_cnt_needle_not_changed():
    cnt = 0
    cnt = grep.update_cnt_needle('sleep', 'ee1', False, cnt)
    assert cnt == 0


def test_update_regex_cnt_needle():
    cnt = 0
    cnt = grep.update_cnt_needle('Are you sleeping?', 'sleep?', True, cnt)
    assert cnt == 1


def test_add_cnt():
    listtest = []
    grep.add_cnt(1, sys.stdin, 1, listtest)
    assert listtest == ['1']


def test_print_res(capsys):
    grep.print_res(['We want to sleep', 'Really want to sleep', 'But we should to write tests TT'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'We want to sleep\nReally want to sleep\nBut we should to write tests TT\n'