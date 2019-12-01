#!/usr/bin/env python3
import grep
import io


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


def test_integrate_not_regex_lix_keys_print_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('fo?o\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-lix', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_integrate_not_regex_civ_keys_count_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-civ', 'foo', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_integrate_not_regex_Lix_keys_print_not_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('fo?o\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-Lix', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_integrate_not_regex_cxv_keys_print_not_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('fo?o\nfoo\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-cxv', 'foo', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:2\na.txt:3\n'


def test_integrate_all_keys_count_files_grep_one_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-civx', '-E', 'fo?o', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_ivx_keys_files_grep_one_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-ivx', '-E', 'fo?o', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'hello fo?o world\nxfooyfoz\nfooo\n'


def test_integrate_ivx_keys_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('foko\nxfooyfoz\nfooo\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-ivx', '-E', 'fo.?o', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:xfooyfoz\nb.txt:hello fo?o world\nb.txt:xfooyfoz\n'


def test_integrate_stdin_grep_civx(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle\nthe needl\npref needle suf'))
    grep.main(['-civx', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_stdin_grep_ivx(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'needle\nneEDle suf\nneedle\npref needLe suf'))
    grep.main(['-vx', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'neEDle suf\npref needLe suf\n'


def test_integrate_ix_keys_files_grep_no_matches(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('foko\nxfooyfoz\nFOOOOOp\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-ix', 'abc.?.?.?', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_integrate_regex_i_keys_files_grep_no_matches(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('foko\nxlkjmnz\nFOOOOp\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', '-E', '.*g.*', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_integrate_regex_ci_keys_files_grep_no_matches(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('foko\nxlkjmnz\nFOOOOp\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-ci', '-E', '.*g.*', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:0\nb.txt:0\n'


def test_integrate_regex_ci_keys_file_grep_no_matches(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('zdrastvuite privet\nxlkjmnz\nFOOOOp\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-ci', '-E', '.*g.*', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '0\n'


def test_integrate_regex_civ_keys_files_grep_no_matches(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fogo\nxfaggomnz\nFOOOGp\n')
    (tmp_path / 'b.txt').write_text('hello fogo world\nxfogyfoz\nfogoo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-civ', '-E', '.*g.*', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:0\nb.txt:0\n'


def test_integrate_stdin_grep_civx_no_matches(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'needle\nneedle\nneedle\nneedle'))
    grep.main(['-civx', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '0\n'
