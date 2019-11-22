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


def test_grep_read_from_file1(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    out = grep.read_from_file('a.txt')
    assert out == ['pref needle\n', 'needle suf\n']


def test_grep_read_from_file2(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    monkeypatch.chdir(tmp_path)
    out = grep.read_from_file('a.txt')
    assert out == ['pref needle?\n', 'needle? suf\n', 'the needl\n', 'pref needle? suf']


def test_grep_parse1():
    in_parse = ['-c', '-E', 'needle', 'b.txt', 'a.txt']
    out = grep.parse(in_parse)
    assert out.needle == 'needle'
    assert out.files == ['b.txt', 'a.txt']
    assert out.count_format
    assert out.regex


def test_grep_parse2():
    in_parse = ['-c', 'needle', 'b.txt', 'a.txt']
    out = grep.parse(in_parse)
    assert out.needle == 'needle'
    assert out.files == ['b.txt', 'a.txt']
    assert out.count_format
    assert not out.regex


def test_grep_parse3():
    in_parse = ['-E', 'needle', 'b.txt', 'a.txt']
    out = grep.parse(in_parse)
    assert out.needle == 'needle'
    assert out.files == ['b.txt', 'a.txt']
    assert not out.count_format
    assert out.regex


def test_grep_parse4():
    in_parse = ['-E', 'needle']
    out = grep.parse(in_parse)
    assert out.needle == 'needle'
    assert out.files == []
    assert not out.count_format
    assert out.regex


def test_grep_parse5():
    in_parse = ['needle']
    out = grep.parse(in_parse)
    assert out.needle == 'needle'
    assert out.files == []
    assert not out.count_format
    assert not out.regex


def test_grep_find_substr_count_one_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('aba\nabaca\nfabca nabc\nraba')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'aba', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_grep_find_regex_count_one_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'b.txt').write_text('ababaca\nnabca')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'ab.*a', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_grep_find_substr_one_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('aba\nabaca\nfabca nabc\nraba')
    monkeypatch.chdir(tmp_path)
    grep.main(['aba', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'aba\nabaca\nraba\n'


def test_grep_find_regex_one_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('aba\nabaca\nfabca nabc\nraba')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'ab.+a', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'abaca\nfabca nabc\n'


def test_grep_find_substr_count1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('aba\nabaca\nfabca nabc\nraba')
    (tmp_path / 'b.txt').write_text('ababaca\nnabca')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'aba', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:3\nb.txt:1\n'


def test_grep_find_substr_count2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('aba\nabaca\nfabca nabc\nraba')
    (tmp_path / 'b.txt').write_text('')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'aba', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:3\nb.txt:0\n'


def test_grep_find_regex_count1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('aba\nabaca\nfabca nabc\nraba')
    (tmp_path / 'b.txt').write_text('ababaca\nnabca')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'ab.*a', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:4\nb.txt:2\n'


def test_grep_find_regex_count2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('aba\nabaca\nfabca nabc\nraba')
    (tmp_path / 'b.txt').write_text('ababaca\nnabca')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'ab.+a', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\nb.txt:2\n'


def test_grep_find_substr1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('aba\nabaca\nfabca nabc\nraba')
    (tmp_path / 'b.txt').write_text('')
    monkeypatch.chdir(tmp_path)
    grep.main(['aba', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:aba\na.txt:abaca\na.txt:raba\n'


def test_grep_find_regex1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('aba\nabaca\nfabca nabc\nraba')
    (tmp_path / 'b.txt').write_text('ababaca\nnabca\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'ab.+a', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:abaca\na.txt:fabca nabc\nb.txt:ababaca\nb.txt:nabca\n'


def test_grep_print_matched1(capsys):
    grep.print_matched(['helpme', 'sos'], False, 'a.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'helpme\nsos\n'


def test_grep_print_matched2(capsys):
    grep.print_matched(['helpme', 'sos'], True, 'a.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:helpme\na.txt:sos\n'


def test_grep_print_matched3(capsys):
    grep.print_matched([2], False, 'a.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_grep_print_matched4(capsys):
    grep.print_matched([2], True, 'a.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\n'
