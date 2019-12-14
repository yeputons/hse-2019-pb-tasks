#!/usr/bin/env python3
import re
import io
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


def test_integrate_keys_case1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-Ecvx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:3\na.txt:3\n'


def test_integrate_keys_ivlx(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-ivlx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_integrade_do_only_not_files_issue(tmp_path, monkeypatch, capsys):
    (tmp_path / '1.txt').write_text('pattern\npattern\npattern')
    (tmp_path / '2.txt').write_text('pattern\npattern\nnot one more :)')
    (tmp_path / '3.txt').write_text('no needles here!\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-L', 'pattern', '1.txt', '2.txt', '3.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3.txt\n'


def test_integrate_keys_ci_stdin(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'TrolololoL\nroleorlf\nlaloLall))'))
    grep.main(['loL', '-c', '-i'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_stdin_regex_grep_count(monkeypatch, capsys):
    monkeypatch.setattr(
        'sys.stdin',
        io.StringIO('pref needle\nneedle suf\nthe needl\npref needl suf'))
    grep.main(['-c', '-E', 'ne*dle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


def test_integrate_keys_i_check_letter_cases(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('Trolololo\ntrololo!\ntRolol!\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', 'tr', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Trolololo\ntrololo!\ntRolol!\n'


def test_print_result_with_filename(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    grep.print_result(['a.txt:1', 'b.txt:2'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:1\nb.txt:2\n'


def test_print_result_without_filename(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    grep.print_result(['1'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_compile_pattern_with_regex():
    assert grep.compile_pattern('a+3?', is_regex=True, ignore_mode=False) == re.compile('a+3?')


def test_compile_pattern_without_regex():
    assert grep.compile_pattern('a*3?', is_regex=False, ignore_mode=False) == re.compile('a\\*3\\?')


def test_compile_pattern_with_ignore():
    assert grep.compile_pattern('A*3?', is_regex=False,
                                ignore_mode=True) == re.compile('A\\*3\\?', re.IGNORECASE)


def test_filter_lines_ix():
    lines = ['ABC?', 'abc?', 'AbC', 'ab', 'c', 'abC??']
    pattern = re.compile(re.escape('abc'), flags=re.IGNORECASE)
    assert grep.filter_lines(pattern, lines, False, True) == ['ab', 'c']


def test_filter_lines_v_regex():
    lines = ['ABC?', 'abc?', 'AbC', 'ab', 'c', 'abC??']
    pattern = re.compile('ab?')
    assert grep.filter_lines(pattern, lines, True, False) == ['ab']
