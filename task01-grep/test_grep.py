#!/usr/bin/env python3
import io
import sys
import grep


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


def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_integrate_files_grep_count_multifile(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    (tmp_path / 'c.txt').write_text('need something\nneedl one more\nneedler is here')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt', 'b.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\nb.txt:1\nc.txt:1\n'


def test_unit_read_input_files(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('Is it real?\nNot_:)\n')
    (tmp_path / 'b.txt').write_text('')
    (tmp_path / 'c.txt').write_text('\n')
    monkeypatch.chdir(tmp_path)
    out = grep.read_input(['a.txt', 'b.txt', 'c.txt'])
    assert out == [['Is it real?', 'Not_:)'], [], ['']]


def test_unit_read_input_stdin(monkeypatch):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\nneedle? suf\nit is not needle'))
    out = grep.read_input([])
    assert out == [['pref needle?', 'needle? suf', 'the needl', 'needle? suf', 'it is not needle']]


def test_unit_detect_lines_substring():
    input_lines = [['cry', "don't cry"], ['crack', 'hehe'], ['', 'rc']]
    detection_func = grep.get_detection_func('cr', False)
    out = grep.detect_requested_lines(detection_func, input_lines)
    assert out == [['cry', "don't cry"], ['crack'], []]


def test_unit_detect_lines_substring_strange():
    input_lines = [['cry', "don't cry"], ['crack', 'hehe'], ['', 'rc']]
    detection_func = grep.get_detection_func('', False)
    out = grep.detect_requested_lines(detection_func, input_lines)
    assert out == input_lines


def test_unit_detect_lines_regex():
    input_lines = [['cry', "don't cry"], ['crack', 'hehe'], ['', 'rc'], ['not here']]
    detection_func = grep.get_detection_func('cr?', True)
    out = grep.detect_requested_lines(detection_func, input_lines)
    assert out == [['cry', "don't cry"], ['crack'], ['rc'], []]


def test_unit_detect_lines_regex_strange():
    input_lines = [['cry', "don't cry"], ['crack', 'hehe'], ['', 'rc'], ['not here']]
    detection_func = grep.get_detection_func('', True)
    out = grep.detect_requested_lines(detection_func, input_lines)
    assert out == input_lines


def test_unit_prepare_output_lines():
    input_lines = [['for what?', 'hz', ''], ['', 'right'], ['']]
    out = grep.prepare_output(input_lines, False)
    assert out == input_lines


def test_unit_prepare_output_lines_count():
    input_lines = [['for what?', 'hz', ''], ['', 'right'], ['']]
    out = grep.prepare_output(input_lines, True)
    assert out == [['3'], ['2'], ['1']]


def test_unit_split_into_lines_files(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('some strange line\none more\n ')
    monkeypatch.chdir(tmp_path)
    out = grep.split_into_lines_file('a.txt')
    assert out == ['some strange line', 'one more', ' ']


def test_unit_split_into_lines(monkeypatch):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref need?\nneedle? suf\nthe needl\npref suf\nit is not needle\n '))
    out = grep.split_into_lines(sys.stdin)
    assert out == ['pref need?', 'needle? suf', 'the needl', 'pref suf', 'it is not needle', ' ']


def test_unit_output(capsys):
    input_lines = [['oh', 'my', 'god', '', ' ', 'end']]
    grep.output([], input_lines)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'oh\nmy\ngod\n\n \nend\n'
