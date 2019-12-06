#!/usr/bin/env python3
from typing import List
import grep


def test_integrate_all_keys_print_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-livx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_integrate_all_keys_print_not_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-Livx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_integrate_all_keys_count_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-civx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:3\na.txt:0\n'


def test_exist_in_line_i_str():
    assert grep.exists_in_line('hi', 'hey HI world', False, True, False)


def test_exist_in_line_i_regex():
    assert grep.exists_in_line('h?T', 'T', True, True, False)


def test_exist_in_line_regex_x():
    assert grep.exists_in_line('h?t', 't', True, False, True)


def test_exist_in_line_str_x():
    assert not grep.exists_in_line('hello', 'hello s', False, False, True)


def test_search_in_lines_v():
    assert grep.search_in_lines(['Line 1', 'Line 2'], False, 'Line 1',
                                False, True, False) == ['Line 2']


def test_print_results_l(capsys):
    lines: List[str] = ['Line 1']
    grep.print_results('a.txt', False, lines, True, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_print_results_big_l(capsys):
    lines: List[str] = []
    grep.print_results('a.txt', False, lines, False, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'
