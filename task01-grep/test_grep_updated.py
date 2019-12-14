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


def test_create_needle_regex():
    assert grep.create_needle('^a.*$', True, False) == re.compile('^a.*$')


def test_create_needle_false():
    assert grep.create_needle('^a.*$', False, False) == re.compile('\\^a\\.\\*\\$')


def test_create_needle_register():
    assert grep.create_needle('^a.*$', False, True) == re.compile('\\^a\\.\\*\\$', re.IGNORECASE)


def test_format_print_length(capsys):
    grep.format_print(1, False, True, ['er', 'erfye', 'erfieri'], 'taatt.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_format_print_is_one(capsys):
    grep.format_print(2, True, False, ['er', 'erfye', 'erfieri'], 'taatt.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'taatt.txt\n'


def test_format_print_false(capsys):
    grep.format_print(2, False, False, ['er', 'erfye', 'erfieri'], 'taatt.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'taatt.txt:er\ntaatt.txt:erfye\ntaatt.txt:erfieri\n'


def test_integrate_key_big_l_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-L', '-E', 'fooo', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    print(out)
    assert err == ''
    assert out == 'a.txt\n'


def test_integrate_big_l_with_stdin(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'None \nnot files \ndsfa\n bar dsad asdf'))
    grep.main(['-L', 'None'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '\n'


def test_integrate_with_l_i_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('Session is coming\nAAAAAAA\nAAAAaa\nSeSSiOn iS CoMinG')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-li', 'Session is coming', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


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


def test_integrate_keys_ci_stdin(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'HeLoLoL\ntroOlOlo\nwhat the duck))'))
    grep.main(['loL', '-c', '-i'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


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
    (tmp_path / 'hey.txt').write_text('h?e?y?\nw?a*\nno*in?')
    monkeypatch.chdir(tmp_path)
    grep.main(['-L', 'hey', 'hey.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'hey.txt\n'
