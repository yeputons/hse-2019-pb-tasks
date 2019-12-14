#!/usr/bin/env python3
from typing import List
import argparse as ap
import re
import grep


def test_parse_args():
    args_str: List[str] = ['-c', '-Evx', 'needle', 'a.txt']
    args: ap.Namespace = grep.parse_args(args_str)
    assert args.counting_mode
    assert args.regex
    assert args.inverse
    assert args.full_match
    assert not args.ignore
    assert not args.with_files
    assert not args.with_files_invert
    assert args.pattern == 'needle'
    assert args.files == ['a.txt']


def test_compile_pattern_regex():
    assert grep.compile_pattern('a+f?', is_regex=True,
                                is_ignore=False) == re.compile('a+f?')


def test_compile_pattern_no_regex():
    assert grep.compile_pattern('a+f?', is_regex=False,
                                is_ignore=False) == re.compile('a\\+f\\?')


def test_compile_pattern_is_ignore():
    assert grep.compile_pattern('a+f?', is_regex=False,
                                is_ignore=True) == re.compile('a\\+f\\?', re.IGNORECASE)


def test_is_matching_regex():
    assert grep.is_matching('affc', re.compile('a+f?'),
                            inverse=False, full_match=False)


def test_is_matching_inverse():
    assert grep.is_matching('affc', re.compile(re.escape('a+f?')),
                            inverse=True, full_match=False)


def test_is_matching_full_match():
    assert not grep.is_matching('affc', re.compile(re.escape('ff')),
                                inverse=False, full_match=True)


def test_filter_matching_lines_inverse():
    test = ['PMI', 'a+f?', 'HSE', 'AU']
    assert grep.filter_matching_lines(test, re.compile(re.escape('a+f?')),
                                      inverse=True, full_match=False) == ['PMI', 'HSE', 'AU']


def test_format_output_no_is_lines_no_is_no_lines():
    assert grep.format_output(['q'], counting_mode=False, with_files=False,
                              with_files_invert=False, source='a.txt') == ['a.txt:q']


def test_format_output_is_lines_no_is_no_lines():
    assert grep.format_output(['q'], counting_mode=False, with_files=True,
                              with_files_invert=False, source='a.txt') == ['a.txt']


def test_format_output_is_lines_is_no_lines():
    assert grep.format_output(['q'], counting_mode=False, with_files=True,
                              with_files_invert=True, source='a.txt') == []


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
