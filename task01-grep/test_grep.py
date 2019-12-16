#!/usr/bin/env python3
import io
import grep


def test_integrate_stdin_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_integrate_stdin_regex_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_integrate_stdin_grep_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_stdin_grep_regex_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-E', '-c', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_integrate_file_regex_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle?', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'the needl\npref needle suf\n'


def test_integrate_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_integrate_files_regex_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle?', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:the needl\nb.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_integrate_files_grep_regex_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'needle?', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:2\na.txt:2\n'


def test_integrate_file_regex_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '-c', 'needle?', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_file_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_integrate_files_grep_regex_count_error(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'needle?', 'b.txt', 'a.txt', 'keklol'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'File keklol does not exist\nb.txt:2\na.txt:2\n'


def test_what_to_return(tmp_path, monkeypatch, capsys):
    grep.what_to_return(['test1', 'test2'], 'test', True, False,
                   False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'test1\ntest2\n'


def test_run_all_count(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.run_all(io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'),
         False, True, False, False, False, False, False,
          True, 'needle?', '')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_run_all_regex_count(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.run_all(io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'),
         True, True, False, False, False, False, False,
          True, 'needle?', '')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


def test_run_all_regex(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.run_all(io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'),
         True, False, False, False, False, False, False,
          True, 'needle?', '')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_run_all(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.run_all(io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'),
         False, False, False, False, False, False, False,
          True, 'needle?', '')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_print_count(tmp_path, monkeypatch, capsys):
    grep.print_count(6, '', True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '6\n'


def test_print_count_file(tmp_path, monkeypatch, capsys):
    grep.print_count(6, 'kek.txt', False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'kek.txt:6\n'


def test_print_result(tmp_path, monkeypatch, capsys):
    grep.print_result(['lol','kek'], 'test', False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'test:lol\ntest:kek\n'


assert(grep.choosing_type_of_search(True, False, False,
                        'test', 'test')== True)


assert(grep.choosing_type_of_search(True, False, False,
                        'test1', 'test')== False)


assert(grep.choosing_type_of_search(True, True, False,
                        'test', 'test')== True)


assert(grep.choosing_type_of_search(True, True, False,
                        'test1', 'test')== False)

