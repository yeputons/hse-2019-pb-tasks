#!/usr/bin/env python3
import re
import grep
from grep import find_pattern
from grep import filter_lines
from grep import format_output
from grep import print_with_flags
from grep import compile_pattern


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


def test_filter_lines_not_regex_ignore():
    lines = ['Jingle', 'Bells', 'jungle', 'JUNGLE']
    pattern = re.compile(re.escape('ju'), flags=re.IGNORECASE)
    assert filter_lines(lines, pattern, 0, 0) == ['jungle', 'JUNGLE']


def test_filter_lines_not_regex_invert():
    lines = ['Jingle', 'Bells', 'jungle', 'juNGLE']
    pattern = re.compile(re.escape('ju'))
    assert filter_lines(lines, pattern, 1, 0) == ['Jingle', 'Bells']


def test_filter_lines_not_regex_full():
    lines = ['Jingle', 'Bells', 'jungle', 'juNGLE']
    pattern = re.compile(re.escape('jungle'))
    assert filter_lines(lines, pattern, 0, 1) == ['jungle']


def test_not_full_find_pattern():
    line = 'Yes, of course'
    pattern = re.compile(re.escape('Yes'))
    assert find_pattern(pattern, line, False)


def test_full_find_pattern():
    line = 'Yes, of course'
    pattern = re.compile(re.escape('Yes'))
    assert not find_pattern(pattern, line, True)


def test_format_output_not_many():
    assert format_output('a.txt', 'Yes', False) == 'Yes'


def test_format_output_is_many():
    assert format_output('a.txt', str(3), True) == 'a.txt:3'


def test_print_with_flags_counter(capsys):
    print_with_flags('a.txt', 2, True, True, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\n'


def test_print_with_flags_found(capsys):
    print_with_flags('a.txt', 2, False, True, True, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_print_with_flags_not_found(capsys):
    print_with_flags('a.txt', 0, False, True, False, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_not_print_with_flags_not_found(capsys):
    print_with_flags('a.txt', 2, False, True, False, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_compile_pattern_without_flags():
    assert compile_pattern('Yes)', False, False) == re.compile('Yes\\)')


def test_compile_pattern_ignore():
    assert compile_pattern('AoAo', True, False) == re.compile('AoAo', re.IGNORECASE)


def test_compile_pattern_regex():
    assert compile_pattern(r'J\d?', False, True) == re.compile(r'J\d?')


def test_compile_pattern_regex_and_ignore():
    assert compile_pattern(r'o\d?', True, True) == re.compile(r'o\d?', re.IGNORECASE)
