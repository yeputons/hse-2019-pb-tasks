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
    (tmp_path / 'b.txt').write_text('fasdkfj\naaaaa')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'a+a+a', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:0\n'


def test_unit_filter_strings_by_pattern_with_cond_first():
    pattern = 'a?lex?'
    pattern = re.compile(pattern)
    data = [['alex', '?', 'alex?', '????alex', 'ale', 'le'],
            ['alex?', 'ale', 'alex', 'ale'],
            ['hello'],
            ['alx?', '?alex?', '?ale', 'lex']]
    cond = False
    ans = grep.filter_strings_by_pattern_with_cond(pattern, data, cond)
    assert ans == [['alex', 'alex?', '????alex', 'ale', 'le'],
                   ['alex?', 'ale', 'alex', 'ale'],
                   [],
                   ['?alex?', '?ale', 'lex']]


def test_unit_filter_strings_by_pattern_with_cond_second():
    pattern = 'a+b*a?'
    pattern = re.compile(pattern)
    data = [['a', '', 'aa'],
            ['aaaaba'],
            [],
            ['abba', 'aba'],
            ['aaaaaa', 'baa']]
    cond = False
    ans = grep.filter_strings_by_pattern_with_cond(pattern, data, cond)
    assert ans == [['a', 'aa'],
                   ['aaaaba'],
                   [],
                   ['abba', 'aba'],
                   ['aaaaaa', 'baa']]


def test_unit_filter_strings_by_pattern_with_cond_third():
    pattern = 'a?'
    pattern = re.compile(re.escape(pattern))
    data = [['a', 'aa'],
            ['a?', '?aa'],
            ['a?', 'a?', 'a?'],
            ['aaaaaaa']]
    cond = False
    ans = grep.filter_strings_by_pattern_with_cond(pattern, data, cond)
    assert ans == [[],
                   ['a?'],
                   ['a?', 'a?', 'a?'],
                   []]


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
    cond = True
    ans = grep.format_output_string(name_file, line, cond)
    assert ans == 'input.txt:test input.txt'


def test_unit_print_lines(capsys):
    files = ['a.txt', 'b.txt', 'a.txt']
    data = [['aa', 'a', 's adf '],
            ['alex', 's sf '],
            ['aa', 'a', 's adf ']]
    cond = True
    grep.print_lines(files, data, cond)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:aa\na.txt:a\na.txt:s adf \n'\
                  'b.txt:alex\nb.txt:s sf \na.txt:a'\
                  'a\na.txt:a\na.txt:s adf \n'


def test_unit_strip_lines():
    lines = ['jsdafkj  pgia\n', 'sdafjha sf', 'alsdjfkdsa\n', '\n', 'n', '\n']
    ans = grep.strip_lines(lines)
    assert ans == ['jsdafkj  pgia', 'sdafjha sf', 'alsdjfkdsa', '', 'n', '']
