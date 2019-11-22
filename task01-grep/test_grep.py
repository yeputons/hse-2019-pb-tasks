#!/usr/bin/env python3
import io
import re
import argparse
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


def test_get_required_lines_grep():
    out = grep.get_required_lines(['pref needle', 'needle suf'],
                                  re.compile(re.escape('needle')).search)
    assert out == ['pref needle', 'needle suf']
    out = grep.get_required_lines([], re.compile(re.escape('needle')).search)
    assert out == []
    out = grep.get_required_lines(['Hi', 'Hello'], re.compile('(He)').search)
    assert out == ['Hello']


def test_get_file_lines_grep(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    out = grep.get_file_lines('a.txt')
    assert out == ['pref needle', 'needle suf']
    (tmp_path / 'a.txt').write_text('')
    monkeypatch.chdir(tmp_path)
    out = grep.get_file_lines('a.txt')
    assert out == []


def test_print_fmt_grep(capsys):
    grep.print_fmt(['g'], '{0}:{1}', 'a.txt', False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:g\n'
    grep.print_fmt(['Hello', 'there'], '{0}:{1}', 'General Kenobi', False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'General Kenobi:Hello\nGeneral Kenobi:there\n'
    grep.print_fmt(['General Kenobi'], '{0}:{1}', 'General Grievous', True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'General Grievous:1\n'
    grep.print_fmt([''], '{0}:{1}', 'Nobody', False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Nobody:\n'
    grep.print_fmt([''], '{1}', 'Literally noone', True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_get_matching_grep():
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-i', dest='ignore', action='store_true')
    parser.add_argument('-v', dest='inverse', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    parser.add_argument('-l', dest='has_lines', action='store_true')
    parser.add_argument('-L', dest='no_lines', action='store_true')

    args = parser.parse_args(['-E', 'needle?'])
    assert grep.get_matching(args) == re.compile(args.needle, flags=0).search
    args = parser.parse_args(['needle?'])
    assert grep.get_matching(args) == re.compile(re.escape(args.needle), flags=0).search


def test_get_format_grep():
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    parser.add_argument('-i', dest='ignore', action='store_true')
    parser.add_argument('-v', dest='inverse', action='store_true')
    parser.add_argument('-x', dest='full_match', action='store_true')
    parser.add_argument('-l', dest='has_lines', action='store_true')
    parser.add_argument('-L', dest='no_lines', action='store_true')

    args = parser.parse_args(['needle?', []])
    assert grep.get_format(args) == '{1}'
    args = parser.parse_args(['needle?', ['file']])
    assert grep.get_format(args) == '{1}'
    args = parser.parse_args(['needle?', 'a', 'b'])
    assert grep.get_format(args) == '{0}:{1}'


def test_parse_args_grep():
    assert grep.parse_args(['needle', 'file']) == \
        argparse.Namespace(count=False, files=['file'], full_match=False, has_lines=False,
                           ignore=False, inverse=False, needle='needle', no_lines=False,
                           regex=False)
    assert grep.parse_args(['n', 'a', 'b']) == \
        argparse.Namespace(count=False, files=['a', 'b'], full_match=False, has_lines=False,
                           ignore=False, inverse=False, needle='n', no_lines=False,
                           regex=False)
    assert grep.parse_args(['n', '-c']) == \
        argparse.Namespace(count=True, files=[], full_match=False, has_lines=False,
                           ignore=False, inverse=False, needle='n', no_lines=False,
                           regex=False)
    assert grep.parse_args(['-E', 'n', 'a']) == \
        argparse.Namespace(count=False, files=['a'], full_match=False, has_lines=False,
                           ignore=False, inverse=False, needle='n', no_lines=False,
                           regex=True)
    assert grep.parse_args(['-E', '-c', 'ned', 'a', 'b']) == \
        argparse.Namespace(count=True, files=['a', 'b'], full_match=False, has_lines=False,
                           ignore=False, inverse=False, needle='ned', no_lines=False,
                           regex=True)
