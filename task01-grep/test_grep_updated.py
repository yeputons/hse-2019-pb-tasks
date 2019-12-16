#!/usr/bin/env python3
import grep


def test_unit_inverse():
    ir_matcher = grep.select_matcher(False, False, False, True)
    assert ir_matcher('abc', 'd')
    assert not ir_matcher('abc', 'a')
    assert not ir_matcher('abc', 'ab')
    assert ir_matcher('', 'd')
    assert not ir_matcher('a', 'a')
    assert ir_matcher('abc', 'abc ')
    assert ir_matcher('123', 'ab')
    assert not ir_matcher('', '')


def test_unit_full_match():
    fm_matcher = grep.select_matcher(False, False, True, False)
    assert fm_matcher('abc', 'abc')
    assert fm_matcher('', '')
    assert not fm_matcher('aaaa', 'aaba')


def test_integrate_regex_full_match():
    matcher = grep.select_matcher(True, False, True, False)
    assert matcher('hello', 'hel*o')
    assert matcher('aaabbb', 'a*b*')
    assert not matcher('aaabbb', 'a*b*c')
    assert matcher('aaabbbCCCCC', 'a*b*C*')


def test_integrate_regex_ignore_case():
    matcher = grep.select_matcher(True, True, False, False)
    assert matcher('heLlo', 'Hel*o')
    assert matcher('helloaaaBbbdddd', 'a*b*')
    assert not matcher('AaAbBb', 'a*b*C')
    assert matcher('aaaAbbbCCCCCcccc', 'a*b*C*')


def test_integrate_regex_full_match_ignore_case():
    matcher = grep.select_matcher(True, True, True, False)
    assert matcher('AaabbB', 'a*B*c*')
    assert matcher('a', 'A')
    assert not matcher('ab', 'A')
    assert not matcher('AbbAbAbbbacc', 'Abb*a*B')
    assert matcher('AABB', 'a*b*c*')


def test_unit_print_filenames(capsys):
    printer = grep.select_printer(True, False, False, False)
    printer('a.txt', ['hell', 'w'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'
    printer('a.txt', [])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_unit_print_filenames_without(capsys):
    printer = grep.select_printer(False, True, False, False)
    printer('a.txt', ['hell', 'w'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    printer('a.txt', [])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


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
