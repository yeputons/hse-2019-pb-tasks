#!/usr/bin/env python3
import io
import grep


# UNIT #


def test_unit_inverse_match():
    def math_all(x):  # pylint: disable=unused-argument
        return True

    def math_none(x):  # pylint: disable=unused-argument
        return False

    def match_asd(x):
        return 'asd' in x

    assert grep.inverse_match(math_all, 'a') is False
    assert grep.inverse_match(math_none, 'a') is True
    assert grep.inverse_match(match_asd, 'a') is True
    assert grep.inverse_match(match_asd, 'asdf') is False


def test_unit_file_filter_all_files():
    assert grep.all_files(('name', [])) is True
    assert grep.all_files(('name', ['asd'])) is True
    assert grep.all_files(('name', ['asd', 'dsa'])) is True
    assert grep.all_files(('name', ['asd', 'dsa', 'sda'])) is True


def test_unit_file_filter_non_empty():
    assert grep.non_empty(('name', [])) is False
    assert grep.non_empty(('name', ['asd'])) is True
    assert grep.non_empty(('name', ['asd', 'dsa'])) is True
    assert grep.non_empty(('name', ['asd', 'dsa', 'sda'])) is True


def test_unit_file_filter_empty_only():
    assert grep.empty_only(('name', [])) is True
    assert grep.empty_only(('name', ['asd'])) is False
    assert grep.empty_only(('name', ['asd', 'dsa'])) is False
    assert grep.empty_only(('name', ['asd', 'dsa', 'sda'])) is False


# INTEGRATION #


def test_integrate_fulltext_ignore_case(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nnEEdLe? suf\nthe neEdl\npref neEDle? suf'))
    grep.main(['-i', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nnEEdLe? suf\npref neEDle? suf\n'


def test_integrate_regex_ignore_case(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref nEEdle?\nneedlE? suf\nthe neeDl\npref needle? suf'))
    grep.main(['-i', '-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref nEEdle?\nneedlE? suf\nthe neeDl\npref needle? suf\n'


def test_integrate_fulltext_inverse(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\npre needle? suf\nthe needl\npref needle? suf'))
    grep.main(['-v', 'pref'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pre needle? suf\nthe needl\n'


def test_integrate_regex_inverse(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\npre needle? suf\nthe needl\npref needle? suf'))
    grep.main(['-v', '-E', 'pref?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'the needl\n'


def test_integrate_fulltext_strict(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\npre needle? suf\nthe needl\npref needle? suf\nneedle'))
    grep.main(['-x', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'needle\n'


def test_integrate_regex_strict(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\npre needle? suf\nneedl\npref needle? suf\nneedle'))
    grep.main(['-x', '-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'needl\nneedle\n'


def test_integrate_list_found(monkeypatch, capsys, tmp_path):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-l', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_integrate_list_empty(monkeypatch, capsys, tmp_path):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-L', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


# GIVEN #


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