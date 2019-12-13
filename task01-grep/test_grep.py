#!/usr/bin/env python3
from typing import Dict
import io
import grep


def test_unit_read_files(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('pyt\npyt\n')
    (tmp_path / 'b.txt').write_text('pytpytpyt')
    (tmp_path / 'c.txt').write_text('pyt pyt pyt\n pyt')
    monkeypatch.chdir(tmp_path)
    saved_lines = [['a.txt', 'pyt'],
                   ['a.txt', 'pyt'],
                   ['b.txt', 'pytpytpyt'],
                   ['c.txt', 'pyt pyt pyt'],
                   ['c.txt', ' pyt']]
    assert grep.read_files(['a.txt', 'b.txt', 'c.txt']) == saved_lines


def test_unit_read_stdin(monkeypatch):
    monkeypatch.setattr('sys.stdin', io.StringIO('pyt\n pyt pyt \n \n pyt\n'))
    assert grep.read_stdin() == [['', 'pyt'], ['', ' pyt pyt '], ['', ' '], ['', ' pyt']]


def test_unit_search():
    search_flags: Dict[str, bool] = {'ignore_case': False, 'invert_ans': False,
                                     'full_match': False, 'regex': False}
    assert grep.search('pyt', 'ptpyppytyp', search_flags)
    assert not grep.search('pyt', 'ptpypptyp', search_flags)
    assert grep.search('pyt', 'ptp!65/,`dsv>04pyt/-fjsw', search_flags)
    assert not grep.search('pyt', '', search_flags)

    search_flags['regex'] = True
    assert grep.search('[p,a]yt+', 'ayttt', search_flags)
    assert grep.search('(p{1,3}[Y,t,s][5-7])z+', 'pY6z', search_flags)
    assert grep.search('(p{1,3}[Y,t,s][5-7])z+', 'ppt5zzzz', search_flags)
    assert not grep.search('(p{1,3}[Y,t,s][5-7])z+', 'pppptt7zz', search_flags)
    assert not grep.search('(p{1,3}[Y,t,s][5-7])z+', '(p{1,3}[Y,t,s][5-7])z+', search_flags)
    assert not grep.search('(p{1,3}[Y,t,s][5-7])z+', '', search_flags)


def test_unit_search_in_lines():
    search_flags: Dict[str, bool] = {'ignore_case': False, 'invert_ans': False,
                                     'full_match': False, 'regex': False}
    input_lines = [['a', 'ptpyppytyp'],
                   ['a', 'ptpypptyp'],
                   ['a', 'pyt'],
                   ['', 'pt`dsv>04pyt/-f'],
                   ['d', ' ']]
    answer = {'a': ['ptpyppytyp', 'pyt'], '': ['pt`dsv>04pyt/-f'], 'd': []}
    assert grep.search_in_lines('pyt', input_lines, search_flags) == answer

    search_flags['regex'] = True
    input_lines = [['a', 'pY6z'],
                   ['a', 'ptpypptyp'],
                   ['c', 'ppt5zzzz'],
                   ['d', '(p{1,3}[Y,t,s][5-7])z+']]
    answer = {'a': ['pY6z'], 'c': ['ppt5zzzz'], 'd': []}
    assert grep.search_in_lines('(p{1,3}[Y,t,s][5-7])z+', input_lines, search_flags) == answer


def test_unit_print_ans_lines(capsys):
    grep.print_ans_lines({'a': ['ptpyppytyp', 'pyt', 'pt`dsv>04pyt/-f']}, '{1}')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'ptpyppytyp\npyt\npt`dsv>04pyt/-f\n'

    grep.print_ans_lines({'a.txt': ['ptpyppytyp', 'pyt'],
                          'b.txt': ['pt`dsv>04pyt/-f'], 'c.txt': []}, '{0}:{1}')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:ptpyppytyp\na.txt:pyt\nb.txt:pt`dsv>04pyt/-f\n'


def test_unit_print_ans_count(capsys):
    grep.print_ans_count({'': ['ptpyppytyp', 'pyt', 'pt`dsv>04pyt/-f']}, '{1}')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'

    grep.print_ans_count({'a.txt': ['ptpyppytyp', 'pyt'],
                          'b.txt': ['pt`dsv>04pyt/-f'], 'c.txt': []}, '{0}:{1}')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\nb.txt:1\nc.txt:0\n'


def test_integrate_stdin_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_integrate_stdin_regex_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_integrate_stdin_grep_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_integrate_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_integrate_files_regex_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\nnot needL')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle?', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:the needl\na.txt:pref needle\na.txt:needle suf\n'


def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'
