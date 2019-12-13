#!/usr/bin/env python3
import io
import grep
from grep import has_needle
from grep import find_in_file
from grep import print_res
from grep import parse_arguments
from grep import is_found
from grep import read_input


# test integrate

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


def test_integrate_stdin_all_keys_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO('fo\nFOO\nhEllo fo?o world\nxfOOyfoz\nfooo\n'))
    grep.main(['-ivx', '-E', 'fo?o'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'hEllo fo?o world\nxfOOyfoz\nfooo\n'


def test_integrate_stdin_all_keys_count_files_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO('hello fo?o world\nxfooyfoz\nfooo\n'))
    grep.main(['-civx', '-E', 'fo?o'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


# test unit
# test has_needle

def test_unit_has_needle_ignore():
    s = 'aBCDEf'
    needles_in = ['A', 'a', 'aBCdef', 'de', 'eF', '']
    needles_not_in = ['AC', 'fa', 'abcdf', 'ACF']
    for needle in needles_in:
        assert has_needle(s, needle, False, True, False, False)
    for needle in needles_not_in:
        assert not has_needle(s, needle, False, True, False, False)


def test_unit_has_needle_inverted():
    s = 'abcdef'
    needles_in = ['a', 'abcdef', 'ef', '']
    needles_not_in = ['ac', 'fa', 'abcdf']
    for needle in needles_in:
        assert not has_needle(s, needle, False, False, True, False)
    for needle in needles_not_in:
        assert has_needle(s, needle, False, False, True, False)


def test_unit_has_needle_full():
    strings = ['abcdef', 'dabdabda', '1 234 5,:![qw]', '', '/']
    needles_in = ['abcdef', 'dabdabda', '1 234 5,:![qw]', '', '/']
    needles_not_in = ['abcdf', 'dabdabdab', '12345,:![qw]', ' ', '']
    for i, s in enumerate(strings):
        assert has_needle(s, needles_in[i], False, False, False, True)
        assert not has_needle(s, needles_not_in[i], False, False, False, True)


def test_unit_has_needle_ignore_full():
    strings = ['abcdEf', 'dabdAbda', '1 234 5,:![qw]', '', '/']
    needles_in = ['ABCDEF', 'DaBdAbDa', '1 234 5,:![QW]', '', '/']
    needles_not_in = ['AbcdF', 'DABDABDAB', '12345,:![qw]', ' ', '']
    for i, s in enumerate(strings):
        assert has_needle(s, needles_in[i], False, True, False, True)
        assert not has_needle(s, needles_not_in[i], False, True, False, True)


def test_unit_has_needle_regex_full():
    s = 'abacaba'
    needles_in = ['abacaba', 'aba?1?2?caba', '.......', 'aba[a-z].[a-z][a-z]']
    needles_not_in = ['', 'abacaba.', '[adc]', 'abac{2}', 'a{5,}']
    for needle in needles_in:
        assert has_needle(s, needle, True, False, False, True)
    for needle in needles_not_in:
        assert not has_needle(s, needle, True, False, False, True)


def test_unit_has_needle_regex_ignore():
    s = 'aBAcaba123adACabaaaa'
    needles_in = ['[ADC]', '.', 'D?', '', 'aBaCaBa', 'ABACABA...adacaba', 'acaba{4,}']
    needles_not_in = ['e+', 'abac{2}', 'abacaba...abacabaaaa', 'a{5,}']
    for needle in needles_in:
        assert has_needle(s, needle, True, True, False, False)
    for needle in needles_not_in:
        assert not has_needle(s, needle, True, True, False, False)


def test_unit_has_needle_all_flags():
    s = 'abACaba'
    needles_in = ['abACAba', 'ABA?1?2?CABA', '.......', 'ABA[a-z].[A-Z][A-Z]']
    needles_not_in = ['', 'ABACABA.', '[adc]', 'ABAC{2}', 'a{5,}']
    for needle in needles_in:
        assert not has_needle(s, needle, True, True, True, True)
    for needle in needles_not_in:
        assert has_needle(s, needle, True, True, True, True)


# test find_in file

def test_unit_find_in_file_all_flags():
    lines = ['aOa', 'cobr', 'MaSlO', 'kavOOO', 'ms']
    needles = ['[Ao][Ao][Ao]', 'mA?sl?O?', 'c?o{1,}b?r?']
    results = [['cobr', 'MaSlO', 'kavOOO', 'ms'],
               ['aOa', 'cobr', 'kavOOO'],
               ['aOa', 'MaSlO', 'kavOOO', 'ms']]
    for i, needle in enumerate(needles):
        out = find_in_file(lines, needle, True, True, True, True)
        assert out == results[i]


# test is_found

def test_unit_is_found():
    found1 = ['a', 'b', '']
    found2 = ['']
    assert is_found(found1, False, False)
    assert is_found(found2, False, False)


def test_unit_is_found_empty():
    found = []
    assert not is_found(found, False, False)


def test_unit_is_found_count():
    found1 = ['a', ' ']
    found2 = ['']
    assert is_found(found1, True, False)
    assert is_found(found2, True, False)


def test_unit_is_found_empty_count():
    found = []
    assert is_found(found, True, False)


def test_unit_is_found_only_not_files():
    found1 = ['1', '2', '3', '44']
    found2 = ['']
    assert not is_found(found1, False, True)
    assert not is_found(found2, False, True)


def test_unit_is_found_empty_only_not_files():
    found = []
    assert is_found(found, False, True)


# test print_res

def test_unit_print_res(capsys):
    result = [('a.txt', ['1', '2']), ('b.txt', ['1 in b', '2 in b'])]
    print_res(result, False, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:1\na.txt:2\nb.txt:1 in b\nb.txt:2 in b\n'


def test_unit_print_res_count(capsys):
    result = [('a.txt', ['odin', 'dva']), ('b.txt', ['odin b', 'dva b'])]
    print_res(result, True, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\nb.txt:2\n'


def test_unit_print_res_only_files(capsys):
    result = [('a.txt', ['1']), ('b.txt', ['1b']), ('kavo.txt', ['1c', '2c'])]
    print_res(result, False, True, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nb.txt\nkavo.txt\n'


def test_unit_print_res_stdin(capsys):
    result = [('', ['1', 'dva', 'three two two,..,'])]
    print_res(result, False, False, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\ndva\nthree two two,..,\n'


# test read_input

def test_read_input_stdin(monkeypatch):
    monkeypatch.setattr('sys.stdin', io.StringIO('fo\nFOO\nhEllo fo?o world\nxfOOyfoz\nfooo\n'))
    lines, one_file = read_input([])
    assert one_file
    assert lines == [('', ['fo\n', 'FOO\n', 'hEllo fo?o world\n', 'xfOOyfoz\n', 'fooo\n'])]


def test_read_input_file(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('a1\nb2\nc3\n')
    monkeypatch.chdir(tmp_path)
    files_input = ['a.txt']
    lines, one_file = read_input(files_input)
    assert one_file
    assert lines == [('', ['a1\n', 'b2\n', 'c3\n'])]


def test_read_input_files(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    files_input = ['a.txt', 'b.txt']
    lines, one_file = read_input(files_input)
    assert not one_file
    assert lines == [('a.txt', ['fO\n', 'FO\n', 'FoO\n']),
                     ('b.txt', ['hello fo?o world\n', 'xfooyfoz\n', 'fooo\n'])]


# test parse_arguments

def test_unit_parse_arguments():
    args_str = ['-livx', '-E', 'tri?s', 'b.txt', 'a.txt']
    args = parse_arguments(args_str)
    assert not args.count
    assert args.files == ['b.txt', 'a.txt']
    assert args.full_match
    assert args.ignore_case
    assert args.inverted
    assert args.needle == 'tri?s'
    assert args.only_files
    assert not args.only_not_files
    assert args.regex
