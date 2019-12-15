import io
import re
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


def test_integrate_files_regex_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('ahaha\natata\n')
    (tmp_path / 'b.txt').write_text('aloha\naaaaa')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'a+a+a', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:0\n'


def test_unit_filter_strings_by_pattern_with_cond():
    pattern = 'a?lex?'
    pattern = re.compile(pattern)
    data = [['alex', '?', 'alex?', '????alex', 'ale', 'le'],
            ['alex?', 'ale', 'alex', 'ale'],
            ['hello'],
            ['alx?', '?alex?', '?ale', 'lex']]
    inverse = False
    full = False
    ans = grep.filter_strings_by_pattern(pattern, data, inverse, full)
    assert ans == [['alex', 'alex?', '????alex', 'ale', 'le'],
                   ['alex?', 'ale', 'alex', 'ale'],
                   [],
                   ['?alex?', '?ale', 'lex']]
    pattern = 'a+b*a?'
    pattern = re.compile(pattern)
    data = [['a', '', 'aa'],
            ['aaaaba'],
            ['hehe'],
            ['abba', 'aba'],
            ['aaaaaa', 'baa']]
    inverse = True
    full = False
    ans = grep.filter_strings_by_pattern(pattern, data, inverse, full)
    assert ans == [[''],
                   [],
                   ['hehe'],
                   [],
                   []]
    pattern = 'a?'
    pattern = re.compile(re.escape(pattern))
    data = [['a', 'aa'],
            ['a?', '?aa'],
            ['a?', 'a?', 'a?'],
            ['aaaaaaa']]
    inverse = False
    full = True
    ans = grep.filter_strings_by_pattern(pattern, data, inverse, full)
    assert ans == [[],
                   ['a?'],
                   ['a?', 'a?', 'a?'],
                   []]
    pattern = 'aa'
    data = [['a', 'aa'],
            ['a?', '?aa'],
            ['a?', 'a?', 'aa', 'a?'],
            ['aaaaaaa']]
    inverse = True
    full = True
    ans = grep.filter_strings_by_pattern(pattern, data, inverse, full)
    assert ans == [['a'],
                   ['a?', '?aa'],
                   ['a?', 'a?', 'a?'],
                   ['aaaaaaa']]


def test_unit_count_filtered_strings():
    data = [['alex', 'alex?', '????alex', 'ale'],
            ['alex?', 'ale', 'alex', 'ale'],
            [],
            ['?alex?', '?ale']]
    ans = grep.count_filtered_strings(data)
    assert ans == [['4'], ['4'], ['0'], ['2']]


def test_unit_format_output_string():
    name_file = 'input.txt'
    line = 'test input.txt'
    file_is = True
    ans = grep.format_output_string(name_file, line, file_is)
    assert ans == 'input.txt:test input.txt'
    file_is = False
    ans = grep.format_output_string(name_file, line, file_is)
    assert ans == 'test input.txt'


def test_unit_print_lines(capsys):
    data = ['it', 'is', 'i']
    name_file = 'a.txt'
    file_is = True
    grep.print_lines(data, name_file, file_is)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:it\na.txt:is\na.txt:i\n'
    file_is = False
    grep.print_lines(data, name_file, file_is)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'it\nis\ni\n'


def test_unit_strip_lines():
    lines = ['\n', 'oooooo', 'nice\n', '\n', 'n', '\n']
    ans = grep.strip_lines(lines)
    assert ans == ['', 'oooooo', 'nice', '', 'n', '']
