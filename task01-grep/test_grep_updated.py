#!/usr/bin/env python3
import io
import sys
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


def test_print_data_is_name(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    grep.print_data('I slept for 3 hours!!!', 'a.txt', True, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_matching_pattern_x_basic_false():
    assert grep.matching_pattern(False, True, False, 'Paradigms', 'Paradigms ss') is False


def test_matching_pattern_x_basic_true():
    assert grep.matching_pattern(False, True, False, 'Paradigms', 'Paradigms') is True


def test_matching_pattern_x_regex():
    assert grep.matching_pattern(True, True, False, 'Paradigm.', 'Paradigms') is True


def test_matching_pattern_i():
    assert grep.matching_pattern(False, False, True, 'paradigms', 'I love PaRaDiGmS (help)') is True


def test_matching_pattern_xi_false():
    assert grep.matching_pattern(False, True, True, 'pArAdigms', 'paradigms are hard') is False


def test_matching_pattern_xi_true():
    assert grep.matching_pattern(False, True, True, 'pArAdigms', 'paradigms') is True


def test_process_x(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'help\nI want\nto go\nto sleep\nto go to'))
    grep.process(sys.stdin, ' ', False, 'to go', True, False, True, False, False, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'to go\n'


def test_process_i(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needles\n afhfk suf\nneedle NeedLE bbb\n')
    (tmp_path / 'b.txt').write_text('the needling\npref needle suf')
    monkeypatch.chdir(tmp_path)
    with open('a.txt') as new:
        grep.process(new, 'a.txt', True, 'NeEdles?', True, False, False, True, False, False, False)
    with open('b.txt') as new:
        grep.process(new, 'b.txt', True, 'NeEdles?', True, False, False, True, False, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:pref needles\na.txt:needle NeedLE bbb\nb.txt:pref needle suf\n'


def test_process_v(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO('I want\nto go\nto sleep\nto GO to'))
    grep.process(sys.stdin, ' ', False, 'go', True, False, False, False, True, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'I want\nto sleep\nto GO to\n'


def test_process_x_big_l(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needles\nto go\nneedle needle bbb\n')
    (tmp_path / 'b.txt').write_text('the needling\npref needle suf')
    monkeypatch.chdir(tmp_path)
    with open('a.txt') as new:
        grep.process(new, 'a.txt', True, 'to go', False, False, True, False, False, False, True)
    with open('b.txt') as new:
        grep.process(new, 'b.txt', True, 'to go', False, False, True, False, False, False, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nb.txt\n'


def test_process_x_small_l(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needles\nto go\nneedle needle bbb\n')
    (tmp_path / 'b.txt').write_text('the needling\npref needle suf')
    monkeypatch.chdir(tmp_path)
    with open('a.txt') as new:
        grep.process(new, 'a.txt', True, 'to go', False, False, True, False, False, True, False)
    with open('b.txt') as new:
        grep.process(new, 'b.txt', True, 'to go', False, False, True, False, False, True, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_process_x_v(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needles\nto go\nTo go\n')
    (tmp_path / 'b.txt').write_text('paradigms\ngo to\nto go\n')
    monkeypatch.chdir(tmp_path)
    with open('a.txt') as new:
        grep.process(new, 'a.txt', True, 'to go', False, False, True, False, True, False, False)
    with open('b.txt') as new:
        grep.process(new, 'b.txt', True, 'to go', False, False, True, False, True, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:pref needles\na.txt:To go\nb.txt:paradigms\nb.txt:go to\n'


def test_process_x_v_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needles\nto go\nTo go\n')
    (tmp_path / 'b.txt').write_text('paradigms\ngo to\nto go\n')
    monkeypatch.chdir(tmp_path)
    with open('a.txt') as new:
        grep.process(new, 'a.txt', True, 'to go', False, True, True, False, True, False, False)
    with open('b.txt') as new:
        grep.process(new, 'b.txt', True, 'to go', False, True, True, False, True, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\nb.txt:2\n'
