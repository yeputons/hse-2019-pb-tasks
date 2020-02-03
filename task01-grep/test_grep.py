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


def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_integrate_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_integrate_files_grep_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_integrate_file_grep_regex_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '-c', 'needle', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_integrate_stdin_grep_regex_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-E', '-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_file_grep_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_substr_search_0():
    assert grep.substr_search('needle', 'pref needle suf', False, False) is True


def test_substr_search_1():
    assert grep.substr_search('needle', 'pref NeEdLe suf', True, False) is True


def test_substr_search_2():
    assert grep.substr_search('needle', 'pref needle suf', False, True) is False


def test_substr_search_3():
    assert grep.substr_search('needle', 'NEEdle', True, True) is True


def test_parse_lines():
    assert grep.parse_lines(['line 1\n', 'line 2\n']) == ['line 1', 'line 2']


def test_match_string():
    assert grep.match_string('needle', 'pref NeEdlEsuf', False, True, False, False) is True


def test_read_files(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    assert grep.read_files(['a.txt', 'b.txt']) == {'a.txt': ['pref needle', 'needle suf'],
                                                   'b.txt': ['the needl', 'pref needle suf']}


def test_read_stdin(monkeypatch):
    monkeypatch.setattr('sys.stdin',
                        io.StringIO('pref needle\nneedle suf\nthe needl\npref needle suf'))
    assert grep.read_stdin() == {'': ['pref needle', 'needle suf',
                                      'the needl', 'pref needle suf']}


def test_filter_lines():
    lines = {'a.txt': ['NeEdLe line', 'NeedlE'],
             'b.txt': ['needle', 'kek'],
             'c.txt': ['yjturklhgjn;', 'kkkk']}
    assert grep.filter_lines(lines, 'needle',
                             False, True, True, True) == {'a.txt': ['NeEdLe line'],
                                                          'b.txt': ['kek'],
                                                          'c.txt': ['yjturklhgjn;', 'kkkk']}


def test_print_answer_count(capsys):
    filtered_lines = {'a.txt': ['NeEdLe line'],
                      'b.txt': ['kek'],
                      'c.txt': ['yjturklhgjn;', 'kkkk']}
    grep.print_answer_count(filtered_lines)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:1\nb.txt:1\nc.txt:2\n'


def test_print_answer_files_only(capsys):
    filtered_lines = {'a.txt': [''],
                      'b.txt': [],
                      'c.txt': ['', 'asdfad', '12341234'],
                      'd.txt': []}
    grep.print_answer_files_only(filtered_lines, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\nd.txt\n'


def test_print_answer_default_0(capsys):
    filtered_lines = {'a.txt': ['NeEdLe line'],
                      'b.txt': ['kek'],
                      'c.txt': ['yjturklhgjn;', 'kkkk']}
    grep.print_answer_default(filtered_lines)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:NeEdLe line\nb.txt:kek\nc.txt:yjturklhgjn;\nc.txt:kkkk\n'


def test_print_answer_default_1(capsys):
    filtered_lines = {'': ['filtered line', 'filtered line 2']}
    grep.print_answer_default(filtered_lines)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'filtered line\nfiltered line 2\n'


def test_print_answer_0(capsys):
    filtered_lines = {'a.txt': ['NeEdLe line'],
                      'b.txt': ['kek'],
                      'c.txt': ['yjturklhgjn;', 'kkkk']}
    grep.print_answer(filtered_lines, True, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:1\nb.txt:1\nc.txt:2\n'


def test_print_answer_1(capsys):
    filtered_lines = {'a.txt': ['NeEdLe line'],
                      'b.txt': ['kek'],
                      'c.txt': ['yjturklhgjn;', 'kkkk']}
    grep.print_answer(filtered_lines, False, True, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nb.txt\nc.txt\n'


def test_print_answer_2(capsys):
    filtered_lines = {'a.txt': [''],
                      'b.txt': [],
                      'c.txt': ['yjturklhgjn;', 'kkkk']}
    grep.print_answer(filtered_lines, False, False, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_print_answer_3(capsys):
    filtered_lines = {'a.txt': ['NeEdLe line'],
                      'b.txt': [],
                      'c.txt': ['yjturklhgjn;', 'kkkk']}
    grep.print_answer(filtered_lines, False, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:NeEdLe line\nc.txt:yjturklhgjn;\nc.txt:kkkk\n'
