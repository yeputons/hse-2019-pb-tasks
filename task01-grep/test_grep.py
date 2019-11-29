from typing import List
import argparse as ap
import io
import grep


def test_parse_args_without_flags():
    args_str: List[str] = ['-c', '-E', 'needle']
    args: ap.Namespace = grep.parse_args(args_str)
    assert args.count and args.regex and args.pattern == 'needle'


def test_parse_args_with_flags():
    args_str: List[str] = ['needle']
    args: ap.Namespace = grep.parse_args(args_str)
    assert not args.count and not args.regex and args.pattern == 'needle'


def test_not_regex_pattern_found_in_line():
    assert grep.pattern_in_line('h+i?', 'ah+i?he', False)


def test_regex_pattern_found_in_line():
    assert grep.pattern_in_line('h+i?', 'ahhhe', True)


def test_not_regex_pattern_not_found_in_line():
    assert not grep.pattern_in_line('h+i?', 'ahhhe', False)


def test_regex_pattern_not_found_in_line():
    assert not grep.pattern_in_line('h+i?', 'aiiie', True)


def test_strip_lines():
    data: List[str] = ['pref needle?\n', 'needle? suf\n', 'the needl\n', 'pref needle? suf']
    assert grep.strip_lines(data) == ['pref needle?', 'needle? suf',
                                      'the needl', 'pref needle? suf']


def test_find_matches():
    data = ['ahhhe', 'h+i?', 'qwerty']
    assert grep.find_matches('h+i?', data, False) == ['h+i?']
    assert grep.find_matches('h+i?', data, True) == ['ahhhe', 'h+i?']


def test_format_data():
    data: List[str] = ['abcdef', 'asdf', 'qwerty', 'oo']
    assert grep.format_data(data, True, None) == ['4']
    assert grep.format_data(data, False, 'name') == ['name:abcdef',
                                                     'name:asdf', 'name:qwerty', 'name:oo']


def test_find_in_file():
    data: List[str] = ['pref needle?', 'needle? suf\n', 'the needl', 'pref needle? suf']
    assert grep.find_in_source(data, 'needle?', False, False) == ['pref needle?',
                                                                  'needle? suf', 'pref needle? suf']


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
