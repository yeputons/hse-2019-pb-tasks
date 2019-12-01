#!/usr/bin/env python3
import io
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


def test_integrate_stdin_grep_ignore(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref NEEDLE?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-i', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref NEEDLE?\nneedle? suf\npref needle? suf\n'


def test_integrate_stdin_grep_ignore_invert(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref NEEDLE?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-iv', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'the needl\n'


def test_integrate_stdin_grep_invert(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref NEEDLE?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-v', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref NEEDLE?\nthe needl\n'


def test_find_in_not_reg_fullmatch():
    assert not grep.find_in_not_reg('line', 'needle line', True)


def test_find_in_reg_not_fullmatch():
    assert grep.find_in_reg('line', 'l+', False)


def test_find_in_invert():
    assert grep.find_in('line', 'needle', False, False, True, False)


def test_add_format_line(tmp_path):
    listres = []
    grep.add_format_line('line', (tmp_path / 'a.txt'), 10, listres)
    assert listres == ['a.txt:line']


def test_collect_res(tmp_path):
    dictlistres = {(tmp_path / 'a.txt'): [],
                   (tmp_path / 'a.txt'): ['abc']}
    dictfiles = {(tmp_path / 'a.txt'): 'empty',
                 (tmp_path / 'a.txt'): 'found'}
    listres = grep.collect_res(dictlistres, dictfiles, True, False, False)
    assert listres != ['a.txt:0', 'b.txt:1']


def test_print_res(capsys):
    listres = ['abc', '123', 'What shall I write?..']
    grep.print_res(listres)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'abc\n123\nWhat shall I write?..\n'
