#!/usr/bin/env python3
import grep


def test_integrate_regex_symbols(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('!!!.*.?!!!')
    (tmp_path / 'b.txt').write_text('aeouaeou')
    monkeypatch.chdir(tmp_path)
    grep.main(['.*.?', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:!!!.*.?!!!\n'


def test_integrate_empty_result(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('hihihi')
    (tmp_path / 'b.txt').write_text('byebyebye')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', 'a', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_integrate_empty_everything(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('')
    (tmp_path / 'b.txt').write_text('')
    monkeypatch.chdir(tmp_path)
    grep.main(['', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_integrate_empty_string(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('hi\nhi\n')
    (tmp_path / 'b.txt').write_text('bye')
    monkeypatch.chdir(tmp_path)
    grep.main(['', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:bye\na.txt:hi\na.txt:hi\n'


def test_integrate_ignorecase_exact(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('[fF]')
    (tmp_path / 'b.txt').write_text('f')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', '-x', '[fF]', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:[fF]\n'


def test_integrate_regex_count_invert(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fOa\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\nkek\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-cv', '-E', '[fF]', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:0\n'


def test_integrate_line_not_exists(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fOa\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-L', '-E', 'fO?a', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_integrate_all_keys_print_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-livx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_integrate_all_keys_print_not_files_grep(tmp_path, monkeypatch,
                                                 capsys):
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
