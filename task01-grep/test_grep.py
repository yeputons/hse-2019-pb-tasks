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


def test_print_result_filename_and_text(capsys):
    grep.print_result(['b.txt:1', 'a.txt:2'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_print_result_text(capsys):
    grep.print_result(['a', 'b', 'c'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a\nb\nc\n'


def test_strip_lines():
    lines = ['London\n', '\nis\n', 'the capital\n of Great Britain.\n\n']
    lines = grep.strip_lines(lines)
    assert lines == ['London', '\nis', 'the capital\n of Great Britain.']


def test_filter_lines_without_regex_with_substring():
    assert grep.filter_lines('b', ['aba', 'bcd', 'banana'],
                             is_regex=False) == ['aba', 'bcd', 'banana']


def test_filter_lines_with_regex_with_regular_expression():
    assert grep.filter_lines('a*b', ['aba', 'bcd', 'banana'],
                             is_regex=True) == ['aba', 'bcd', 'banana']


def test_filter_lines_without_regex_with_regular_expression():
    assert grep.filter_lines('a*b', ['aba', 'bcd', 'banana'], is_regex=False) == []


def test_filter_lines_with_regex_with_substring():
    assert grep.filter_lines('a', ['aba', 'bcd', 'banana'], is_regex=True) == ['aba', 'banana']


def test_grep_lines_without_regex_without_counting_mode():
    assert grep.grep_lines(['abc'], 'file.txt', 'a', is_regex=False,
                           counting_mode=False) == ['file.txt:abc']


def test_grep_lines_without_regex_with_counting_mode():
    assert grep.grep_lines(['abc'], 'file.txt', 'a', is_regex=False,
                           counting_mode=True) == ['file.txt:1']


def test_grep_lines_with_regex_with_counting_mode():
    assert grep.grep_lines(['abc'], 'file.txt', 'a', is_regex=True,
                           counting_mode=True) == ['file.txt:1']


def test_grep_lines_with_regex_without_counting_mode():
    assert grep.grep_lines(['abc'], 'file.txt', 'a', is_regex=True,
                           counting_mode=False) == ['file.txt:abc']


def test_match_pattern_without_regex_with_substring():
    assert grep.match_pattern('Ma', 'Masha', is_regex=False)


def test_match_pattern_with_regex_with_regular_expression():
    assert grep.match_pattern('a*', 'Masha', is_regex=True)


def test_match_pattern_with_regex_with_substring():
    assert grep.match_pattern('Ma', 'Masha', is_regex=True)


def test_match_pattern_without_regex_with_regular_expression():
    assert not grep.match_pattern('a*', 'Masha', is_regex=False)
