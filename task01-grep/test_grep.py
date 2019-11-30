#!/usr/bin/env python3
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


def test_integrate_the_same_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt', 'b.txt', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\nb.txt:1\nb.txt:1\na.txt:2\n'


def test_integrate_file_grep_empty_out(tmp_path, monkeypatch, capsys):
    (tmp_path / 'first.txt').write_text("what's\nwrong\nwith\nyou?\n")
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'wro*ng?s+', 'first.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_integrate_files_no_such_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'b.txt', 'c.txt', 'a.txt', 'd.txt'])
    out, err = capsys.readouterr()
    assert err == 'No such file: c.txt\nNo such file: d.txt\n'
    assert out == ''


def test_unit_split_files_by_existence(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('something')
    (tmp_path / 'b.txt').write_text('something#2')
    monkeypatch.chdir(tmp_path)
    existing, nonexistent = grep.split_files_by_existence(['a.txt', 'not.txt',
                                                           'b.txt', 'b.txt', 'd.txt'])
    assert existing == ['a.txt', 'b.txt', 'b.txt']
    assert nonexistent == ['not.txt', 'd.txt']


def test_unit_read_files(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('something\nhello\nhow are you?\n')
    (tmp_path / 'b.txt').write_text('interesting\nwhat is going on?\n\n')
    monkeypatch.chdir(tmp_path)
    read = grep.read_files(['a.txt', 'b.txt'])
    assert read == [['something\n', 'hello\n', 'how are you?\n'],
                    ['interesting\n', 'what is going on?\n', '\n']]


def test_unit_strip_lines():
    lines = ['hello, Anya!\n', '\nHow are you?\n', 'I hope\n you like this hw!\n\n']
    lines = grep.strip_lines(lines)
    assert lines == ['hello, Anya!', '\nHow are you?', 'I hope\n you like this hw!']


def test_unit_filter_line():
    searcher = re.compile('hello')
    matched = grep.match_line('hello, how are you?', searcher, False, False)
    assert matched


def test_unit_filter_lines():
    lines = ['hello yohoo!', 'how are you?', 'do you want?', 'do u want?']
    searcher = re.compile(re.escape('you'))
    lines = grep.filter_lines(lines, searcher, False, False)
    assert lines == ['how are you?', 'do you want?']


def test_unit_filter_lines_regex():
    lines = ['hello yohoo!', 'how are you?', 'do you want?', 'do u want?']
    searcher = re.compile('you?')
    lines = grep.filter_lines(lines, searcher, False, False)
    assert lines == ['hello yohoo!', 'how are you?', 'do you want?']


def test_prepare_output_without_flags_and_name():
    lines = ["I'm happy, I'll be printed!", 'why are doing that? Printer.',
             'STOP IT PLEASE. Wow, I found a printer']
    output = grep.prepare_output(lines, None, False, False, False)
    assert output == ["I'm happy, I'll be printed!", 'why are doing that? Printer.',
                      'STOP IT PLEASE. Wow, I found a printer']


def test_prepare_output_with_name_and_c():
    lines = ["I'm happy, I'll be printed!", 'why are doing that? Printer.',
             'STOP IT PLEASE. Wow, I found a printer']
    output = grep.prepare_output(lines, 'KEK.lol', True, False, False)
    assert output == ['KEK.lol:3']


def test_unit_get_arguments_files_flags():
    args = grep.parse_arguments(['needle', 'a.txt', 'b.txt', 'c.txt', '-E', '-c'])
    assert args.pattern == 'needle'
    assert args.regex
    assert args.counting
    assert args.files == ['a.txt', 'b.txt', 'c.txt']


def test_unit_print_lines(capsys):
    lines = ['HELP ME', 'I have to be strong!', 'I will finish it!!!!']
    grep.print_matched_lines(lines)
    out = capsys.readouterr()[0]
    assert out == 'HELP ME\nI have to be strong!\nI will finish it!!!!\n'


def test_unit_get_arguments_nothing():
    args = grep.parse_arguments(['nope'])
    assert args.pattern == 'nope'
    assert not args.regex
    assert not args.counting
    assert not args.files
