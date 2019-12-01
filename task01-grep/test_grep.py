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


# MINE


def test_print_data_one_file(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    grep.print_data('pref needle suf', 'no_name', False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_print_data_no_files(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    grep.print_data('I think this test is useless', 'no_name', False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'I think this test is useless\n'


def test_print_data_various_files(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    grep.print_data('just like my life)))', 'a.txt', True, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:just like my life)))\n'


def test_print_data_count(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    grep.print_data('24', 'no_name', False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '24\n'


def test_print_data_various_files_count(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    grep.print_data('24', 'a.txt', True, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:24\n'


def test_matching_pattern_true_0():
    assert grep.matching_pattern(True, False, False, 'v', 'hhh valgrind vbvb') is True


def test_matching_pattern_true_1():
    assert grep.matching_pattern(True, False, False, 'hhh val vbv?', 'hhh val vbvb') is True


def test_matching_pattern_true_2():
    assert grep.matching_pattern(False, False, False, 'v', 'hhh valgrind vbvb') is True


def test_matching_pattern_false_0():
    assert grep.matching_pattern(True, False, False, 'valgrind * m', 'hhhh valgrind vbvb') is False


def test_matching_pattern_false_1():
    assert grep.matching_pattern(False, False, False, 'm', 'hhh valgrind vbvb') is False


def test_process_one_file_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    with open('a.txt') as new:
        grep.process(new, 'a.txt', False, 'needle', False, True, False, False, False, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_process_various_files_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    with open('a.txt') as new:
        grep.process(new, 'b.txt', True, 'needle', False, True, False, False, False, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:2\n'


def test_process_various_files_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needles\n afhfk suf\nneedle needle bbb\n')
    (tmp_path / 'b.txt').write_text('the needling\npref needle suf')
    monkeypatch.chdir(tmp_path)
    with open('a.txt') as new:
        grep.process(new, 'a.txt', True, 'needle', True, False, False, False, False, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:pref needles\na.txt:needle needle bbb\n'


def test_process_one_file_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needles\n afhfk suf\nneedle needle aaa\n')
    monkeypatch.chdir(tmp_path)
    with open('a.txt') as new:
        grep.process(new, 'a.txt', False, 'needle', True, False, False, False, False, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needles\nneedle needle aaa\n'


def test_process_no_files_regex(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'needles kjkj need g\nnedned ghjf\nneedle aaa\n'))
    grep.process(sys.stdin, ' ', False, 'needle', True, False, False, False, False, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'needles kjkj need g\nneedle aaa\n'
