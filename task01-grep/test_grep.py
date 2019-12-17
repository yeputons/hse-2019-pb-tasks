#!/usr/bin/env python3
import io
import argparse
import grep


def test_get_lines_from_file(tmp_path, monkeypatch):
    (tmp_path / 'this.txt').write_text('grrr\ngre\n')
    monkeypatch.chdir(tmp_path)
    assert grep.get_lines_from_file('this.txt') == ['grrr', 'gre']


def test_find_pattern_common():
    args = grep.parse_args(['-E', 'needle?', 'needle?', 'needlee'])
    assert grep.find_pattern_common(args, 'needlee') is False
    assert grep.find_pattern_common(args, 'needle?') is True


def test_find_pattern_regex():
    args = grep.parse_args(['needle?', 'ndle', 'needlee'])
    assert grep.find_pattern_regex(args, 'needlee') is True
    assert grep.find_pattern_regex(args, 'ndle') is False


def test_is_matching_regex():
    args = grep.parse_args(['-E', 'needle?', 'ndle', 'needlee'])
    assert grep.is_matching(args, 'ndle') is False
    assert grep.is_matching(args, 'needle?') is True


def test_is_matching_common():
    args = grep.parse_args(['needle?', 'ndle', 'needle?'])
    assert grep.is_matching(args, 'needle?') is True
    assert grep.is_matching(args, 'ndle') is False


def choose_format(args: argparse.Namespace) -> str:
    if args.print_files or args.print_not_files:
        return '{0}'
    return '{0}:{1}' if len(args.files) > 1 else '{1}'


def test_choose_format_many_files(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    args = grep.parse_args(['needle', 'b.txt', 'a.txt'])
    assert grep.choose_format(args) == '{0}:{1}'


def test_choose_format_one_file(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    args = grep.parse_args(['needle', 'a.txt'])
    assert grep.choose_format(args) == '{1}'


def test_choose_format_no_files():
    args = grep.parse_args(['needle', 'needle?'])
    assert grep.choose_format(args) == '{1}'


def test_print_output_common(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    monkeypatch.chdir(tmp_path)
    args = grep.parse_args(['pref needle?', 'a.txt'])
    grep.print_output(['pref needle?', 'needle? suf',
                       'the needl', 'pref needle? suf'], '', args)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\npref needle? suf\n'


def test_print_output_common_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    monkeypatch.chdir(tmp_path)
    args = grep.parse_args(['-c', 'pref needle?', 'a.txt'])
    grep.print_output(['pref needle?', 'needle? suf', 'the needl',
                       'pref needle? suf'], '', args)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_print_output_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    monkeypatch.chdir(tmp_path)
    args = grep.parse_args(['-E', 'pref needle?', 'a.txt'])
    grep.print_output(['pref needle?', 'needle? suf', 'the needl',
                       'pref needle? suf'], '', args)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\npref needle? suf\n'


def test_print_output_regex_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    monkeypatch.chdir(tmp_path)
    args = grep.parse_args(['-c', '-E', 'needle', 'a.txt'])
    grep.print_output(['pref needle?', 'needle? suf', 'the needl',
                       'pref needle? suf'], '', args)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_stdin_regex_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'ggggrep\ngrep?grep!\ngrrrep\ngreppppp'))
    grep.main(['-c', '-E', 'grep?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_files_regex_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'this.txt').write_text('grrr\ngre\n')
    (tmp_path / 'that.txt').write_text('grep!\nggggrepppp')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'grep?', 'this.txt', 'that.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'this.txt:1\nthat.txt:2\n'


# Tests below were already given


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
