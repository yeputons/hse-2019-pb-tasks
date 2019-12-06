#!/usr/bin/env python3
from typing import List
import io
import grep


# def test_integrate_stdin_grep(monkeypatch, capsys):
#     monkeypatch.setattr('sys.stdin', io.StringIO(
#         'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
#     grep.main(['needle?'])
#     out, err = capsys.readouterr()
#     assert err == ''
#     assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'
#
#
# def test_integrate_stdin_regex_grep(monkeypatch, capsys):
#     monkeypatch.setattr('sys.stdin', io.StringIO(
#         'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
#     grep.main(['-E', 'needle?'])
#     out, err = capsys.readouterr()
#     assert err == ''
#     assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'
#
#
# def test_integrate_stdin_grep_count(monkeypatch, capsys):
#     monkeypatch.setattr('sys.stdin', io.StringIO(
#         'pref needle\nneedle suf\nthe needl\npref needle suf'))
#     grep.main(['-c', 'needle'])
#     out, err = capsys.readouterr()
#     assert err == ''
#     assert out == '3\n'
#
#
# def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
#     (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
#     monkeypatch.chdir(tmp_path)
#     grep.main(['needle', 'a.txt'])
#     out, err = capsys.readouterr()
#     assert err == ''
#     assert out == 'pref needle suf\n'
#
#
# def test_integrate_files_grep(tmp_path, monkeypatch, capsys):
#     (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
#     (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
#     monkeypatch.chdir(tmp_path)
#     grep.main(['needle', 'b.txt', 'a.txt'])
#     out, err = capsys.readouterr()
#     assert err == ''
#     assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'
#
#
# def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
#     (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
#     (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
#     monkeypatch.chdir(tmp_path)
#     grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
#     out, err = capsys.readouterr()
#     assert err == ''
#     assert out == 'b.txt:1\na.txt:2\n'
#
#
# def test_integrate_file_grep_regex(tmp_path, monkeypatch, capsys):
#     (tmp_path / 'a.txt').write_text('ahhe\nhhhline\n')
#     monkeypatch.chdir(tmp_path)
#     grep.main(['-E', 'h+?', 'a.txt'])
#     out, err = capsys.readouterr()
#     assert err == ''
#     assert out == 'ahhe\nhhhline\n'
#
#
# def test_integrate_files_grep_regex(tmp_path, monkeypatch, capsys):
#     (tmp_path / 'a.txt').write_text('Higher school of\nkekonomics\n')
#     (tmp_path / 'b.txt').write_text('Love\nthis one\n')
#     monkeypatch.chdir(tmp_path)
#     grep.main(['-E', 'o+', 'a.txt', 'b.txt'])
#     out, err = capsys.readouterr()
#     assert err == ''
#     assert out == 'a.txt:Higher school of\na.txt:kekonomics\nb.txt:Love\nb.txt:this one\n'
#
#
# def test_integrate_files_grep_regex_count(tmp_path, monkeypatch, capsys):
#     (tmp_path / 'a.txt').write_text('Some prefix 00\n')
#     (tmp_path / 'b.txt').write_text('Another\nneedle\n')
#     monkeypatch.chdir(tmp_path)
#     grep.main(['-c', '-E', 'o+', 'a.txt', 'b.txt'])
#     out, err = capsys.readouterr()
#     assert err == ''
#     assert out == 'a.txt:1\nb.txt:1\n'


def test_exists_in_line_empty():
    assert not grep.exists_in_line('some text', '', False, False, False)


def test_exists_in_line_regex():
    assert grep.exists_in_line('.o+', 'file.o', True, False, False)
    assert not grep.exists_in_line('.exe+', 'a.bin', True, False, False)


def test_search_in_lines_func():
    lines: List[str] = ['Line 1', 'Line 2', 'Line 3']
    assert grep.search_in_lines(lines, False, '2', False, False, False) == ['Line 2']


def test_search_in_lines_regex():
    lines: List[str] = ['Line 1', 'Line 2', 'Line 3']
    assert grep.search_in_lines(lines, True, 'i+n', False,
                                False, False) == ['Line 1', 'Line 2', 'Line 3']


def test_search_in_lines_empty():
    lines: List[str] = []
    assert grep.search_in_lines(lines, False, 'pattern', False, False, False) == []


def test_print_line_func_prefix_empty(capsys):
    grep.print_line('0', '')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '0\n'


def test_print_line_func(capsys):
    grep.print_line('Some line', 'a.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txtSome line\n'


def test_print_result_function(capsys):
    lines: List[str] = ['Line 1']
    grep.print_results('a.txt', False, lines, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txtLine 1\n'


def test_print_result_function_empty(capsys):
    lines: List[str] = []
    grep.print_results('', True, lines, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '0\n'


def test_print_result_function_count(capsys):
    lines: List[str] = ['line 1', 'line 2']
    grep.print_results('', True, lines, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_print_result_function_count_len(capsys):
    lines: List[str] = ['line 1', 'line 2']
    grep.print_results('a.txt:', True, lines, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\n'


def test_file_search_no_file(capsys):
    grep.find_pattern(['a.txt'], False, True, 'h+?', False, False, False, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Can not open a file:a.txt. Error has occurred\n'


def test_files_search(tmp_path, monkeypatch, capsys):
    (tmp_path / 'b.txt').write_text('Some stuff\n')
    monkeypatch.chdir(tmp_path)
    grep.find_pattern(['b.txt'], False, False, 'stuff', False, False, False, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Some stuff\n'


def test_console_search_empty(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(''))
    out, err = capsys.readouterr()
    grep.find_pattern([], False, False, 'str', False, False, False, False, False)
    assert err == ''
    assert out == ''
