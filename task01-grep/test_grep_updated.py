#!/usr/bin/env python3
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


def test_integrate_files_grep_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-l', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_integrate_files_grep_regex_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf\n')
    (tmp_path / 'c.txt').write_text('needlejf\na needle b\nneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '-l', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nc.txt\n'


def test_integrate_files_grep_ignore_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf\n')
    (tmp_path / 'c.txt').write_text('a o a o NEEDLE LEL\na needle b\nneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', '-l', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nc.txt\n'


def test_integrate_files_grep_fullmatch_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf\n')
    (tmp_path / 'c.txt').write_text('a o a o NEEDLE LEL\na needle b\nneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-x', '-l', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'c.txt\n'


def test_integrate_files_grep_ignore_reverse_strings_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf\n')
    (tmp_path / 'c.txt').write_text('a o a o NEEDLE LEL\na needle b\nneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', '-v', '-l', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_integrate_files_grep_ignore_reverse_strings_reverse_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf\n')
    (tmp_path / 'c.txt').write_text('a o a o NEEDLE LEL\na needle b\nneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', '-v', '-L', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nc.txt\n'


def test_integrate_files_grep_fullmatch_reverse_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf\n')
    (tmp_path / 'c.txt').write_text('a o a o NEEDLE LEL\na needle b\nneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-x', '-L', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\na.txt\n'


def test_integrate_files_grep_ignore_reverse_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf\n')
    (tmp_path / 'c.txt').write_text('a o a o NEEDLE LEL\na needle b\nneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', '-L', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_integrate_files_grep_regex_reverse_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf\n')
    (tmp_path / 'c.txt').write_text('needlejf\na needle b\nneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '-L', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_integrate_files_grep_reverse_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref neeoaoaodle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-L', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'
