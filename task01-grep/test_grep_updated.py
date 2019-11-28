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


def test_re_search_modifier():
    line = 'ahhhe'
    needle = 'h*i?'
    assert grep.re_search_modifier(line, needle, False, False, False)
    assert not grep.re_search_modifier(line, needle, True, False, False)
    assert grep.re_search_modifier(line, needle, True, False, True)
    line = 'hey HI world'
    needle = 'hi'
    assert grep.re_search_modifier(line, needle, False, True, False)
    line = 'HeI'
    assert not grep.re_search_modifier(line, needle, False, True, False)


def test_substring_search_modifier():
    line = 'ahhhe'
    needle = 'hH?'
    assert not grep.substring_search_modifier(line, needle, False, True, False)
    assert grep.substring_search_modifier(line, needle, False, True, True)
    needle = 'ahhhe'
    assert grep.substring_search_modifier(line, needle, True, False, False)
    line = 'hey HI world'
    needle = 'hi'
    assert not grep.substring_search_modifier(line, needle, False, True, True)
