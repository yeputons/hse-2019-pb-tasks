#!/usr/bin/env python3

import io
import grep


def test_matching():
    needle = 'abab'
    line = 'kkajfababafg'
    assert grep.match(needle, line, {grep.REGEX: False})
    needle = 'aba?a'
    line = 'abra'
    assert not grep.match(needle, line, {grep.REGEX: False})
    line = 'abaaa'
    assert grep.match(needle, line, {grep.REGEX: True})


def test_preproccesing():
    assert grep.preproccesing(['afasf\n', 'afaksf\n']) == ['afasf', 'afaksf']
    assert grep.preproccesing([]) == []
    assert grep.preproccesing(['wer', '\n']) == ['wer', '']


def test_search_needle_in_src():
    needle = 'abab'
    src = []
    assert grep.search_needle_in_src(needle, src, {grep.REGEX: False}) == []
    src = ['qababr', 'qadbab', 'quabab']
    assert grep.search_needle_in_src(needle, src, {grep.REGEX: False}) == [
        'qababr', 'quabab']
    needle = '[1]'
    src = ['[2 ghs', ']] req', '[1e]', 'pp[1]asf']
    assert grep.search_needle_in_src(
        needle, src, {grep.REGEX: False}) == ['pp[1]asf']
    needle = 'a'
    src = ['rtt', 'pq', 'cnb']
    assert grep.search_needle_in_src(needle, src, {grep.REGEX: False}) == []


def test_print_search_result(capsys):
    grep.print_search_result({'stdin': ['afa', 'aqwe']})
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'afa\naqwe\n'
    grep.print_search_result({'input.txt': ['aa', ' bb']}, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'
    grep.print_search_result(
        {'input.txt': ['aa', 'bbb'], 'input2.txt': ['bb', 'aaa']})

    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'input.txt:aa\ninput.txt:bbb\ninput2.txt:bb\ninput2.txt:aaa\n'


def test_integrate_stdin_grep(monkeypatch, capsys):
    monkeypatch.setattr(
        'sys.stdin',
        io.StringIO('pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_integrate_stdin_regex_grep(monkeypatch, capsys):
    monkeypatch.setattr(
        'sys.stdin',
        io.StringIO('pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_integrate_stdin_grep_count(monkeypatch, capsys):
    monkeypatch.setattr(
        'sys.stdin',
        io.StringIO('pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_stdin_regex_grep_count(monkeypatch, capsys):
    monkeypatch.setattr(
        'sys.stdin',
        io.StringIO('pref needle\nneedle suf\nthe needl\npref needl suf'))
    grep.main(['-c', '-E', 'ne*dle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


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


def test_integrate_non_trivial(tmp_path, monkeypatch, capsys):
    (tmp_path/'a.txt').write_text('abgf?e\nioqs\nklo*a\n')
    (tmp_path/'b.txt').write_text('gf?etr\nths\nro?a\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'ro?a', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
