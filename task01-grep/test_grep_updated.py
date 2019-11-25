#!/usr/bin/env python3

import io
import grep


def test_get_value():
    assert not grep.get_value({'aa': False}, 'aa')
    assert grep.get_value({'aa': True}, 'aa')
    assert not grep.get_value({'bb': True}, 'aa')
    assert not grep.get_value({'bb': False}, 'aa')


def test_match_ignore_case():
    assert grep.match('AAb', 'AAbtrg', {grep.IGNORE_CASE: True})
    assert grep.match('Aab', 'aABte', {grep.IGNORE_CASE: True})
    assert not grep.match('Aab', 'aAb', {grep.IGNORE_CASE: False})
    assert grep.match('', '', {})
    assert grep.match('aaa', 'AaA', {grep.REGEX: True, grep.IGNORE_CASE: True})
    assert grep.match('aa?a', 'AA', {grep.REGEX: True, grep.IGNORE_CASE: True})
    assert not grep.match(
        'ab?a', 'aBba', {grep.REGEX: True, grep.IGNORE_CASE: True})


def test_search_needle_in_src_inverted():
    needle = 'abab'
    src = []
    assert grep.search_needle_in_src(
        needle, src, {grep.REGEX: False, grep.INVERTED: True}) == []
    src = ['qababr', 'qadbab', 'quabab']
    assert grep.search_needle_in_src(
        needle, src, {grep.REGEX: False, grep.INVERTED: True}) == ['qadbab']
    needle = '[1]'
    src = ['[2 ghs', ']] req', '[1e]', 'pp[1]asf']
    assert grep.search_needle_in_src(
        needle, src, {grep.REGEX: False, grep.INVERTED: False}) == ['pp[1]asf']
    needle = 'a'
    src = ['rtt', 'pq', 'cnb']
    assert grep.search_needle_in_src(
        needle, src, {grep.REGEX: True, grep.INVERTED: True}) == src


def test_match_full_match():
    assert grep.match('AAA', 'AAA', {grep.FULL_MATCH: True})
    assert grep.match(
        'AAA', 'aaa', {grep.FULL_MATCH: True, grep.IGNORE_CASE: True})
    assert grep.match('AA?A', 'AA', {grep.FULL_MATCH: True, grep.REGEX: True})
    assert not grep.match('AAA', 'AAB', {grep.FULL_MATCH: True})
    assert not grep.match(
        'AAA', 'aaaa', {grep.FULL_MATCH: True, grep.IGNORE_CASE: True})
    assert grep.match(
        'Aa*t', 'aaaaaat', {grep.FULL_MATCH: True, grep.REGEX: True, grep.IGNORE_CASE: True})
    assert grep.match(
        'ArT', 'aRt', {grep.FULL_MATCH: True, grep.IGNORE_CASE: True})


def test_file_name_found(capsys):
    grep.print_search_result({'aa.txt': ['asf', 'af', 'qwe'], 'bb.txt': [
        'fs', 'aff', 'qr']}, {grep.FILE_NAMES_FOUND: True})
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'aa.txt\nbb.txt\n'
    grep.print_search_result({}, {grep.FILE_NAMES_FOUND: True})
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_file_name_not_found(capsys):
    grep.print_search_result({'aa.txt': [], 'bb.txt': ['afsa']},
                             {grep.FILE_NAMES_NOT_FOUND: True})
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'aa.txt\n'


def test_integrate_ignore_case_full_match_stdin(capsys, monkeypatch):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nnEEdle\nthe needl\npref needl suf'))
    grep.main(['-c', '-x', '-i', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_integrate_inverted_only_files(tmp_path, capsys, monkeypatch):
    (tmp_path/'a.txt').write_text('abgf?e\nioqs\nklo*a\n')
    (tmp_path/'b.txt').write_text('gf?etr\nths\nro?a\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-lvE', 'oq?s', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nb.txt\n'


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
    (tmp_path / 'b.txt').write_text(
        'hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(
        ['-Livx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_integrate_all_keys_count_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text(
        'fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text(
        'hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(
        tmp_path)
    grep.main(
        ['-civx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:3\na.txt:0\n'
