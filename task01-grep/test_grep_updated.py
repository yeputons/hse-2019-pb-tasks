#!/usr/bin/env python3
import io
import re
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


def test_integrate_keys_ci_stdin(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'HeLoLoL\ntroOlOlo\nwhat the duck))'))
    grep.main(['loL', '-c', '-i'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_keys_liv_and_nonexistent_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text("Hey, I'm so tired, I wanna die\nI'm working on\n")
    (tmp_path / 'b.txt').write_text('nothing interesting\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', '-v', '-l', "i'M", 'a.txt', 'b.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == 'No such file: c.txt\n'
    assert out == 'b.txt\n'


def test_integrate_keys_i_check_letter_cases(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('Hello\nHey!\nhEy!\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', 'he', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Hello\nHey!\nhEy!\n'


def test_integrate_empty_output(tmp_path, monkeypatch, capsys):
    (tmp_path / 'hey.dot').write_text('h?e?y?\nw?a*\nno*in?')
    monkeypatch.chdir(tmp_path)
    grep.main(['-l', 'hey', 'hey.dot'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_integrate_not_empty_because_flag_big_l(tmp_path, monkeypatch, capsys):
    (tmp_path / 'hey.dot').write_text('h?e?y?\nw?a*\nno*in?')
    monkeypatch.chdir(tmp_path)
    grep.main(['-L', 'hey', 'hey.dot'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'hey.dot\n'


def test_unit_filter_line_xv_regex():
    searcher = re.compile('going?', flags=re.IGNORECASE)
    matched_false = grep.filter_line('goin', True, True, searcher)
    matched_true = grep.filter_line('I am going', True, True, searcher)
    assert not matched_false and matched_true


def test_unit_filter_lines_ix():
    lines = ['go?', 'Go?', 'go!', 'g', 'going', 'go??']
    matched_lines = grep.filter_lines(lines, 'go?', False, False, True, True)
    assert matched_lines == ['go?', 'Go?']


def test_unit_filter_lines_v_regex():
    lines = ['go?', 'Go?', 'go!', 'g', 'going', 'go??']
    matched_lines = grep.filter_lines(lines, 'go?', True, True, False, False)
    assert matched_lines == ['Go?']


def test_unit_prepare_output_with_file_name():
    lines = ['Mom will be proud of me!', 'I am going to be famous', 'I am going to be printed!!!']
    output = grep.prepare_output(lines, 'me.lol', False, False, False)
    assert output == ['me.lol:Mom will be proud of me!',
                      'me.lol:I am going to be famous',
                      'me.lol:I am going to be printed!!!']


def test_unit_prepare_output_without_file_name():
    lines = ['Mom will be proud of me!', 'I am going to be famous', 'I am going to be printed!!!']
    output = grep.prepare_output(lines, None, False, False, False)
    assert output == ['Mom will be proud of me!',
                      'I am going to be famous',
                      'I am going to be printed!!!']


def test_unit_prepare_output_count():
    lines = ['Mom will be proud of me!', 'I am going to be famous', 'I am going to be printed!!!']
    output = grep.prepare_output(lines, 'me.lol', True, False, False)
    assert output == ['me.lol:3']


def test_unit_prepare_output_only_files():
    lines = ['Mom will be proud of me!', 'I am going to be famous', 'I am going to be printed!!!']
    output = grep.prepare_output(lines, 'me.lol', False, True, False)
    assert output == ['me.lol']


def test_unit_prepare_output_only_not_files():
    lines = ['Mom will be proud of me!', 'I am going to be famous', 'I am going to be printed!!!']
    output = grep.prepare_output(lines, 'me.lol', False, False, True)
    assert output == []


def test_unit_parse_arguments():
    args = grep.parse_arguments(['i am so tired', 'a.txt', '-livx'])
    assert args.pattern == 'i am so tired'
    assert not args.regex
    assert not args.counting
    assert not args.only_not_files
    assert args.files == ['a.txt']
    assert args.only_files
    assert args.invert
    assert args.ignore
    assert args.fullmatch
