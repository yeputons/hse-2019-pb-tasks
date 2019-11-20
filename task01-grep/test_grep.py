from typing import List
import argparse as ap
import io
import grep


def test_parse_args():
    args_str: List[str] = ['-c', '-E', 'needle']
    args: ap.Namespace = grep.parse_args(args_str)
    assert args.count and args.regex and args.pattern == 'needle'
    args_str = ['needle']
    args = grep.parse_args(args_str)
    assert not args.count and not args.regex and args.pattern == 'needle'


def test_strip_lines(tmp_path, monkeypatch):
    (tmp_path / 'test1.txt').write_text('pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    monkeypatch.chdir(tmp_path)
    f = open('test1.txt', 'r+')
    result: List[str] = grep.strip_lines(f)
    f.close()
    assert result == ['pref needle?', 'needle? suf', 'the needl', 'pref needle? suf']


def test_find_matches():
    data: List[str] = ['ahhhe', 'asdfgh', 'h+i?']
    assert grep.find_matches('h', data, False) == ['ahhhe', 'asdfgh', 'h+i?']
    assert grep.find_matches('hh', data, False) == ['ahhhe']
    assert grep.find_matches('h+i?', data, False) == ['h+i?']
    assert grep.find_matches('qw', data, False) == []
    data = ['ahhhe', 'asdfgh', 'h+i?', 'qwerty']
    assert grep.find_matches('h*i?', data, True) == ['ahhhe', 'asdfgh', 'h+i?', 'qwerty']
    assert grep.find_matches('h+i?', data, True) == ['ahhhe', 'asdfgh', 'h+i?']
    assert grep.find_matches('h+i+', data, True) == []


def test_format_data():
    data: List[str] = ['abcdef', 'asdf', 'qwerty', 'oo']
    assert grep.format_data(data, False, False, 'name') == ['abcdef', 'asdf', 'qwerty', 'oo']
    assert grep.format_data(data, True, False, 'name') == ['4']
    assert grep.format_data(data, False, True, 'name') == ['name:abcdef',
                                                           'name:asdf', 'name:qwerty', 'name:oo']
    assert grep.format_data(data, True, True, 'name') == ['name:4']


def test_find_in_file(tmp_path, monkeypatch):
    (tmp_path / 'test1.txt').write_text('pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    monkeypatch.chdir(tmp_path)
    f = open('test1.txt', 'r+')
    result: List[str] = grep.find_in_file(f, 'test1.txt', 'needle?', False, False, False)
    f.close()
    assert result == ['pref needle?', 'needle? suf', 'pref needle? suf']


def test_integrate_stdin_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_integrate_stdin_regex_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'abcdef\nahhhe\nhah\n'))
    grep.main(['-E', 'h+i?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'ahhhe\nhah\n'


def test_integrate_stdin_grep_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'test1.txt').write_text('pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'test1.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_integrate_multiple_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'test1.txt').write_text('pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    monkeypatch.chdir(tmp_path)
    (tmp_path / 'test2.txt').write_text('pre needle?\nneedle? '
                                        'suff\nthe needlll\npreff needle? suff')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'test1.txt', 'test2.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'test1.txt:pref needle?\ntest1.txt:needle? suf\ntest1.txt:pref needle? suf\n' \
                  'test2.txt:pre needle?\ntest2.txt:needle? suff\ntest2.txt:preff needle? suff\n'


def test_integrate_file_regex_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'test1.txt').write_text('abcdef\nahhhe\nhah\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'h+i?', 'test1.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'ahhhe\nhah\n'


def test_integrate_file_count_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'test1.txt').write_text('pref needle\nneedle suf\nthe needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'test1.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_multiple_file_count_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'test1.txt').write_text('pref needle\nneedle suf\nthe needl\npref needle suf')
    (tmp_path / 'test2.txt').write_text('nneedl\naneedleb\nnedle')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'test1.txt', 'test2.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'test1.txt:3\ntest2.txt:1\n'
