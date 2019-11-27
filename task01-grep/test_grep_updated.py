#!/usr/bin/env python3
import grep
import argparse
import io

input_first = 'it was very funny\n' \
              'he saw this object\n' \
              'summer was cold\n' \
              'saint clause was in my home\n'
input_second = 'yes, when i was a child\n' \
               'i had too many LOVE\n' \
               'it was cool. and now\n' \
               'i remember about it with love'


# integrate test for some files with flag -x
def test_integrate_first(tmp_path, monkeypatch, capsys):
    files = {'first.txt': input_first,
             'second.txt': input_second}

    for file in files:
        (tmp_path / file).write_text(files[file])
    monkeypatch.chdir(tmp_path)
    grep.main(['-x', r'it was cool. and now', 'first.txt', 'second.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'second.txt:it was cool. and now\n'


# integrate test for some files with flag -i
def test_integrate_second(tmp_path, monkeypatch, capsys):
    files = {'first.txt': input_first,
             'second.txt': input_second}

    for file in files:
        (tmp_path / file).write_text(files[file])
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-i', 'love', 'first.txt', 'second.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'first.txt:0\n' \
                  'second.txt:2\n'


# integrate test for some files with flag -v
def test_integrate_third(tmp_path, monkeypatch, capsys):
    files = {'first.txt': input_first,
             'second.txt': input_second}

    for file in files:
        (tmp_path / file).write_text(files[file])
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-v', '-E', r'\s[m][a-z]*', 'first.txt', 'second.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'first.txt:3\n' \
                  'second.txt:3\n'


# integrate test for some files with flags -v and -x
def test_integrate_fourth(tmp_path, monkeypatch, capsys):
    files = {'first.txt': input_first,
             'second.txt': input_second}

    for file in files:
        (tmp_path / file).write_text(files[file])
    monkeypatch.chdir(tmp_path)
    grep.main(['-vx', 'he saw this object', 'first.txt', 'second.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'first.txt:it was very funny\n' \
                  'first.txt:summer was cold\n' \
                  'first.txt:saint clause was in my home\n' \
                  'second.txt:yes, when i was a child\n' \
                  'second.txt:i had too many LOVE\n' \
                  'second.txt:it was cool. and now\n' \
                  'second.txt:i remember about it with love\n'


# integrate test for one file with flag -l
def test_integrate_fifth(tmp_path, monkeypatch, capsys):
    files = {'first.txt': input_first}

    for file in files:
        (tmp_path / file).write_text(files[file])
    monkeypatch.chdir(tmp_path)
    grep.main(['-l', 'was', 'first.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'first.txt\n'


# integrate test for one file with flag -L
def test_integrate_sixth(tmp_path, monkeypatch, capsys):
    files = {'first.txt': input_first}

    for file in files:
        (tmp_path / file).write_text(files[file])
    monkeypatch.chdir(tmp_path)
    grep.main(['-L', '-E', r'\s[c][a-z]*', 'first.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


# integrate test for one file with flags -v and -i
def test_integrate_seventh(tmp_path, monkeypatch, capsys):
    files = {'first.txt': input_second}

    for file in files:
        (tmp_path / file).write_text(files[file])
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-v', '-i', 'love', 'first.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


# integrate test for one file with flag -i and flag -x
def test_integrate_eighth(tmp_path, monkeypatch, capsys):
    files = {'first.txt': input_second}

    for file in files:
        (tmp_path / file).write_text(files[file])
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-xi', r'i had too many love', 'first.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


# integrate test for one file with flag -i and flag -x and flag -v
def test_integrate_ninth(tmp_path, monkeypatch, capsys):
    files = {'first.txt': input_second}

    for file in files:
        (tmp_path / file).write_text(files[file])
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-ixv', r'i had too many love', 'first.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


# integrate test for standard input with flag -i
def test_integrate_tenth(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(input_second))
    grep.main(['-i', 'love'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'i had too many LOVE\n' \
                  'i remember about it with love\n'


def test_for_convert_first():
    string = 'Hello WOrlD'
    args = argparse.Namespace(count=True, name_with_str=False, name_without_str=False,
                              full_find=False, ignore_case=False, inversion=False,
                              files=[], regex=True, substring='[s][g]+')

    data = grep.convert(string, args)
    assert data == string


def test_for_convert_second():
    string = 'Hello WOrlD'
    args = argparse.Namespace(count=True, name_with_str=False, name_without_str=False,
                              full_find=False, ignore_case=True, inversion=True,
                              files=[], regex=True, substring='[s][g]+')

    data = grep.convert(string, args)
    assert data == 'hello world'
