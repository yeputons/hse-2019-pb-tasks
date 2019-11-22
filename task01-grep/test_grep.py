#!/usr/bin/env python3
import io
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


def test2_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'needle?', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:2\na.txt:2\n'


def test_input_from_files_without_e(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test2_input_from_files_without_e(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:pref needle\na.txt:needle suf\nb.txt:pref needle suf\n'


def test3_input_from_files_without_e(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\nb.txt:1\n'


def test_unit_input_from_files_without_e(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt']
    grep.input_from_files(files, 'needle', True, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test2_unit_input_from_files_without_e(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt']
    grep.input_from_files(files, 'needle', False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle\nneedle suf\n'


def test3_unit_input_from_files_without_e(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt']
    grep.input_from_files(files, 'needle', True, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test4_unit_input_from_files_without_e(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt', 'b.txt']
    grep.input_from_files(files, 'needle', True, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\nb.txt:1\n'


def test5_unit_input_from_files_without_e(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt', 'b.txt']
    grep.input_from_files(files, 'needle', False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:pref needle\na.txt:needle suf\nb.txt:pref needle suf\n'


def test_unit_input_from_files_with_e(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt']
    grep.input_from_files(files, 'needle?', False, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test2_unit_input_from_files_with_e(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt']
    grep.input_from_files(files, 'needle?', True, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


def test3_unit_input_from_files_with_e(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    (tmp_path / 'b.txt').write_text('pref needl\n')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt', 'b.txt']
    grep.input_from_files(files, 'needle?', True, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:4\nb.txt:1\n'


def test4_unit_input_from_files_with_e(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\n')
    (tmp_path / 'b.txt').write_text('pref needl\n')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt', 'b.txt']
    grep.input_from_files(files, 'needle?', False, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:the needl\nb.txt:pref needl\n'


def test5unit_input_from_files_with_e(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the need\n')
    (tmp_path / 'b.txt').write_text('pref need\n')
    monkeypatch.chdir(tmp_path)
    files = ['a.txt', 'b.txt']
    grep.input_from_files(files, 'needle?', False, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_unit_input_from_stdin_without_e(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.input_from_stdin('needle', True, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test2_unit_input_from_stdin_without_e(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.input_from_stdin('needle', False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle\nneedle suf\npref needle suf\n'


def test_unit_input_from_stdin_with_e(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.input_from_stdin('needle?', False, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test2_unit_input_from_stdin_with_e(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.input_from_stdin('needle?', True, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'
