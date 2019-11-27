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


def test_unit_get_lines_with_needle(capsys):
    lines = ['ball', 'all', 'tall', 'pal lamp', 'hello']
    result = grep.get_lines_with_needle(lines, 'all', False)
    correct = ['ball', 'all', 'tall']
    out, err = capsys.readouterr()
    assert correct == result
    assert out == ''
    assert err == ''


def test_unit_get_lines_with_needle_with_regex(capsys):
    lines = ['ball', 'all', 'tall', 'pal lamp', 'hello']
    result = grep.get_lines_with_needle(lines, 'a?ll', True)
    correct = ['ball', 'all', 'tall', 'hello']
    out, err = capsys.readouterr()
    assert correct == result
    assert out == ''
    assert err == ''


def test_unit_print_needle_with_name(capsys):
    files_and_lines = [('name1', ['ball', 'all', 'tall']), ('name2', ['pal lamp', 'hello'])]
    grep.print_lines(files_and_lines, '{}:{}', False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'name1:ball\nname1:all\nname1:tall\nname2:pal lamp\nname2:hello\n'


def test_unit_print_needle_without_name(capsys):
    files_and_lines = [('', ['ball', 'all', 'tall', 'pal lamp', 'hello'])]
    grep.print_lines(files_and_lines, '{}{}', False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'ball\nall\ntall\npal lamp\nhello\n'


def test_unit_print_lines_with_count_and_name(capsys):
    files_and_lines = [('name1', ['ball', 'all']), ('name2', ['tall', 'pal lamp', 'hello'])]
    grep.print_lines(files_and_lines, '{}:{}', True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'name1:2\nname2:3\n'


def test_unit_find_false(capsys):
    line = 'hi hello good morning'
    needle = 'ell'
    result = grep.find(line, needle, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert result


def test_unit_not_find_false(capsys):
    line = 'hi hello good morning'
    needle = 'god'
    result = grep.find(line, needle, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert not result


def test_unit_find_true(capsys):
    line = 'hi hello good morning gd'
    needle = 'goo?d'
    result = grep.find(line, needle, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert result


def test_unit_not_find_true(capsys):
    line = 'hi hello good morning'
    needle = 'go?ne'
    result = grep.find(line, needle, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert not result


def test_read_from_stdin(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    result = grep.read_from_stdin()
    assert result == ['pref needle?', 'needle? suf', 'the needl', 'pref needle? suf']
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_read_from_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    result = grep.read_from_file('a.txt')
    assert result == ['the needl', 'pref needle suf']
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
