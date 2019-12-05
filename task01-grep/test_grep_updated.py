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


def test_unit_filter_matching_lines():
    input_ = ['test', 'test', 'also test', 'tes', 'list end']
    result = grep.filter_matching_lines(re.compile(re.escape('test')), input_)
    assert result == ['test', 'test', 'also test']


def test_unit_print_lines(capsys):
    input_ = ['Print it', 'Print it too', '\n']
    grep.print_lines(input_)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Print it\n' \
                  'Print it too\n' \
                  '\n' \
                  '\n'


def test_unit_build_pattern():
    result = grep.build_pattern('fo?o', is_regex=True, is_full_match=True)
    assert result == re.compile('^fo?o$')


def test_unit_rstrip_lines():
    lines = ['begin? \n middle end?', '\n\n\n\n\n\n\n', '', 'pref\n', '\ntext...text\t']
    lines = grep.rstrip_lines(lines, '\n')
    assert lines == ['begin? \n middle end?', '', '', 'pref', '\ntext...text\t']


def test_unit_count_lines():
    lines = [['first', '2th', 'third'], [], [], ['word']]
    lines = grep.count_lines(lines)
    assert lines == [3, 0, 0, 1]


def test_unit_add_prefix():
    lines = [' <- prefix', 'The str need a prefix', '']
    prefix = 'title'
    lines = grep.add_prefix(prefix, lines, chars_between=')')
    assert lines == ['title) <- prefix', 'title)The str need a prefix', 'title)']


def test_unit_get_difference():
    first = ['alone', '', 1, 2, 3, True, '...']
    second = ['', '', 10, 2, 3, False, True, '3 dots']
    assert grep.get_difference(first, second) == ['alone', 1, '...']


def test_unit_get_difference_empty():
    first = []
    second = []
    assert grep.get_difference(first, second) == []


def test_integrate_with_l_i_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('Session is coming\nAAAAAAA\nAAAAaa\nSeSSiOn iS CoMinG')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-li', 'Session is coming', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_integrate_with_vcx_regex_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('1\n1\n2\n3\n5\n8\n13\n21\n34')
    (tmp_path / 'b.txt').write_text('1\n1\n2\n5\n14\n42\n132')
    monkeypatch.chdir(tmp_path)
    grep.main(['-vcx', '-E', '5', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:6\na.txt:8\n'


def test_integrate_with_vix_regex_stdin(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'hi\nHeLo\nHelllllo\nHwerqllo\nH e l l o\nheHIlO'))
    grep.main(['-vcx', '-E', 'He?Lo'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '5\n'


def test_integrate_big_l_with_stdin(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'None \nnot files \ndsfa\n bar dsad asdf'))
    grep.main(['-L', 'None'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'None \n'


def test_integrate_empty_stdin(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        ''))
    grep.main(['-vxi', 'EMPTY'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
