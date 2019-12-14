#!/usr/bin/env python3
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


def test_integrate_all_keys_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-ivx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:hello fo?o world\nb.txt:xfooyfoz\nb.txt:fooo\n'


def test_integrate_key_v_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-v', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:fO\na.txt:FO\na.txt:FoO\n'


def test_integrate_key_i_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:hello fo?o world\nb.txt:xfooyfoz\n' \
                  'b.txt:fooo\na.txt:fO\na.txt:FO\na.txt:FoO\n'


def test_integrate_key_x_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-x', '-E', 'fooo', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    print(out)
    assert err == ''
    assert out == 'b.txt:fooo\n'


def test_integrate_key_l_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-l', '-E', 'fooo', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    print(out)
    assert err == ''
    assert out == 'b.txt\n'


# ----------------------------------------------UNIT--------------------------------------


def test_compile_pattern():
    assert re.compile('a\\.', re.IGNORECASE) == grep.compile_pattern('a.', False, True)


def test_get_find_function():
    pattern = re.compile('ab')

    def f_test(line):
        return bool(re.fullmatch(pattern, line)) ^ 1

    f_correct = grep.get_find_function(pattern, True, True)
    assert f_test('a') == f_correct('b')


def test_filter_blocks():
    blocks = [['lol ke', 'lol'], ['kek']]
    pattern = re.compile('ke?')

    def f(line):
        return bool(re.search(pattern, line)) ^ 1

    assert grep.filter_blocks(blocks, f) == [['lol'], []]


def test_print_file_name_only(capsys):
    blocks = [['a', 'x'], ['b']]
    sources = ['1', '2']
    grep.print_file_name_only(zip(blocks, sources), True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n2\n'
