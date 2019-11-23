#!/usr/bin/env python3
from argparse import Namespace
import grep


def test_unit_find_in_str():
    assert grep.find_in_str('str', 'preFStR', ['ignore_case'])
    assert grep.find_in_str('str', 'STRsUf', ['ignore_case'])
    assert grep.find_in_str('str', 'STR', ['ignore_case', 'full_match'])
    assert not grep.find_in_str('str', 'stRd', ['ignore_case', 'full_match'])
    assert not grep.find_in_str('str', 'ctr', ['ignore_case'])
    assert not grep.find_in_str('str', 'sTk', ['ignore_case'])

    assert grep.find_in_str('str', 'STR', ['regex', 'ignore_case', 'full_match'])
    assert grep.find_in_str('a?', 'A', ['regex', 'ignore_case', 'full_match'])
    assert grep.find_in_str('aB.*ef', 'AbCdeF', ['regex', 'ignore_case'])
    assert not grep.find_in_str('aBa+', 'abcBAA', ['regex', 'ignore_case'])
    assert not grep.find_in_str('aBa+', 'aaba+', ['regex', 'ignore_case', 'full_match'])


def test_unit_get_matching_args():
    assert grep.get_matching_args(Namespace(ignore_case=True)) == ['ignore_case']
    assert grep.get_matching_args(Namespace(full_match=True)) == ['full_match']


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
