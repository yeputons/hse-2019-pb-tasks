#!/usr/bin/env python3
import io
import sys
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


def test_integrate_stdin_regex_count_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-c', '-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


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


def test_integrate_file_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_integrate_files_grep_regex_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_file_grep_get_list(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('hello\naloha\nprivetttt\nOprivetO\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'privet', 'a.txt'])
    with open('a.txt', 'r') as fin:
        print(grep.get_list(False, False, False, False, False, False, '', 'privet', fin))
        out, err = capsys.readouterr()
        assert out == "2\n['privetttt', 'OprivetO']\n"
        assert err == ''


def test_stdin_grep_get_list_stdin(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'hello\naloha\nprivetttt\nOprivetO\n'))
    grep.main(['privet'])
    grep.get_list(False, False, False, False, False, False, '', 'privet', sys.stdin)
    out, err = capsys.readouterr()
    assert out == 'privetttt\nOprivetO\n'
    assert err == ''


def test_grep_find_true():
    regex = False; inverse = False
    find_substr = False; ignore_case = False
    line = 'ThisisaSENtense'
    needle = 'SEN'
    bool_value = grep.find(regex, inverse, find_substr, ignore_case, needle, line)
    assert bool_value
    

def test_grep_find_false():
    regex = False; inverse = False
    find_substr = False; ignore_case = False
    line = 'ThisisaSENtense'
    needle = 'SEN123'
    bool_value = grep.find(regex, inverse, find_substr, ignore_case, needle, line)
    assert not bool_value


def test_grep_find_inverse_true():
    regex = False; inverse = True
    find_substr = False; ignore_case = False
    line = 'ThisisaSENtense'
    needle = 'SEN'
    bool_value = grep.find(regex, inverse, find_substr, ignore_case, needle, line)
    assert not bool_value


def test_grep_find_inverse_false():
    regex = False; inverse = True
    find_substr = False; ignore_case = False
    line = 'Thisisasentense'
    needle = 'SEN'
    bool_value = grep.find(regex, inverse, find_substr, ignore_case, needle, line)
    assert bool_value


def test_grep_find_find_substr_true():
    regex = False; inverse = False
    find_substr = True; ignore_case = False
    line = 'hello\n'
    needle = 'hello'
    bool_value = grep.find(regex, inverse, find_substr, ignore_case, needle, line)
    assert bool_value


def test_grep_find_find_substr_false():
    regex = False; inverse = False
    find_substr = True; ignore_case = False
    line = 'ollehhello\n'
    needle = 'hello'
    bool_value = grep.find(regex, inverse, find_substr, ignore_case, needle, line)
    assert not bool_value


def test_grep_find_ignore_case_true():
    regex = False; inverse = False
    find_substr = False; ignore_case = True
    line = '123HELLO123'
    needle = 'hello'
    bool_value = grep.find(regex, inverse, find_substr, ignore_case, needle, line)
    assert bool_value


def test_grep_find_ignore_case_false():
    regex = False; inverse = False
    find_substr = False; ignore_case = True
    line = 'HELLO'
    needle = 'hello'
    bool_value = grep.find(regex, inverse, find_substr, ignore_case, needle, line)
    assert bool_value


def test_grep_find_ignore_case_find_substr_true():
    regex = False; inverse = False
    find_substr = True; ignore_case = True
    line = 'HELLO\n'
    needle = 'hello'
    bool_value = grep.find(regex, inverse, find_substr, ignore_case, needle, line)
    assert bool_value


def test_grep_find_ignore_case_find_substr_false():
    regex = False; inverse = False
    find_substr = True; ignore_case = True
    line = 'HELLO123\n'
    needle = 'hello'
    bool_value = grep.find(regex, inverse, find_substr, ignore_case, needle, line)
    assert not bool_value


def test_grep_find_inverse_find_substr_true():
    regex = False; inverse = True
    find_substr = True; ignore_case = False
    line = 'hello999\n'
    needle = 'hello'
    bool_value = grep.find(regex, inverse, find_substr, ignore_case, needle, line)
    assert bool_value


def test_grep_find_inverse_find_substr_false():
    regex = False; inverse = True
    find_substr = True; ignore_case = False
    line = 'hello\n'
    needle = 'hello'
    bool_value = grep.find(regex, inverse, find_substr, ignore_case, needle, line)
    assert not bool_value


def test_grep_find_inverse_ignore_case():
    regex = False; inverse = True
    find_substr = False; ignore_case = True
    line = 'hello'
    needle = 'HELLo'
    bool_value = grep.find(regex, inverse, find_substr, ignore_case, needle, line)
    assert not bool_value


def test_grep_create_parser():
    args_str = ['-c', 'privet', 'a.txt']
    args = grep.create_parser(args_str)
    assert args.count
    assert not args.regex
    assert args.needle == 'privet'
    assert args.files == ['a.txt']


def test_grep_find_regex_true():
    regex = True; inverse = False
    find_substr = False; ignore_case = False
    needle = r'\d{2}'
    line = 'hello34bye'
    bool_value = grep.find(regex, inverse, find_substr, ignore_case, needle, line)
    assert bool_value


def test_grep_find_regex_false():
    regex = True; inverse = False
    find_substr = False; ignore_case = False
    needle = r'\d{2}'
    line = 'helloalohabye'
    bool_value = grep.find(regex, inverse, find_substr, ignore_case, needle, line)
    assert not bool_value


def test_grep_find_regex_inverse_true():
    regex = True; inverse = True
    find_substr = False; ignore_case = False
    needle = r'\d{2}'
    line = 'helloalohabye'
    bool_value = grep.find(regex, inverse, find_substr, ignore_case, needle, line)
    assert bool_value


def test_grep_find_regex_inverse_false():
    regex = True; inverse = True
    find_substr = False; ignore_case = False
    needle = r'\d{2}'
    line = 'hello34bye'
    bool_value = grep.find(regex, inverse, find_substr, ignore_case, needle, line)
    assert not bool_value


def test_grep_find_regex_find_substr_true():
    regex = True; inverse = False
    find_substr = True; ignore_case = False
    needle = r'\d{2}'
    line = '34'
    bool_value = grep.find(regex, inverse, find_substr, ignore_case, needle, line)
    assert bool_value


def test_grep_find_regex_find_substr_false():
    regex = True; inverse = False
    find_substr = True; ignore_case = False
    needle = r'\d{2}'
    line = 'wow34wow'
    bool_value = grep.find(regex, inverse, find_substr, ignore_case, needle, line)
    assert not bool_value


def test_grep_print_list(capsys):
    list_of_lines = ['line1', 'line2', 'line3']
    grep.print_list(list_of_lines)
    out, err = capsys.readouterr()
    assert out == 'line1\nline2\nline3\n'
    assert err == ''


def test_grep_print_list_one(capsys):
    list_of_lines = ['line1', 'line2', 'line3']
    prefix = ''
    grep.print_list(list_of_lines, prefix)
    out, err = capsys.readouterr()
    assert out == 'line1\nline2\nline3\n'
    assert err == ''


def test_grep_print_list_num(capsys):
    list_of_lines = ['line1', 'line2', 'line3']
    file_name = 'a.txt'
    prefix = file_name + ':'
    grep.print_list(list_of_lines, prefix)
    out, err = capsys.readouterr()
    assert out == 'a.txt:line1\na.txt:line2\na.txt:line3\n'
    assert err == ''


def test_grep_print_list_count(capsys):
    list_of_lines = ['line1', 'line2', 'line3']
    grep.print_list_count(list_of_lines)
    out, err = capsys.readouterr()
    assert out == '3\n'
    assert err == ''


def test_grep_print_list_count_one(capsys):
    list_of_lines = ['line1', 'line2', 'line3']
    prefix = ''
    grep.print_list_count(list_of_lines, prefix)
    out, err = capsys.readouterr()
    assert out == '3\n'
    assert err == ''


def test_grep_print_list_count_num(capsys):
    list_of_lines = ['line1', 'line2', 'line3']
    prefix = 'a.txt:'
    grep.print_list_count(list_of_lines, prefix)
    out, err = capsys.readouterr()
    assert out == 'a.txt:3\n'
    assert err == ''
