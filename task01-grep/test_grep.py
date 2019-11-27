#!/usr/bin/env python3
import io
import grep


def test_integrate_grep_stdin(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'one two\ntwo? one\nthe once'))
    grep.main(['one'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'one two\ntwo? one\n'


def test_integrate_grep_stdin__reg(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'one1 two\ntwo? one\nthe once2'))
    grep.main(['-E', '[0-9]+'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'one1 two\nthe once2\n'


def test_integrate_grep_stdin_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'one two\ntwo? one\nthe once'))
    grep.main(['one', '-c'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_grep_stdin_reg_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'one1 two\ntwo? one\nthe once2'))
    grep.main(['-E', '[0-9]+', '-c'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_grep_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('one two\ntwo? one\nthe once')
    monkeypatch.chdir(tmp_path)
    grep.main(['one', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'one two\ntwo? one\n'


def test_integrate_grep_file_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('one two\ntwo? one\nthe once')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'one', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_grep_file_reg(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('one1 two\ntwo? one\nthe once24')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '[0-9]+', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'one1 two\nthe once24\n'


def test_integrate_grep_file_reg_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('one1 two\ntwo? one\nthe once24')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '-c', '[0-9]+', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_grep_two_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('one two\ntwo? one\nthe once')
    (tmp_path / 'b.txt').write_text('two\none, two\nonly once')
    monkeypatch.chdir(tmp_path)
    grep.main(['one', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:one two\na.txt:two? one\nb.txt:one, two\n'


def test_integrate_grep_two_files_reg(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('one two2\ntwo2 one\nthe once')
    (tmp_path / 'b.txt').write_text('two\none, two\nonly once4')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '[0-9]', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:one two2\na.txt:two2 one\nb.txt:only once4\n'


def test_integrate_grep_two_files_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('one two\ntwo? one\nthe once')
    (tmp_path / 'b.txt').write_text('two\none, two\nonly once')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'one', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\nb.txt:1\n'


def test_integrate_grep_two_files_reg_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('one two2\ntwo2 one\nthe once')
    (tmp_path / 'b.txt').write_text('two\none, two\nonly once4')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '-c', '[0-9]', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\nb.txt:1\n'


def test_integrate_grep_empty_files_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('one two\ntwo? one\nthe once')
    (tmp_path / 'b.txt').write_text('two\ntwo, two\nonly once')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'one', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\nb.txt:0\n'


def test_unit_write(capsys):
    grep.write(['a.txt'], False, {'a.txt': ['one', 'two']})
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'one\ntwo\n'


def test_unit_write_count(capsys):
    grep.write(['a.txt'], True, {'a.txt': ['one', 'two']})
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_unit_write_two_files_count(capsys):
    grep.write(['a.txt', 'b.txt'], True, {'a.txt': ['one', 'two'], 'b.txt': ['one']})
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\nb.txt:1\n'


def test_unit_write_two_files(capsys):
    grep.write(['a.txt', 'b.txt'], False, {'a.txt': ['one', 'two'], 'b.txt': ['one']})
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:one\na.txt:two\nb.txt:one\n'


def test_unit_find(tmpdir):
    a_file = tmpdir.join('a.txt')
    a_file.write('one two\ntwo? one\nonce')
    assert grep.find(False, 'one', a_file) == ['one two', 'two? one']


def test_unit_find_regex(tmpdir):
    a_file = tmpdir.join('a.txt')
    a_file.write('one two\ntwo? one\nonce')
    assert grep.find(True, 'o', a_file) == ['one two', 'two? one', 'once']


def test_unit_find_regex_sym(tmpdir):
    a_file = tmpdir.join('a.txt')
    a_file.write('one1 two\ntwo? one\nonce24')
    assert grep.find(True, '[0-9]+', a_file) == ['one1 two', 'once24']
