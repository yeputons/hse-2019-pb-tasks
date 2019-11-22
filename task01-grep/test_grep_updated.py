#!/usr/bin/env python3
import argparse
import grep


def test_integrate_all_keys_print_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-livx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def atest_integrate_all_keys_print_not_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-Livx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def atest_integrate_all_keys_count_files_grep(tmp_path, monkeypatch, capsys):
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
