#!/usr/bin/env python3
import io
import grep


def test_integrate_stdin_grep(monkeypatch, capsys) -> None:
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_integrate_stdin_regex_grep(monkeypatch, capsys) -> None:
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_integrate_stdin_grep_count(monkeypatch, capsys) -> None:
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_stdin_regex_grep_count(monkeypatch, capsys) -> None:
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', '-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


def test_integrate_file_grep(tmp_path, monkeypatch, capsys) -> None:
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_integrate_file_regex_grep_count(tmp_path, monkeypatch, capsys) -> None:
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'needle?', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_files_grep(tmp_path, monkeypatch, capsys) -> None:
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_integrate_files_regex_grep(tmp_path, monkeypatch, capsys) -> None:
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle?', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:the needl\nb.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_integrate_files_regex_grep_count(tmp_path, monkeypatch, capsys) -> None:
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'needle?', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:2\na.txt:2\n'


def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys) -> None:
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_unit_files_output(capsys) -> None:
    grep.files_output(2, 'temp.txt', 'needle')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'temp.txt:needle\n'


def test_unit_in_file(tmp_path, monkeypatch, capsys) -> None:
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.in_files('a.txt', 'needle', False, False, 1)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_unit_in_file_count_for_one(tmp_path, monkeypatch, capsys) -> None:
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    grep.in_files('a.txt', 'needle', True, False, 1)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_unit_in_file_count_for_many(tmp_path, monkeypatch, capsys) -> None:
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    grep.in_files('a.txt', 'needle', True, False, 3)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\n'


def test_unit_regex_in_file(tmp_path, monkeypatch, capsys) -> None:
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.in_files('a.txt', 'needle?', False, True, 1)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'the needl\npref needle suf\n'


def test_unit_regex_in_file_count_for_one(tmp_path, monkeypatch, capsys) -> None:
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.in_files('a.txt', 'needle?', True, True, 1)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_unit_regex_in_file_count_for_many(tmp_path, monkeypatch, capsys) -> None:
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.in_files('a.txt', 'needle?', True, True, 10)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\n'


def test_unit_regex_in_file_false(tmp_path, monkeypatch, capsys) -> None:
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.in_files('a.txt', 'needle?', False, False, 1)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
