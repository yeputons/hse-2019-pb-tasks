#!/usr/bin/env python3
import io
import grep


def test_integrate_stdin_regex_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_integrate_stdin_grep_xc(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf\nneedle\nneedle\nneed'))
    grep.main(['-xc', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_stdin_grep_ix_regex(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO('fooooooooooo\nfo\nfoo\nFOo\nFO'))
    grep.main(['-ix', '-E', 'fo?o'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'fo\nfoo\nFOo\nFO\n'


def test_integrate_parse_stdin_grep_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.parse_std_in('needle?', regex=False, count=True, inv=False, low=False, full_match=False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_parse_stdin_grep_trivial(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.parse_std_in('needle?', regex=False, count=False,
                      inv=False, low=False, full_match=False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_integrate_parse_stdin_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO('WWWWWWOWWWWWWWW\nWOW\nwow\nwowowowoww'))
    grep.parse_std_in('WOW', regex=False, count=False, inv=True, low=True, full_match=True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'WWWWWWOWWWWWWWW\nwowowowoww\n'


def test_integrate_files_grep_lix_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fooooooooooo\nfo\nfoo\nFOo\nFO')
    (tmp_path / 'b.txt').write_text('ooo\nnothing\nRaw test')
    monkeypatch.chdir(tmp_path)
    grep.main(['-lix', '-E', 'fo?o', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_integrate_files_grep_livx_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('foo\nfo\nfoo\nFOo\nFO')
    (tmp_path / 'b.txt').write_text('ooo\nnothing\nRaw test')
    monkeypatch.chdir(tmp_path)
    grep.main(['-livx', '-E', 'fo?o', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_integrate_files_grep_without_matching_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('foo\nfo\nfoo\nFOo\nFO')
    (tmp_path / 'b.txt').write_text('ooo\nnothing\nRaw test')
    monkeypatch.chdir(tmp_path)
    grep.main(['-Lix', '-E', 'fo?o', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_integrate_one_file_l_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-l', 'needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_integrate_one_file_invert_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-L', 'nooooo', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nb.txt\n'


def test_integrate_one_file_grep_trivial(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf\nneedle\n what about needle?')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\nneedle\n what about needle?\n'


def test_integrate_files_grep_trivial(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    files = ['a.txt', 'b.txt']
    monkeypatch.chdir(tmp_path)
    grep.parse_files(files, 'needle', regex=True, count=False, inv=False, low=False,
                     full_match=False, files_only=False, invert_files=False)
    assert 'a.txt:pref needle\na.txt:needle suf\nb.txt:pref needle suf\n'


def test_integrate_files_grep_count(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    files = ['a.txt', 'b.txt']
    monkeypatch.chdir(tmp_path)
    grep.parse_files(files, 'needle', regex=False, count=True, inv=False, low=False,
                     full_match=False, files_only=False, invert_files=False)
    assert 'a.txt:2\nb.txt:1\n'


def test_integrate_files_grep_lowercase_filenames_only(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('woooooooooow\nWow\nWWWWOWWWW')
    (tmp_path / 'b.txt').write_text('ababa\nababab\nbabbbb')
    (tmp_path / 'c.txt').write_text('Wow\nWow\nWow')
    files = ['a.txt', 'b.txt', 'c.txt']
    monkeypatch.chdir(tmp_path)
    grep.parse_files(files, 'WOW', regex=False, count=False, inv=False, low=True,
                     full_match=False, files_only=True, invert_files=False)
    assert 'a.txt\nc.txt\n'


def test_integrate_files_grep_count_invert(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('woooooooooow\nWow\nWWWWOWWWW')
    (tmp_path / 'b.txt').write_text('ababa\nababab\nbabbbb')
    (tmp_path / 'c.txt').write_text('Wow\nWow\nWow')
    files = ['a.txt', 'b.txt', 'c.txt']
    monkeypatch.chdir(tmp_path)
    grep.parse_files(files, 'Wow', regex=False, count=True, inv=True, low=False,
                     full_match=False, files_only=False, invert_files=False)
    assert 'a.txt:2\nb.txt:3\nc.txt:0\n'


def test_integrate_files_grep_invert_files_invert(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('woooooooooow\nWow\nWWWWOWWWW')
    (tmp_path / 'b.txt').write_text('ababa\nababab\nbabbbb')
    (tmp_path / 'c.txt').write_text('Wow\nWow\nWow')
    files = ['a.txt', 'b.txt', 'c.txt']
    monkeypatch.chdir(tmp_path)
    grep.parse_files(files, 'Wow', regex=False, count=True, inv=False, low=False,
                     full_match=False, files_only=False, invert_files=True)
    assert 'c.txt\n'


def test_needle_full_match_find():
    line = 'find\n something here, ffind, Find_here!'
    assert not grep.match(line, 'find', regex=False, low=False, full_match=True, inv=False)


def test_regex_lowercase_find():
    line = 'find something here, FFFind, find f'
    assert grep.match(line, 'F*', regex=True, low=True, full_match=False, inv=False)


def test_make_filtered_list_count():
    line = io.StringIO('find something here\nno\nwhy no?\nwho knows the answer?')
    list_to_check = grep.form_the_list(line, 'no', regex=False, count=True, inv=False,
                                       low=False, full_match=False)
    assert list_to_check == ['3']


def test_make_filtered_list_count_full_match():
    line = io.StringIO('find something here\nno\nwhy no?\nwho knows the answer?')
    list_to_check = grep.form_the_list(line, 'no', regex=False, count=True, inv=False,
                                       low=False, full_match=True)
    assert list_to_check == ['1']


def test_make_filtered_list_trivial():
    line = io.StringIO('find something here\nno\nwhy no?\nwho knows the answer?')
    list_to_check = grep.form_the_list(line, 'no', regex=False, count=False, inv=False,
                                       low=False, full_match=False)
    assert list_to_check == ['no', 'why no?', 'who knows the answer?']


def test_print_list_grep():
    list_ = ['pref needle', 'needle suf']
    grep.formatted_output('a.txt', list_, files_only=False, invert_files=False)
    assert 'a.txt:pref needle\na.txt:needle suf\n'


def test_print_empty_list_invert_grep():
    list_ = []
    grep.formatted_output('a.txt', list_, files_only=True, invert_files=True)
    assert 'a.txt'


def test_print_list_not_one_file_grep():
    lists_ = [[], ['something', 'something', 'something']]
    files = ['a.txt', 'b.txt']
    for i in range(2):
        grep.formatted_output(files[i], lists_[i], files_only=True, invert_files=False)
    assert 'b.txt'


def test_print_list_not_one_file_invert_grep():
    lists_ = [[], ['something', 'something', 'something']]
    files = ['a.txt', 'b.txt']
    for i in range(2):
        grep.formatted_output(files[i], lists_[i], files_only=True, invert_files=True)
    assert 'a.txt'


def test_print_empty_stdin_grep():
    list_ = []
    grep.formatted_output('a.txt', list_, files_only=True, invert_files=True)
    assert 'a.txt'
