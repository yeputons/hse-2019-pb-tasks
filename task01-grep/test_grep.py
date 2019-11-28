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


def test_integrate_stdin_regex_grep_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        '20/07/2001\nhi 5\n10/04/2007\n789/234234/23423'))
    grep.main(['-c', '-E', '[0-9]{2}/[0-9]{2}/[0-9]{4}'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_integrate_file_regex_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('75/what\n123\n239/what\n/what')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '[0-9]/what', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '75/what\n239/what\n'


def test_integrate_file_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('imok\nokokokhelp_me_plsokok\nhelp_me_how\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'help_me_pls', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_integrate_file_regex_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('my_mark-->4\nmy_mark-10\nmark-8\nm-5')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', '8|10|9', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_doublefile_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:pref needle suf\na.txt:pref needle suf\n'


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


def test_integrate_files_regex_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('thrpt\naaaa\npfff')
    (tmp_path / 'b.txt').write_text('ooooo\nkek\n\nmIT')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '[^aeyuoitTIAEYUOm]', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:kek\na.txt:thrpt\na.txt:pfff\n'


def test_integrate_files_regex_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('123.456\nstainalife\nneedle?')
    (tmp_path / 'b.txt').write_text('42.32\n532.234\n324.324\nmIT\n324.643')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', r'\d{3}.\d{3}', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:3\na.txt:1\n'


def test_parse_arguments():
    testing_parser = grep.parse_arguments(['-c', '-E', 'needline', 'file_1.txt', 'file_2.txt'])
    assert testing_parser.needle == 'needline'
    assert testing_parser.count
    assert testing_parser.regex
    assert testing_parser.files == ['file_1.txt', 'file_2.txt']


def test_print_output(capsys):
    grep.print_output(['kek', 'lol'], False, '')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'kek\nlol\n'


def test_print_output_count(capsys):
    grep.print_output(['kek', 'lol'], True, '')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_print_output_file(capsys):
    grep.print_output(['kek', 'lol'], False, 'a.txt:')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:kek\na.txt:lol\n'


def test_print_output_file_count(capsys):
    grep.print_output(['kek', 'lol'], True, 'a.txt:')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\n'


def test_create_ans_list():
    testing_list = grep.create_ans_list('love', ['All you', 'need is', 'love!'], False)
    assert testing_list == ['love!']


def test_create_ans_list_regex():
    testing_list = grep.create_ans_list(r'\d{2}/\d{2}/\d{4}',
                                        ['20/02/1991', 'w', '14/11/2019'],
                                        True)
    assert testing_list == ['20/02/1991', '14/11/2019']


def test_work_with_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fff yes!\nnot working\nfff')
    monkeypatch.chdir(tmp_path)
    grep.work_with_file('a.txt', '', 'ff', False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'fff yes!\nfff\n'
