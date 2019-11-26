#!/usr/bin/env python3
import io
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


def test_integrate_file_grep_count_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_integrate_stdin_grep_count_regex(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', '-E', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_files_grep_count_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_print_result(capsys):
    grep.print_result(['b.txt:1', 'a.txt:2'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_print_answer_1(capsys):
    grep.print_result(['a', 'b', 'c'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a\nb\nc\n'


def test_strip_lines():
    lines = ['London\n', '\nis\n', 'the capital\n of Great Britain.\n\n']
    lines = grep.strip_lines(lines)
    assert lines == ['London', '\nis', 'the capital\n of Great Britain.']


def test_filter_lines1():
    assert grep.filter_lines(False, 'a', ['aba', 'bcd', 'banana']) == ['aba', 'banana']


def test_filter_lines2():
    assert grep.filter_lines(False, 'b', ['aba', 'bcd', 'banana']) == ['aba', 'bcd', 'banana']


def test_filter_lines3():
    assert grep.filter_lines(True, 'a*b', ['aba', 'bcd', 'banana']) == ['aba', 'bcd', 'banana']


def test_filter_lines4():
    assert grep.filter_lines(False, 'a*b', ['aba', 'bcd', 'banana']) == []


def test_grep_lines1():
    assert grep.grep_lines(['abc'], 'file.txt', 'a', False, False) == ['file.txt:abc']


def test_grep_lines2():
    assert grep.grep_lines(['abc'], 'file.txt', 'a', False, True) == ['file.txt:1']


def test_grep_lines3():
    assert grep.grep_lines(['abc'], 'file.txt', 'a', True, True) == ['file.txt:1']


def test_grep_lines4():
    assert grep.grep_lines(['abc'], 'file.txt', 'a', True, False) == ['file.txt:abc']


def test_match_pattern1():
    assert grep.match_pattern(False, 'Ma', 'Masha')


def test_match_pattern2():
    assert grep.match_pattern(True, 'a*', 'Masha')
