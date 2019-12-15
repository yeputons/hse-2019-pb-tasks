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


def test_integrate_ignore(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('aaaa\nAbbA\na\naa\n')
    (tmp_path / 'b.txt').write_text('A\nAAAA\naa\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', 'aA', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:AAAA\nb.txt:aa\na.txt:aaaa\na.txt:aa\n'


def test_integrate_invert_and_ignore(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('aaaa\nAbbA\na\naa\natata\n')
    (tmp_path / 'b.txt').write_text('ahaha\nA\nAAAA\naa\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-vi', 'aA', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:ahaha\nb.txt:A\na.txt:AbbA\na.txt:a\na.txt:atata\n'


def test_integrate_invert_and_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('aaaaa\nask\nme')
    (tmp_path / 'b.txt').write_text('ahaha\nA\nAAAA\naa\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-v', '-E', 'a+', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:A\nb.txt:AAAA\na.txt:me\n'


def test_integrate_full_match(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('aaa\nAAA\n')
    (tmp_path / 'b.txt').write_text('ahaha\nA\nAAAA\naaa\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-x', 'aaa', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:aaa\na.txt:aaa\n'


def test_integrate_full_match_and_ignore(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('aAa\naaA\n')
    (tmp_path / 'b.txt').write_text('ahaha\nA\nAAAA\nAaa\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-xi', 'aaa', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:Aaa\na.txt:aAa\na.txt:aaA\n'


def test_integrate_all_keys_with_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('aaa\nAAA\n')
    (tmp_path / 'b.txt').write_text('ahaha\nA\nAAAA\naaa\nasdfj')
    monkeypatch.chdir(tmp_path)
    grep.main(['-cvxi', 'aaa', 'b.txt', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:4\na.txt:0\nb.txt:4\n'


def test_integrate_all_keys_with_print_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('ahaha\nA\nAAAA\naaa\nal')
    (tmp_path / 'b.txt').write_text('ahaha\nAAAA\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-lvxi', 'aaa', 'b.txt', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\na.txt\nb.txt\n'


def test_unit_match_files_with_filtered_strings():
    data = [('a.txt', ['aa', 'a', 'Lalalala']),
            ('b.txt', ['alex', 'xela']),
            ('in.txt', []),
            ('a.txt', ['aa', 'a', 'Lalalala'])]
    flag_not_strings = False
    ans = grep.match_files_with_filtered_strings(data, flag_not_strings)
    assert ans == [['a.txt', 'b.txt', 'a.txt']]
    data = [('a.txt', []),
            ('b.txt', ['i try']),
            ('in.txt', []),
            ('a.txt', [])]
    flag_not_strings = True
    ans = grep.match_files_with_filtered_strings(data, flag_not_strings)
    assert ans == [['a.txt', 'in.txt', 'a.txt']]


def test_unit_regex_search():
    pattern = 'a+b+c'
    string = 'aaabbbbc'
    full = True
    ans = grep.regex_search(pattern, string, full)
    assert ans
    pattern = 'abc+'
    string = 'aaac'
    full = False
    ans = grep.regex_search(pattern, string, full)
    assert not ans
