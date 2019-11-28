#!/usr/bin/env python3
import io
import grep
import argparse


# unit tests

# for function search_string_as_regex
def test_unit_search_string_as_regex_ignore_case():
    args = argparse.Namespace(needle='Wings?', ignore_case=True, full_match=False, invert=False)
    assert grep.search_string_as_regex(args, 'winGs') is True
    assert grep.search_string_as_regex(args, 'Wings') is True
    assert grep.search_string_as_regex(args, 'Wingz') is True
    args = argparse.Namespace(needle='Wings', ignore_case=True, full_match=False, invert=False)
    assert grep.search_string_as_regex(args, 'WinGS') is True


def test_unit_search_string_as_regex_full_match():
    args = argparse.Namespace(needle='Wings?', ignore_case=False, full_match=True, invert=False)
    assert grep.search_string_as_regex(args, 'winGs') is False
    assert grep.search_string_as_regex(args, 'Wings') is True
    assert grep.search_string_as_regex(args, 'Wings?') is False
    assert grep.search_string_as_regex(args, 'Wingss') is False
    assert grep.search_string_as_regex(args, 'EWings') is False


def test_unit_search_string_as_regex_invert():
    args = argparse.Namespace(needle='Wings?', ignore_case=False, full_match=False, invert=True)
    assert grep.search_string_as_regex(args, 'winGs') is True
    assert grep.search_string_as_regex(args, 'wingff') is True
    assert grep.search_string_as_regex(args, 'Wings') is False
    assert grep.search_string_as_regex(args, 'Wings?') is False
    assert grep.search_string_as_regex(args, 'Wingss') is False
    assert grep.search_string_as_regex(args, 'EWings') is False


def test_unit_search_string_as_regex_two_flags():
    args = argparse.Namespace(needle='Wings?', ignore_case=True, full_match=False, invert=True)
    assert grep.search_string_as_regex(args, 'wingff') is False
    assert grep.search_string_as_regex(args, 'winGs') is False
    assert grep.search_string_as_regex(args, 'Wings') is False
    assert grep.search_string_as_regex(args, 'Wings?') is False
    assert grep.search_string_as_regex(args, 'Wingss') is False
    assert grep.search_string_as_regex(args, 'EWings') is False
    args = argparse.Namespace(needle='Wings?', ignore_case=False, full_match=True, invert=True)
    assert grep.search_string_as_regex(args, 'winGs') is True
    assert grep.search_string_as_regex(args, 'Wings') is False
    assert grep.search_string_as_regex(args, 'Wings?') is True
    assert grep.search_string_as_regex(args, 'Wingss') is True
    assert grep.search_string_as_regex(args, 'EWings') is True
    args = argparse.Namespace(needle='Wings?', ignore_case=True, full_match=True, invert=False)
    assert grep.search_string_as_regex(args, 'winGs') is True
    assert grep.search_string_as_regex(args, 'Wings') is True
    assert grep.search_string_as_regex(args, 'Wings?') is False
    assert grep.search_string_as_regex(args, 'Wingss') is False
    assert grep.search_string_as_regex(args, 'EWings') is False


def test_unit_search_string_as_regex_all_flags():
    args = argparse.Namespace(needle='Wings?', ignore_case=True, full_match=True, invert=True)
    assert grep.search_string_as_regex(args, 'wingff') is True
    assert grep.search_string_as_regex(args, 'winGs') is False
    assert grep.search_string_as_regex(args, 'Wings') is False
    assert grep.search_string_as_regex(args, 'Wings?') is True
    assert grep.search_string_as_regex(args, 'Wingss') is True
    assert grep.search_string_as_regex(args, 'EWings') is True


# for function search_string
def test_unit_search_string_ignore_case():
    args = argparse.Namespace(needle='Wings*', ignore_case=True, full_match=False, invert=False)
    assert grep.search_string(args, 'Wings*') is True
    assert grep.search_string(args, 'wings*') is True
    assert grep.search_string(args, 'Wings') is False
    assert grep.search_string(args, 'sdgwings*sdg') is True


def test_unit_search_string_full_match():
    args = argparse.Namespace(needle='Wings*', ignore_case=False, full_match=True, invert=False)
    assert grep.search_string(args, 'Wings*') is True
    assert grep.search_string(args, 'wings*') is False
    assert grep.search_string(args, 'Wings**') is False
    assert grep.search_string(args, 'sdgwings*sdg') is False


def test_unit_search_string_invert():
    args = argparse.Namespace(needle='Wings*', ignore_case=False, full_match=False, invert=True)
    assert grep.search_string(args, 'Wings*') is False
    assert grep.search_string(args, 'wings*') is True
    assert grep.search_string(args, 'Wings**') is False
    assert grep.search_string(args, 'sdgwings*sdg') is True


def test_unit_search_string_two_flags():
    args = argparse.Namespace(needle='Wings*', ignore_case=True, full_match=False, invert=True)
    assert grep.search_string(args, 'Wings*') is False
    assert grep.search_string(args, 'wings*') is False
    assert grep.search_string(args, 'Wings') is True
    assert grep.search_string(args, 'sdgwings*sdg') is False
    args = argparse.Namespace(needle='Wings*', ignore_case=False, full_match=True, invert=True)
    assert grep.search_string(args, 'Wings*') is False
    assert grep.search_string(args, 'wings*') is True
    assert grep.search_string(args, 'Wings**') is True
    assert grep.search_string(args, 'sdgwings*sdg') is True
    args = argparse.Namespace(needle='Wings*', ignore_case=True, full_match=True, invert=False)
    assert grep.search_string(args, 'Wings*') is True
    assert grep.search_string(args, 'wings*') is True
    assert grep.search_string(args, 'Wings**') is False
    assert grep.search_string(args, 'sdgwings*sdg') is False


def test_unit_search_string_all_flags():
    args = argparse.Namespace(needle='Wings*', ignore_case=True, full_match=True, invert=True)
    assert grep.search_string(args, 'Wings*') is False
    assert grep.search_string(args, 'wings*') is False
    assert grep.search_string(args, 'Wings**') is True
    assert grep.search_string(args, 'sdgwings*sdg') is True


# for function parse

# for function print_output_for_file


# integrate tests
def test_integrate_stdin_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_integrate_stdin_grep_different_flags(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-c', '-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


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


def test_integrate_stdin_count_zero(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', 'needlestr'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '0\n'


def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_integrate_file_grep_empty(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle?', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_integrate_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_integrate_files_grep_empty_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('There is nothing')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\n'


def test_integrate_files_grep_same_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:pref needle\na.txt:needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_integrate_files_grep_count_empty(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'the', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:0\n'


def test_integrate_files_grep_count_same_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'a.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\na.txt:2\n'


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


def test_integrate_all_keys_not_regex_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-livx', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\na.txt\n'


def test_integrate_some_keys_invert_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-cv', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:0\na.txt:3\n'


def test_integrate_some_keys_ignore_case_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-ci', 'fo', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:3\na.txt:3\n'
