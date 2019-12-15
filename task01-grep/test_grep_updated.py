#!/usr/bin/env python3
import re
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


def test_integrate_print_files_empty(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('mew fo?o world\nxfooyfoz\nfooo\n')
    (tmp_path / 'c.txt').write_text('\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-livx', '-E', 'fo?o', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\nc.txt\n'


def test_find_pattern_in_line_equal():
    result = grep.find_pattern_in_line(re.compile('needle?'), 'pref needle?', True)
    assert not result


def test_find_pattern_in_line_not_equal():
    result = grep.find_pattern_in_line(re.compile('needle?'), 'pref needle?', False)
    assert result


def test_format_output():
    result = grep.format_data(True, 'aaa')
    assert result == 'aaa:{}'


def test_print_result_at_least_one_found(capsys):
    grep.print_result('{}', 'a.txt', ['1x\n', '1y\n'], True, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_print_result_no_one_found(capsys):
    grep.print_result('{}', 'a.txt', ['1x\n', '1y\n'], False, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_print_result_standard(capsys):
    grep.print_result('{}', 'a.txt', ['1x\n', '1y\n'], False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1x\n\n1y\n\n'


def test_find_pattern_count_regex():
    result = grep.find_pattern(True, ['a', 'b', 'ac'], re.compile('[a-z]'), False, False)
    assert result == ['3']


def test_find_pattern_count_invert():
    result = grep.find_pattern(True, ['a', 'b', 'ac'], re.compile('[a-z]'), False, True)
    assert result == ['0']


def test_find_pattern_count_fullmatch_invert():
    result = grep.find_pattern(True, ['a', 'b', 'ac'], re.compile('[a-z]'), True, True)
    assert result == ['1']


def test_find_pattern_fullmatch_invert():
    result = grep.find_pattern(False, ['a', 'b', 'ac'], re.compile('[a-z]'), True, True)
    assert result == ['ac']


def test_find_pattern_fullmatch():
    result = grep.find_pattern(False, ['a', 'b', 'ac'], re.compile('[a-z]'), True, False)
    assert result == ['a', 'b']


def test_find_pattern():
    result = grep.find_pattern(False, ['a', 'b', 'ac'], re.compile('[a-z]'), False, False)
    assert result == ['a', 'b', 'ac']
