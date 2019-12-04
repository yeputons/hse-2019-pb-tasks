#!/usr/bin/env python3
import argparse
import re
import grep


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


def test_parse_args_grep():
    assert grep.parse_args(['-i', 'needle', 'file']) == \
        argparse.Namespace(count=False, files=['file'], full_match=False, has_lines=False,
                           ignore=True, inverse=False, needle='needle', no_lines=False,
                           regex=False)
    assert grep.parse_args(['-i', '-x', '-v', '-c', '-E', 'n', 'a', 'b']) == \
        argparse.Namespace(count=True, files=['a', 'b'], full_match=True, has_lines=False,
                           ignore=True, inverse=True, needle='n', no_lines=False,
                           regex=True)
    assert grep.parse_args(['n', '-l']) == \
        argparse.Namespace(count=False, files=[], full_match=False, has_lines=True,
                           ignore=False, inverse=False, needle='n', no_lines=False,
                           regex=False)
    assert grep.parse_args(['-E', '-L', 'n', 'a']) == \
        argparse.Namespace(count=False, files=['a'], full_match=False, has_lines=False,
                           ignore=False, inverse=False, needle='n', no_lines=True,
                           regex=True)
    assert grep.parse_args(['-i', '-x', '-v', '-c', '-E', '-l', '-L', 'n', 'a', 'b']) == \
        argparse.Namespace(count=True, files=['a', 'b'], full_match=True, has_lines=True,
                           ignore=True, inverse=True, needle='n', no_lines=True,
                           regex=True)


def test_print_fmt_grep(capsys):
    args = grep.parse_args(['-l', 'needle?'])
    grep.print_fmt(['g'], '{0}', 'a.txt', args)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'
    args = grep.parse_args(['-L', 'needle?'])
    grep.print_fmt(['Hello', 'there'], '{0}', 'General Kenobi', args)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    args = grep.parse_args(['-L', 'needle?'])
    grep.print_fmt([], '{0}', 'General Grievous', args)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'General Grievous\n'
    args = grep.parse_args(['-l', 'needle?'])
    grep.print_fmt([], '{0}', 'Nobody', args)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_get_matching_grep():
    args = grep.parse_args(['-i', '-E', 'needle?'])
    assert grep.get_matching(args) == re.compile(args.needle, flags=re.I).search
    args = grep.parse_args(['-x', 'needle?'])
    assert grep.get_matching(args) == re.compile(re.escape(args.needle), flags=0).fullmatch
    args = grep.parse_args(['-ix', 'needle?'])
    assert grep.get_matching(args) == re.compile(re.escape(args.needle), flags=re.I).fullmatch
    args = grep.parse_args(['-v', '-E', 'neeafewfqwfqwfwqdle?'])


def test_get_format_grep():
    args = grep.parse_args(['-l', 'needle?', []])
    assert grep.get_format(args) == '{0}'
    args = grep.parse_args(['-L', 'needle?', ['file']])
    assert grep.get_format(args) == '{0}'
