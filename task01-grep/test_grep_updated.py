#!/usr/bin/env python3
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


def test_integrate_all_keys_count_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-civx', '-E', 'fo?o', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_all_keys_print_files_grep__str(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-livx', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\na.txt\n'


def test_integrate_all_keys_print_not_files_grep__str(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-Livx', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_integrate_all_keys_count_files_grep__str(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-civx', 'fo', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:3\na.txt:1\n'


def test_integrate_all_keys_count_file_grep__str(tmp_path, monkeypatch, capsys):
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-civx', 'fooo', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_all_keys_stdin__str(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'hello fo?o world\nxfooyfoz\nfooo\n'))
    grep.main(['-ivx', 'fooo'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'hello fo?o world\nxfooyfoz\n'


def test_integrate_all_keys_count__stdin__str(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'hello fo?o world\nxfooyfoz\nfooo\n'))
    grep.main(['-civx', 'fooo'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_all_keys_stdin(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'hello fo?o world\nxfooyfoz\nfooo\n'))
    grep.main(['-ivx', '-E', 'fo?o'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'hello fo?o world\nxfooyfoz\nfooo\n'


def test_integrate_all_keys_count__stdin(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'hello fo?o world\nxfooyfoz\nfooo\n'))
    grep.main(['-civx', '-E', 'fo?o'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_unit_find_regex__ignore():
    args = grep.parse(['-i', '-E', 'fo?o'])
    assert grep.find_regex(args, 'Foo')


def test_unit_find_regex():
    args = grep.parse(['-E', 'fo?o'])
    assert not grep.find_regex(args, 'Foo')


def test_unit_find_regex_fullmatch():
    args = grep.parse(['-x', '-E', 'fo?o'])
    assert not grep.find_regex(args, 'food')


def test_unit_find_str__ignore():
    args = grep.parse(['-i', 'foo'])
    assert grep.find_str(args, 'Food')


def test_unit_find_str():
    args = grep.parse(['foo'])
    assert not grep.find_str(args, 'Food')


def test_unit_find_str__fullmatch_true():
    args = grep.parse(['-x', 'foo'])
    assert not grep.find_str(args, 'food')


def test_unit_find_str__fullmatch_false():
    args = grep.parse(['-x', 'food'])
    assert grep.find_str(args, 'food')


def test_unit_find_lines_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    args = grep.parse(['-livx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    with open('b.txt', 'r') as in_file:
        grep.find_lines(args, in_file, 'b.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_unit_find_lines_not_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    args = grep.parse(['-Livx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    args.ans = not args.ans
    args.inverse = not args.inverse
    with open('b.txt', 'r') as in_file:
        grep.find_lines(args, in_file, 'b.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_unit_find_lines_count_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    args = grep.parse(['-civx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    with open('b.txt', 'r') as in_file:
        grep.find_lines(args, in_file, 'b.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:3\n'


def test_unit_print_lines_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    args = grep.parse(['-livx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    grep.print_lines(['hello fo?o world', 'xfooyfoz'], args, 'b.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_unit_print_lines_files_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    args = grep.parse(['-civx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    grep.print_lines(['hello fo?o world', 'xfooyfoz'], args, 'b.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:2\n'


def test_unit_print_lines(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    args = grep.parse(['-ivx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    grep.print_lines(['hello fo?o world', 'xfooyfoz'], args, 'b.txt')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:hello fo?o world\nb.txt:xfooyfoz\n'
