#!/usr/bin/env python3
"""plug"""
from typing import Pattern
import io
import re

import grep


def test_integrate_stdin_grep(monkeypatch, capsys):
    """plug"""
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_integrate_stdin_regex_grep(monkeypatch, capsys):
    """plug"""
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_integrate_stdin_grep_count(monkeypatch, capsys):
    """plug"""
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_stdin_grep_regex_count(monkeypatch, capsys):
    """plug"""
    monkeypatch.setattr('sys.stdin', io.StringIO(
        '112\nWWW\nSU35\nF'))
    grep.main(['-c', '-E', '[0-9]'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    """plug"""
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_integrate_files_grep(tmp_path, monkeypatch, capsys):
    """plug"""
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    """plug"""
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_integrate_file_grep_count(tmp_path, monkeypatch, capsys):
    """plug"""
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_files_regex_grep(tmp_path, monkeypatch, capsys):
    """plug"""
    (tmp_path / 'a.txt').write_text('112\nmiu\n')
    (tmp_path / 'b.txt').write_text('one-two-three\n123')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '[0-9]', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:123\na.txt:112\n'


def test_integrate_file_regex_grep(tmp_path, monkeypatch, capsys):
    """plug"""
    (tmp_path / 'a.txt').write_text('wronganswer4\njunkz\npython')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '[0-9]', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'wronganswer4\n'


def test_integrate_file_count_regex_grep(tmp_path, monkeypatch, capsys):
    """plug"""
    (tmp_path / 'a.txt').write_text('wronganswer4\njunkz\npython')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', '[0-9]', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_integrate_files_count_regex_grep(tmp_path, monkeypatch, capsys):
    """plug"""
    (tmp_path / 'a.txt').write_text('wronganswer4\njunkz\npython')
    (tmp_path / 'b.txt').write_text('LeBron\nJames\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', '[0-9]', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:1\nb.txt:0\n'


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


def test_init_arguments():
    """plug"""
    args = grep.init_arguments(['task', 'input.txt', '-E', '-c'])
    assert args.pattern == 'task'
    assert args.files == ['input.txt']
    assert args.regex
    assert args.count


def test_create_regex_e_i():
    """plug"""
    test_string = '.'
    is_regular = True
    is_ignore = True
    result_string = grep.create_regex(test_string, is_regular, is_ignore)
    assert result_string == re.compile('.', re.IGNORECASE)


def test_create_regex_e():
    """plug"""
    test_string = '[0-9]\\d'
    is_regular = True
    is_ignore = False
    result_string = grep.create_regex(test_string, is_regular, is_ignore)
    assert result_string == re.compile('[0-9]\\d')


def test_create_regex_i():
    """plug"""
    test_string = 'master'
    is_regular = False
    is_ignore = True
    result_string = grep.create_regex(test_string, is_regular, is_ignore)
    assert result_string == re.compile('master', re.IGNORECASE)


def test_create_regex():
    """plug"""
    test_string = 'master'
    is_regular = False
    is_ignore = False
    result_string = grep.create_regex(test_string, is_regular, is_ignore)
    assert result_string == re.compile('master')


def test_strip_lines():
    """plug"""
    list_ = ['plov\n', 'lavash\n', 'pomidor\n']
    result_list = grep.strip_lines(list_)
    assert result_list == ['plov', 'lavash', 'pomidor']


def test_create_list_filenames():
    file_names = ['a.txt', 'b.txt', 'c.txt']
    result = grep.create_list_stream_names(file_names)
    assert result == file_names


def test_create_all_lines(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('mem\nory\n')
    (tmp_path / 'b.txt').write_text('lim\nit\n')
    monkeypatch.chdir(tmp_path)
    read = grep.create_lines_of_lines(['a.txt', 'b.txt'])
    assert read == [['mem\n', 'ory\n'],
                    ['lim\n', 'it\n']]


def test_bool_match_with_flag_match():
    is_match = True
    is_invert = True
    line = 'kek'
    pattern = re.compile('kek')
    assert not grep.bool_match(line, pattern, is_invert, is_match)


def test_bool_match_without_flag_match():
    is_match = False
    is_invert = True
    line = 'kekek'
    pattern = re.compile('kek')
    assert not grep.bool_match(line, pattern, is_invert, is_match)


def test_bool_match_without_flag_invert():
    is_match = False
    is_invert = False
    line = 'kekek'
    pattern = re.compile('kek')
    assert grep.bool_match(line, pattern, is_invert, is_match)


def test_processing_result_lines():
    pattern = re.compile('alg')
    lines = ['algebra', 'minecraft', 'dota']
    is_match = False
    is_invert = True
    assert grep.processing_result_lines(lines, pattern, is_invert, is_match) == ['minecraft', 'dota']


def test_process_result_lines_more_interesting():
    lines = ['kEk', 'sdKEK', 'miu']
    is_invert = True
    is_match = True
    assert grep.processing_result_lines(lines, re.compile('kek', flags=re.I), is_invert, is_match) == ['sdKEK',
                                                                                                       'miu']


def test_process_file_with_str_not_empty_lines():
    lines = ['a', 'b', 'c']
    file_name = 'a.txt'
    assert grep.process_file_with_str(lines, file_name) == ['a.txt']


def test_process_file_with_str_empty_lines():
    lines = []
    file_name = 'a.txt'
    assert grep.process_file_with_str(lines, file_name) == []


def test_process_file_without_str_empty_lines():
    lines = []
    file_name = 'a.txt'
    assert grep.process_file_without_str(lines, file_name) == ['a.txt']


def test_process_file_without_str_not_empty_lines():
    lines = ['a', 'b', 'c']
    file_name = 'a.txt'
    assert grep.process_file_without_str(lines, file_name) == []


def test_process_count_std_input_or_one_file():
    lines = ['a', 'b', 'c']
    stream_name = 'None'
    assert grep.process_count(lines, stream_name) == ['3']


def test_process_count_many_file_input():
    lines = ['a', 'b', 'c']
    stream_name = 'a.txt'
    assert grep.process_count(lines, stream_name) == ['a.txt:3']


def test_process_no_flags_stdin_or_one_file():
    lines = ['a', 'b', 'c']
    stream_name = 'None'
    assert grep.process_no_flags(lines, stream_name) == ['a', 'b', 'c']


def test_process_no_flags_many_input_files():
    lines = ['a', 'b', 'c']
    file_name = 'a.txt'
    assert grep.process_no_flags(lines, file_name) == ['a.txt:a', 'a.txt:b', 'a.txt:c']


def test_process_underprint_results_random_flag():
    lines = ['a', 'ab', 'ac', 'bc', 'abc']
    stream_name = 'file.txt'
    is_file_with_str = True
    is_file_without_str = False
    is_count = False
    assert grep.processing_underprint_results(lines, stream_name, is_count,
                                              is_file_with_str, is_file_without_str) == ['file.txt']


def test_print_grep_results(capsys):
    """plug"""
    ans_list = ['a', 'ab', 'abc', 'abcd', 'abcde']
    grep.print_grep_results(ans_list)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a\nab\nabc\nabcd\nabcde\n'
