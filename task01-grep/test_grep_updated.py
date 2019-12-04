#!/usr/bin/env python3
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


def test_integrate_Ecvx_keys(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-Ecvx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:3\na.txt:3\n'


def test_integrate_ivLx_keys(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-ivLx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_print_result_with_filename(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    grep.print_result(['a.txt:1', 'b.txt:2'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:1\nb.txt:2\n'


def test_print_result_without_filename(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    grep.print_result(['1'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_format_lines_without_is_has_lines_without_is_no_lines():
    assert grep.format_lines('a', 'a.txt', is_has_lines=False, is_no_lines=False) == 'a.txt:a'


def test_format_lines_with_is_has_lines_without_is_no_lines():
    assert grep.format_lines('2', 'a.txt', is_has_lines=True, is_no_lines=False) == 'a.txt'


def test_format_lines_with_is_has_lines_with_is_no_lines():
    assert grep.format_lines('22', 'a.txt', is_has_lines=True, is_no_lines=True) == 'a.txt'


def test_format_lines_without_is_has_lines_with_is_no_lines():
    assert not grep.format_lines('1', 'a.txt', is_has_lines=False, is_no_lines=True)


def test_match_pattern_with_is_regex_is_ignore_is_full_match():
    assert not grep.match_pattern('ab', 'ABC', is_regex=True, is_ignore=True, is_full_match=True)


def test_match_pattern_with_is_regex_is_ignore_without_is_full_match():
    assert grep.match_pattern('a*', 'ABC', is_regex=True, is_ignore=True, is_full_match=False)


def test_match_pattern__with_is_regex_without_is_ignore_without_is_full_match():
    assert grep.match_pattern('b', 'AbC', is_regex=True, is_ignore=False, is_full_match=False)


def test_match_pattern_without_is_regex_is_ignore_without_is_full_match():
    assert grep.match_pattern('A', 'ABC', is_regex=False, is_ignore=False, is_full_match=False)


def test_match_pattern_with_is_regex_without_is_ignore_with_is_full_match():
    assert not grep.match_pattern('a*c', 'ABC', is_regex=True, is_ignore=False, is_full_match=True)


def test_match_pattern_without_is_regex_with_is_ignore_with_is_full_match():
    assert grep.match_pattern('abcd', 'ABCD', is_regex=False, is_ignore=True, is_full_match=True)


def test_match_pattern_without_is_regex_with_is_ignore_without_is_full_match():
    assert grep.match_pattern('aB', 'ABC', is_regex=False, is_ignore=True, is_full_match=False)


def test_match_pattern_without_is_regex_without_is_ignore_with_is_full_match():
    assert not grep.match_pattern('d', 'ABC', is_regex=False, is_ignore=False, is_full_match=True)
