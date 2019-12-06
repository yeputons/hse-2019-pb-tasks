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


def test_integrate_atleast_one_line(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\noOoOoOo\n')
    (tmp_path / 'b.txt').write_text('hello world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-lix', 'oOoOoOo', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_integrate_ixv(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('p\npp\npppp\n')
    (tmp_path / 'b.txt').write_text('ooo\noo\no\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-ixv', 'pp', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:ooo\nb.txt:oo\nb.txt:o\na.txt:p\na.txt:pppp\n'


def test_integrate_(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('p\npp\npppp\n')
    (tmp_path / 'b.txt').write_text('ooo\noo\no\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-vc', 'pp', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:3\na.txt:1\n'


def test_unit_check_pattern():
    check = grep.check_pattern('enchantment?!!', 'enchantment?', False, True)
    assert (check is True)


def test_unit_print(capsys):
    grep.print_out_result(['listentotheqwindvlow', 'ridingintheshdowrs'], True, False, False, False, 'chain.txt', 2)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'
