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


def test_unit_parse_args_files_count_regex():
    parsed_args = grep.parse_args(['-c', '-E', 'date', 'text.txt', 'hw.tex'])
    assert parsed_args == grep.argparse.Namespace(count=True, files=['text.txt', 'hw.tex'],
                                                  pattern='date', regex=True)


def test_unit_parse_args_files_not_count_not_regex():
    parsed_args = grep.parse_args(['date', 'text.txt', 'hw.tex'])
    assert parsed_args == grep.argparse.Namespace(count=False, files=['text.txt', 'hw.tex'],
                                                  pattern='date', regex=False)


def test_unit_parse_args_no_files():
    parsed_args = grep.parse_args(['-E', 'date'])
    assert parsed_args == grep.argparse.Namespace(count=False, files=[],
                                                  pattern='date', regex=True)


def test_unit_filter_matched_lines_regex():
    lines = grep.filter_matched_lines(['b.cpp', 'a.c', 'mmmc'], '[a-z]+\\.cp*', True)
    assert lines == ['b.cpp', 'a.c']


def test_unit_filter_matched_lines_not_regex():
    lines = grep.filter_matched_lines(['hello world', 'CGSG_FOREVER_30', 'DF5'], 'F', False)
    assert lines == ['CGSG_FOREVER_30', 'DF5']


def test_unit_count_lines_with_pattern_regex():
    cnt = grep.count_lines_with_pattern(['b.cpp', 'a.c', 'mmmc'], '[a-z]+\\.cp*', True)
    assert cnt == 2


def test_unit_count_lines_with_pattern_not_regex():
    cnt = grep.count_lines_with_pattern(['hello world', 'CGSG_FOREVER_30', 'DF5'], 'F', False)
    assert cnt == 2


def test_unit_find_lines_from_grep_not_regex_not_count():
    parsed_args = grep.parse_args(['needle?'])
    lines = grep.find_lines_from_grep(['pref needle?', 'needle? suf', 'the needl',
                                       'pref needle? suf'], parsed_args.pattern,
                                      parsed_args.regex, parsed_args.count)
    assert lines == ['pref needle?', 'needle? suf', 'pref needle? suf']


def test_unit_find_lines_from_grep_regex_count():
    parsed_args = grep.parse_args(['-c', 'needle?', '-E'])
    result = grep.find_lines_from_grep(['pref needle?', 'needle? suf',
                                        'the needl', 'pref needle? suf'], parsed_args.pattern,
                                       parsed_args.regex, parsed_args.count)
    assert result == [4]
