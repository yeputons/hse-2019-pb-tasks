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


def test_unit_find_regex_ign_full_false(capsys):
    line = 'hi hELLlo God morning gd'
    needle = 'gO?Od'
    flags = {
        'count': False,
        'regex': True,
        'igncase': True,
        'rev': False,
        'fullmatch': True,
        'good_file_names': False,
        'bad_file_names': False
    }
    result = grep.find(line, needle, flags)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert not result


def test_unit_find_regex_ign_full_true(capsys):
    line = 'god'
    needle = 'gO?Od'
    flags = {
        'count': False,
        'regex': True,
        'igncase': True,
        'rev': False,
        'fullmatch': True,
        'good_file_names': False,
        'bad_file_names': False
    }
    result = grep.find(line, needle, flags)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert result


def test_unit_find_regex_ign_true(capsys):
    line = 'hi hELLlo God morning gd'
    needle = 'gO?Od'
    flags = {
        'count': False,
        'regex': True,
        'igncase': True,
        'rev': False,
        'fullmatch': False,
        'good_file_names': False,
        'bad_file_names': False
    }
    result = grep.find(line, needle, flags)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert result


def test_unit_find_regex_ign_false(capsys):
    line = 'hi hELLlo God morning gd'
    needle = 'gO+Od'
    flags = {
        'count': False,
        'regex': True,
        'igncase': True,
        'rev': False,
        'fullmatch': False,
        'good_file_names': False,
        'bad_file_names': False
    }
    result = grep.find(line, needle, flags)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert not result


def test_unit_find_regex_full_false(capsys):
    line = 'hi hELLlo god morning gd'
    needle = 'gO?Od'
    flags = {
        'count': False,
        'regex': True,
        'igncase': False,
        'rev': False,
        'fullmatch': True,
        'good_file_names': False,
        'bad_file_names': False
    }
    result = grep.find(line, needle, flags)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert not result


def test_unit_find_regex_full_true(capsys):
    line = 'god'
    needle = 'gO?od'
    flags = {
        'count': False,
        'regex': True,
        'igncase': False,
        'rev': False,
        'fullmatch': True,
        'good_file_names': False,
        'bad_file_names': False
    }
    result = grep.find(line, needle, flags)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert result


def test_unit_find_regex_true(capsys):
    line = 'hi hELLlo GOd morning gd'
    needle = 'GO?Od'
    flags = {
        'count': False,
        'regex': True,
        'igncase': False,
        'rev': False,
        'fullmatch': False,
        'good_file_names': False,
        'bad_file_names': False
    }
    result = grep.find(line, needle, flags)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert result


def test_unit_find_regex_false(capsys):
    line = 'hi hELLlo God morning gd'
    needle = 'gOd'
    flags = {
        'count': False,
        'regex': True,
        'igncase': False,
        'rev': False,
        'fullmatch': False,
        'good_file_names': False,
        'bad_file_names': False
    }
    result = grep.find(line, needle, flags)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert not result


def test_unit_find_ign_full_false(capsys):
    line = 'hi hELLlo God morning gd'
    needle = 'gOOd'
    flags = {
        'count': False,
        'regex': False,
        'igncase': True,
        'rev': False,
        'fullmatch': True,
        'good_file_names': False,
        'bad_file_names': False
    }
    result = grep.find(line, needle, flags)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert not result


def test_unit_find_ign_full_true(capsys):
    line = 'god'
    needle = 'gOd'
    flags = {
        'count': False,
        'regex': False,
        'igncase': True,
        'rev': False,
        'fullmatch': True,
        'good_file_names': False,
        'bad_file_names': False
    }
    result = grep.find(line, needle, flags)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert result


def test_unit_find_ign_true(capsys):
    line = 'hi hELLlo GoOd morning gd'
    needle = 'o gOOd'
    flags = {
        'count': False,
        'regex': False,
        'igncase': True,
        'rev': False,
        'fullmatch': False,
        'good_file_names': False,
        'bad_file_names': False
    }
    result = grep.find(line, needle, flags)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert result


def test_unit_find_ign_false(capsys):
    line = 'hi hELLlo God morning gd'
    needle = 'gOOd'
    flags = {
        'count': False,
        'regex': False,
        'igncase': True,
        'rev': False,
        'fullmatch': False,
        'good_file_names': False,
        'bad_file_names': False
    }
    result = grep.find(line, needle, flags)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert not result


