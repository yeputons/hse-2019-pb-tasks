from typing import List
import argparse as ap
import re
import io
import grep


def test_parse_args():
    args_str: List[str] = ['-c', '-Evx', 'needle', 'a.txt']
    args: ap.Namespace = grep.parse_args(args_str)
    assert args.count
    assert args.regex
    assert args.invert_mode
    assert args.full_match
    assert not args.ignore_case
    assert not args.only_files
    assert not args.only_files_invert
    assert args.pattern == 'needle'
    assert args.file_names == ['a.txt']


def test_strip_lines():
    data: List[str] = ['pref needle?\n', 'needle? suf\n', 'the needl\n', 'pref needle? suf']
    assert grep.strip_lines(data) == ['pref needle?', 'needle? suf',
                                      'the needl', 'pref needle? suf']


def test_compile_pattern_regex():
    assert grep.compile_pattern('h+i?', True, False) == re.compile('h+i?')


def test_compile_pattern_not_regex():
    assert grep.compile_pattern('h+i?', False, False) == re.compile('h\\+i\\?')


def test_compile_pattern_ignore_case():
    assert grep.compile_pattern('h+i?', False, True) == re.compile('h\\+i\\?', re.IGNORECASE)


def test_match_line_not_regex():
    line: str = 'ahhhe'
    assert not grep.match_line(re.compile(re.escape('h+i?')),
                               line, full_match=False, invert_mode=False)


def test_match_line_regex():
    line: str = 'ahhhe'
    assert grep.match_line(re.compile('h+i?'), line, full_match=False, invert_mode=False)


def test_match_line_invert():
    line: str = 'ahhhe'
    assert grep.match_line(re.compile(re.escape('h+i?')),
                           line, full_match=False, invert_mode=True)


def test_match_line_full_match():
    line: str = 'ahhhe'
    assert not grep.match_line(re.compile(re.escape('hh')),
                               line, full_match=True, invert_mode=False)


def test_match_line_ignore_case():
    line: str = 'aHhHe'
    assert grep.match_line(re.compile(re.escape('hh'), re.IGNORECASE),
                           line, full_match=False, invert_mode=False)


def test_match_lines_not_regex():
    data: List[str] = ['ahhhe', 'h+i?', 'qwerty', 'abid']
    assert grep.match_lines(re.compile(re.escape('h+i?')),
                            data, full_match=False, invert_mode=False) == ['h+i?']


def test_match_lines_regex():
    data: List[str] = ['ahhhe', 'h+i?', 'qwerty', 'abid']
    assert grep.match_lines(re.compile('h+i?'),
                            data, full_match=False, invert_mode=False) == ['ahhhe', 'h+i?']


def test_match_lines_invert():
    data: List[str] = ['ahhhe', 'h+i?', 'qwerty', 'abid']
    assert grep.match_lines(re.compile(re.escape('h+i?')),
                            data, full_match=False, invert_mode=True) == ['ahhhe', 'qwerty', 'abid']


def test_format_data_classic_mode_no_name():
    data: List[str] = ['string1', 'string2']
    assert grep.format_data(data, counting_mode=False,
                            only_files=False, only_files_invert=False) == ['string1', 'string2']


def test_format_data_classic_mode_with_source_name():
    data: List[str] = ['string1', 'string2']
    assert grep.format_data(data, counting_mode=False,
                            only_files=False, only_files_invert=False,
                            source_name='file.txt') == ['file.txt:string1', 'file.txt:string2']


def test_format_data_counting_mode_no_name():
    data: List[str] = ['string1', 'string2']
    assert grep.format_data(data, counting_mode=True,
                            only_files=False, only_files_invert=False) == ['2']


def test_format_data_counting_mode_with_source_name():
    data: List[str] = ['string1', 'string2']
    assert grep.format_data(data, counting_mode=True,
                            only_files=False, only_files_invert=False,
                            source_name='file.txt') == ['file.txt:2']


def test_format_data_files_mode():
    data: List[str] = ['string1', 'string2']
    assert grep.format_data(data, counting_mode=False, only_files_invert=False,
                            only_files=True, source_name='file.txt') == ['file.txt']


def test_format_data_files_invert_mode():
    data: List[str] = ['string1', 'string2']
    assert grep.format_data(data, counting_mode=False, only_files_invert=True,
                            only_files=False, source_name='file.txt') == []


def test_find_in_source():
    data: List[str] = ['pref needle?', 'needle? suf\n', 'the needl', 'pref needle? suf']
    assert grep.find_in_source(data, re.compile(re.escape('needle?')),
                               invert_mode=False, only_files_invert=False,
                               only_files=False, counting_mode=False, full_match=False,
                               source_name='test.txt') == ['test.txt:pref needle?',
                                                           'test.txt:needle? suf',
                                                           'test.txt:pref needle? suf']


def test_print_result(capsys):
    grep.print_result(['neadle', 'notneedle', 'filename:sometext'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'neadle\nnotneedle\nfilename:sometext\n'


def test_print_empty_result(capsys):
    grep.print_result([])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_integrate_file_grep_empty_result(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['neadle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


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


def test_integrate_multiple_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'test1.txt').write_text('pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    monkeypatch.chdir(tmp_path)
    (tmp_path / 'test2.txt').write_text('pre needle?\nneedle? '
                                        'suff\nthe needlll\npreff needle? suff')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'test1.txt', 'test2.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'test1.txt:pref needle?\ntest1.txt:needle? suf\ntest1.txt:pref needle? suf\n' \
                  'test2.txt:pre needle?\ntest2.txt:needle? suff\ntest2.txt:preff needle? suff\n'


def test_integrate_invert_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-v', 'needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'the needl\n'


def test_integrate_ignore_case_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('HeI\nHI\nHei\nqwerty')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', 'Hi', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'HI\n'


def test_integrate_full_match_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needle\nneedlee\nneadle\nneeedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-x', 'needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'needle\n'


def test_integrate_invert_full_match_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needle\nneedlee\nneadle\nneeedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-xv', 'needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'needlee\nneadle\nneeedle\n'


def test_integrate_full_match_file_mode_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needle\nneedlee\nneadle\nneeedle\n')
    (tmp_path / 'b.txt').write_text('')
    (tmp_path / 'c.txt').write_text('neeeeedlee\nneadle\nneeedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-lx', 'needle', 'a.txt', 'b.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_integrate_full_ignore_case_invert_mode_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('HEH\n')
    (tmp_path / 'b.txt').write_text('')
    (tmp_path / 'c.txt').write_text('HhH\nheH\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-Li', 'hH', 'a.txt', 'b.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nb.txt\n'


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


def test_integrate_all_keys_no_mode_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-ivx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:hello fo?o world\nb.txt:xfooyfoz\nb.txt:fooo\n'


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
