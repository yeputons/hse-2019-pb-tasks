#!/usr/bin/env python3
from typing import List
import io
import grep


class MyStdinTest:
    def __init__(self, input_content: str, arguments: List[str], expected_output: str):
        self.input_content = input_content
        self.arguments = arguments
        self.expected_output = expected_output


def integrate_stdin_test_helper(monkeypatch, capsys, input_content: str,
                                arguments: List[str], expected_output: str):
    monkeypatch.setattr('sys.stdin', io.StringIO(input_content))
    grep.main(arguments)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == expected_output


def test_integrate_stdin_grep_basic(monkeypatch, capsys):
    tests = [
        MyStdinTest('simple test\nabac cabac cabaca\nnext line is empty\n\nend',
                    ['e'], 'simple test\nnext line is empty\nend\n'),
        MyStdinTest('no output\nexpected\n\n\nthis time\n', ['no such line'], '\n'),
        MyStdinTest('', ['empty input'], '\n'),
        MyStdinTest('same\nsame\nsame\nsame\nline', ['am'], 'same\nsame\nsame\nsame\n')
    ]
    for test in tests:
        integrate_stdin_test_helper(monkeypatch, capsys,
                                    test.input_content, test.arguments, test.expected_output)


def test_integrate_stdin_grep_regex(monkeypatch, capsys):
    tests = [
        MyStdinTest('simple test\ntabac cabac cabaca\nnext line is empty\n\nend',
                    ['-E', '\\b\\w{4}\\b'], 'simple test\nnext line is empty\n'),
        MyStdinTest('no output\nexpected\n\n\nthis time\n', ['-E', '[A-Z]+'], '\n'),
        MyStdinTest('', ['-E', '[empty input]+'], '\n'),
        MyStdinTest('sAme\nsAme\nsAme\nsAme\nline', ['-E', '[A-Z]'], 'sAme\nsAme\nsAme\nsAme\n')
    ]
    for test in tests:
        integrate_stdin_test_helper(monkeypatch, capsys,
                                    test.input_content, test.arguments, test.expected_output)


def test_integrate_stdin_grep_count(monkeypatch, capsys):
    tests = [
        MyStdinTest('simple test\ntabac cabac cabaca\nnext line is empty\n\nend',
                    ['-c', '-E', '\\b\\w{4}\\b'], '2\n'),
        MyStdinTest('no output\nexpected\n\n\nthis time\n', ['-E', '-c', '[A-Z]+'], '0\n'),
        MyStdinTest('', ['-E', '-c', '[empty input]+'], '0\n'),
        MyStdinTest('sAme\nsAme\nsAme\nsAme\nline', ['-c', '-E', '[A-Z]'], '4\n')
    ]
    for test in tests:
        integrate_stdin_test_helper(monkeypatch, capsys,
                                    test.input_content, test.arguments, test.expected_output)


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


def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def search_needle_in_file_line_dict_test_helper(
        input_dict: grep.fl_dict_type, needle: str, regex: bool,
        expected_dict: grep.fl_dict_type) -> bool:
    return grep.search_needle_in_file_line_dict(input_dict, needle, regex) == expected_dict


def test_unit_search_needle_in_file_line_dict():
    func = search_needle_in_file_line_dict_test_helper

    assert func(
        {'file1': ['basic test', 'second line'], 'file2': ['another line']},
        'line', False,
        {'file1': ['second line'], 'file2': ['another line']}
    )
    assert func(
        {'emptyfile1': [], 'emptyfile2': [], 'file3': ['does not match']},
        'needle', False,
        {'emptyfile1': [], 'emptyfile2': [], 'file3': []}
    )
    assert func(
        {'file1': ['', '', ''], 'file2': []},
        'so empty', False,
        {'file1': [], 'file2': []}
    )
    assert func(
        {'file1': ['line 1', 'line 2'], 'file2': ['line 2', 'line 3']},
        '2', False,
        {'file1': ['line 2'], 'file2': ['line 2']}
    )
    assert func(
        {'file1': ['basic Test', 'second line'], 'file2': ['anOther line']},
        '[A-Z]', True,
        {'file1': ['basic Test'], 'file2': ['anOther line']}
    )
    assert func(
        {'emptyfile1': [], 'emptyfile2': [], 'file3': ['does not match']},
        '[A-Z]', True,
        {'emptyfile1': [], 'emptyfile2': [], 'file3': []}
    )
    assert func(
        {'file1': ['line1', 'line 2'], 'file2': ['line 2', 'line3']},
        '\\b\\w{4}\\b', True,
        {'file1': ['line 2'], 'file2': ['line 2']}
    )


def test_unit_lines_to_numbers():
    func = grep.lines_to_numbers
    assert func(
        {'file1': ['basic test', 'second line'], 'file2': ['another line']}
    ) == {'file1': ['2'], 'file2': ['1']}

    assert func(
        {'emptyfile1': [], 'emptyfile2': [], 'file3': ['not empty']}
    ) == {'emptyfile1': ['0'], 'emptyfile2': ['0'], 'file3': ['1']}


def test_unit_print_output_dict(capsys):
    func = grep.print_output_dict

    func({'file1': ['basic test', 'second line'], 'file2': ['another line']}, '{filename}:{line}')
    out, err = capsys.readouterr()
    assert out == 'file1:basic test\nfile1:second line\nfile2:another line\n'
    assert err == ''

    func({'file': ['line1', 'line2']}, '{line}')
    out, err = capsys.readouterr()
    assert out == 'line1\nline2\n'
    assert err == ''

    func({'file': []}, '{line}')
    out, err = capsys.readouterr()
    assert out == '\n'
    assert err == ''

    func({'file': []}, '{line}')
    out, err = capsys.readouterr()
    assert out == '\n'
    assert err == ''


def test_unit_read_files(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    result = grep.read_files(['b.txt', 'a.txt'])
    assert result == {
        'b.txt': ['the needl', 'pref needle suf'],
        'a.txt': ['pref needle', 'needle suf']
    }


def test_unit_read_stdin(monkeypatch):
    monkeypatch.setattr('sys.stdin', io.StringIO('pref needle suf\nohlala\n\n'))
    result = grep.read_stdin()
    assert result == {
        '': ['pref needle suf', 'ohlala', '']
    }