def test_unit_find_full_false(capsys):
    line = 'hi hELLlo god morning gd'
    needle = 'eLLo gOd'
    flags = {
        'count': False,
        'regex': False,
        'igncase': False,
        'rev': False,
        'fullmatch': True,
        'good_file_names': False,
        'bad_file_names': False
    }
    result = grep.find(line, needle, flags)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert not result


def test_unit_find_full_true(capsys):
    line = 'god'
    needle = 'god'
    flags = {
        'count': False,
        'regex': False,
        'igncase': False,
        'rev': False,
        'fullmatch': True,
        'good_file_names': False,
        'bad_file_names': False
    }
    result = grep.find(line, needle, flags)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert result


def test_unit_find_true(capsys):
    line = 'hi hELLlo GOd morning gd'
    needle = 'GOd'
    flags = {
        'count': False,
        'regex': False,
        'igncase': False,
        'rev': False,
        'fullmatch': False,
        'good_file_names': False,
        'bad_file_names': False
    }
    result = grep.find(line, needle, flags)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert result


def test_unit_find_false(capsys):
    line = 'hi hELLlo God morning gd'
    needle = 'gOd'
    flags = {
        'count': False,
        'regex': False,
        'igncase': False,
        'rev': False,
        'fullmatch': False,
        'good_file_names': False,
        'bad_file_names': False
    }
    result = grep.find(line, needle, flags)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert not result


def test_unit_get_lines_with_needle(capsys):
    lines = ['ball', 'all', 'tALL', 'pal lamp', 'hello']
    flags = {
        'count': False,
        'regex': False,
        'igncase': True,
        'rev': False,
        'fullmatch': False,
        'good_file_names': False,
        'bad_file_names': False
    }
    result = grep.get_lines_with_needle(lines, 'all', flags)
    correct = ['ball', 'all', 'tALL']
    out, err = capsys.readouterr()
    assert correct == result
    assert out == ''
    assert err == ''


def test_unit_get_lines_with_needle_rev(capsys):
    lines = ['ball', 'all', 'tALL', 'pal laMP', 'hello']
    flags = {
        'count': False,
        'regex': False,
        'igncase': True,
        'rev': True,
        'fullmatch': False,
        'good_file_names': False,
        'bad_file_names': False
    }
    result = grep.get_lines_with_needle(lines, 'all', flags)
    correct = ['pal laMP', 'hello']
    out, err = capsys.readouterr()
    assert correct == result
    assert out == ''
    assert err == ''


def test_unit_print_needle_with_names_one_empty(capsys):
    files_and_lines = [
        ('name1', ['ball', 'all', 'tall']),
        ('name2', ['pal lamp', 'hello']),
        ('name3', [])
    ]
    flags = {
        'count': False,
        'regex': False,
        'igncase': False,
        'rev': False,
        'fullmatch': False,
        'good_file_names': False,
        'bad_file_names': False
    }
    grep.print_lines(files_and_lines, '{}:{}', flags)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'name1:ball\nname1:all\nname1:tall\nname2:pal lamp\nname2:hello\n'


def test_unit_print_needle_with_names_good(capsys):
    files_and_lines = [
        ('name1', ['ball', 'all', 'tall']),
        ('name2', ['pal lamp', 'hello']),
        ('name3', [])
    ]
    flags = {
        'count': False,
        'regex': False,
        'igncase': False,
        'rev': False,
        'fullmatch': False,
        'good_file_names': True,
        'bad_file_names': False
    }
    grep.print_lines(files_and_lines, '{}:{}', flags)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'name1\nname2\n'


def test_unit_print_needle_with_names_bad(capsys):
    files_and_lines = [
        ('name1', ['ball', 'all', 'tall']),
        ('name2', ['pal lamp', 'hello']),
        ('name3', [])
    ]
    flags = {
        'count': False,
        'regex': False,
        'igncase': False,
        'rev': False,
        'fullmatch': False,
        'good_file_names': False,
        'bad_file_names': True
    }
    grep.print_lines(files_and_lines, '{}:{}', flags)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'name3\n'
