#!/usr/bin/env python3
import grep


def test_filter_lines_with_ignorecase():
    assert grep.filter_lines(['Anna', 'anna', 'aNNA', 'annikura'], 'Anna', is_ignorecase=True) ==\
           ['Anna', 'anna', 'aNNA']


def test_filter_lines_with_fullmatch():
    assert grep.filter_lines(['Misha', 'misha', 'mISHA', 'Hey'], 'Misha', is_fullmatch=True) ==\
           ['Misha']


def test_exec_grep_with_invert():
    assert grep.exec_grep(['abbbb', 'file', 'main.cpp', 'main.cpp'], 'main.cpp', is_invert=True) ==\
           ['abbbb', 'file']


def check_output(capsys, expected_output):
    out, err = capsys.readouterr()
    assert err == ''
    assert out == expected_output


def test_integrate_all_keys_print_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-livx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    check_output(capsys, 'b.txt\n')


def test_integrate_all_keys_print_not_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-Livx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    check_output(capsys, 'a.txt\n')


def test_integrate_all_keys_count_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-civx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    check_output(capsys, 'b.txt:3\na.txt:0\n')
