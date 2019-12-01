import io
import re
import grep


def test_unit_filter_matching_lines():
    lines = ['incorrect line', 'correct line', 'right line', 'correct', 'c\no\nr\nr\ne\nc\nt']
    answer = grep.filter_matching_lines(re.escape('correct'), lines)
    assert answer == ['incorrect line', 'correct line', 'correct']


def test_unit_filter_matching_lines_regex():
    lines = ['...', 'dot', 'dot', 'abc', 'c', '']
    answer = grep.filter_matching_lines(re.compile('...'), lines)
    assert answer == ['...', 'dot', 'dot', 'abc']


def test_unit_print_lines(capsys):
    lines = ['first line', '<prefix>:second line', 'third line']
    grep.print_lines(lines)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'first line\n' \
                  '<prefix>:second line\n' \
                  'third line\n'


def test_unit_count_lines():
    lines = [['first', '2th', 'third'], [], [], ['word']]
    lines = grep.count_lines(lines)
    assert lines == [3, 0, 0, 1]


def test_unit_count_lines_empty():
    lines = []
    lines = grep.count_lines(lines)
    assert lines == []


def test_unit_build_pattern():
    substr = 'needle'
    result = grep.build_pattern(substr, False)
    assert result == re.compile(re.escape(substr))


def test_unit_build_pattern_regex():
    regex = '[0-9][a-z][Z-Z]*'
    result = grep.build_pattern(regex, True)
    assert result == re.compile(regex)


def test_unit_rstrip_lines():
    lines = ['begin? \n middle end?', '\n\n\n\n\n\n\n', '', 'pref\n', '\ntext...text\t']
    lines = grep.rstrip_lines(lines, '\n')
    assert lines == ['begin? \n middle end?', '', '', 'pref', '\ntext...text\t']


def test_unit_add_prefix():
    lines = [' <- prefix', 'The str need a prefix', '']
    prefix = 'title'
    lines = grep.add_prefix(prefix, lines, chars_between=')')
    assert lines == ['title) <- prefix', 'title)The str need a prefix', 'title)']


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


def test_integrate_files_grep_same_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('Прямой автострады тугая полоска\n'
                                    'И я по бетонной гремящей струне\n'
                                    'Лечу на железной гремящей повозке\n'
                                    'Где прадед мой ездил на рыжем коне')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'гремя', 'a.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\na.txt:2\n'


def test_integrate_files_grep_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('Living easy, living free\n'
                                    'Season ticket on a one-way ride\n'
                                    'Asking nothing, leave me be\n'
                                    'Taking everything in my stride...')
    (tmp_path / 'b.txt').write_text('Not a song\n'
                                    '(((\n'
                                    'Not a song\n'
                                    '(((')
    monkeypatch.chdir(tmp_path)
    grep.main(['Not a song', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:Not a song\nb.txt:Not a song\n'


def test_integrate_grep_empty_stdin(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(''))
    grep.main(['Not a song'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_integrate_grep_empty_file_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'Not a song', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '0\n'
