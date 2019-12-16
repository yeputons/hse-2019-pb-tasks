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


def test_integrate_not_found_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'c.txt', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == 'c.txt:not found\n'
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


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


def test_unit_parse_args_files_count_regex():
    parsed_args = grep.parse_args(['-c', '-E', 'date', 'text.txt', 'hw.tex'])
    assert parsed_args.count
    assert parsed_args.files == ['text.txt', 'hw.tex']
    assert parsed_args.pattern == 'date'
    assert parsed_args.regex


def test_unit_parse_args_files_not_count_not_regex():
    parsed_args = grep.parse_args(['date', 'text.txt', 'hw.tex'])
    assert not parsed_args.count
    assert parsed_args.files == ['text.txt', 'hw.tex']
    assert parsed_args.pattern == 'date'
    assert not parsed_args.regex


def test_unit_parse_args_no_files():
    parsed_args = grep.parse_args(['-E', 'date'])
    assert not parsed_args.count
    assert parsed_args.files == []
    assert parsed_args.pattern == 'date'
    assert parsed_args.regex


def test_unit_filter_matched_lines_regex():
    lines = grep.filter_matched_lines(['b.cpp', 'a.c', 'mmmc'],
                                      grep.compile_pattern('[a-z]+\\.cp*', is_pattern_regex=True))
    assert lines == ['b.cpp', 'a.c']


def test_unit_filter_matched_lines_not_regex():
    lines = grep.filter_matched_lines(['hello world', 'CGSG_FOREVER_30', 'DF5'],
                                      grep.compile_pattern('F'))
    assert lines == ['CGSG_FOREVER_30', 'DF5']
