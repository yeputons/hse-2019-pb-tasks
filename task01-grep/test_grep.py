#!/usr/bin/env python3
import io
import grep


def test_normal_search():
    assert grep.single_grep('i', ['hi'], grep.normal_search) == ['hi']
    assert grep.single_grep('i', ['hi'], grep.normal_search) == ['hi']
    assert grep.single_grep('i', ['hi', 'hi'],
                            grep.normal_search) == ['hi', 'hi']
    assert grep.single_grep('a', [''], grep.normal_search) == []


def test_regex_search():
    assert grep.single_grep('i', ['hi'], grep.regex_search) == ['hi']
    assert grep.single_grep('i', ['hi'], grep.regex_search) == ['hi']
    assert grep.single_grep('i', ['hi', 'hi'],
                            grep.regex_search) == ['hi', 'hi']
    assert grep.single_grep('a', [''],
                            grep.regex_search) == []  # File has 0 lines
    assert grep.single_grep('.*', [''],
                            grep.regex_search) == ['']  # File has 0 lines
    assert grep.single_grep('.*', [' '],
                            grep.regex_search) == [' ']  # File has 1 line
    assert grep.single_grep('.*', ['hi'], grep.regex_search) == ['hi']


def test_single_grep():
    def search_hi(_, y):
        return 'hi' in y

    assert grep.single_grep('unused', ['hihihi', 'hihi', 'hi', 'hhhh'],
                            search_hi) == ['hihihi', 'hihi', 'hi']
    assert grep.single_grep('unused', ['', ''], search_hi) == []

    assert grep.single_grep('x', ['xa', 'xxx', 'xxy'],
                            lambda x, y: x in y) == ['xa', 'xxx', 'xxy']


def test_read_input(monkeypatch, tmp_path):
    parser = grep.create_parser()

    args = parser.parse_args(['needle'])
    monkeypatch.setattr(
        'sys.stdin',
        io.StringIO('pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    assert grep.read_input(args) == [[
        'pref needle?', 'needle? suf', 'the needl', 'pref needle? suf'
    ]]

    args = parser.parse_args(['needle', 'a.txt'])
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    assert grep.read_input(args) == [['pref needle', 'needle suf']]

    args = parser.parse_args(['needle', 'a.txt', 'b.txt'])
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    assert grep.read_input(args) == [['pref needle', 'needle suf'],
                                     ['the needl', 'pref needle suf']]


def test_create_parser():
    parser = grep.create_parser()

    args = parser.parse_args(['needle'])
    assert args.needle == 'needle'
    assert not args.files
    assert not args.count
    assert not args.regex

    args = parser.parse_args(['-E', 'needle', 'a', 'b', 'c', '-c'])
    assert args.needle == 'needle'
    assert args.files == ['a', 'b', 'c']
    assert args.count
    assert args.regex


def test_print_answers(capsys):
    parser = grep.create_parser()

    grep.print_answers([['hi', 'bye']], parser.parse_args(['needle']))
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'hi\nbye\n'

    grep.print_answers([['hi', 'bye']], parser.parse_args(['needle', 'file1']))
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'hi\nbye\n'

    grep.print_answers([['aa'], ['bb']],
                       parser.parse_args(['needle', 'file1', 'file2']))
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'file1:aa\nfile2:bb\n'

    grep.print_answers([[], ['bb']],
                       parser.parse_args(['needle', 'file1', 'file2']))
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'file2:bb\n'


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
