#!/usr/bin/env python3
import grep


def test_choose_format_grep_files():
    args = grep.parse_args(['-l', 'needle?', []])
    assert grep.choose_format(args) == '{0}'


def test_choose_format_grep_files_not():
    args = grep.parse_args(['-L', 'needle?', ['file']])
    assert grep.choose_format(args) == '{0}'


def test_print_output_all_keys_common(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneEdlE? Suf\nthe needl')
    monkeypatch.chdir(tmp_path)
    args = grep.parse_args(['-ivx', 'pref needle?', 'a.txt'])
    grep.print_output(['pref needle?', 'neEdlE? Suf', 'the needl', ], '', args)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'neEdlE? Suf\nthe needl\n'


def test_print_output_all_keys_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneEdlE? Suf\nthe needl')
    monkeypatch.chdir(tmp_path)
    args = grep.parse_args(['-E', '-ivx', 'pref needle?', 'a.txt'])
    grep.print_output(['pref needle?', 'neEdlE? Suf', 'the needl', ], '', args)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneEdlE? Suf\nthe needl\n'


def test_print_output_all_keys_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneEdlE? Suf\nthe needl')
    monkeypatch.chdir(tmp_path)
    args = grep.parse_args(['-E', '-civx', 'pref needle?', 'a.txt'])
    grep.print_output(['pref needle?', 'neEdlE? Suf', 'the needl', ], '', args)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_all_keys_count_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('example\n')
    (tmp_path / 'b.txt').write_text('exxxxample\nexomple??\nEXAMBLE!\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '-civx', 'example', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:3\na.txt:0\n'


def test_integrate_all_keys_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('an\nexa\nmple\n')
    (tmp_path / 'b.txt').write_text('example\nexample??\nEXAMPLE!\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '-livx', 'example', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nb.txt\n'


def test_integrate_all_keys_files_not_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('example\n')
    (tmp_path / 'b.txt').write_text('exxxxample\nexomple??\nEXAMBLE!\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '-livx', 'example', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'
