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
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_unit_split_files_by_existence(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('something')
    (tmp_path / 'b.txt').write_text('something#2')
    monkeypatch.chdir(tmp_path)
    existing, nonexistent = grep.split_files_by_existence(['a.txt', 'not.txt', 'b.txt', 'b.txt', 'd.txt'])
    out, err = capsys.readouterr()
    assert existing == ['a.txt', 'b.txt', 'b.txt']
    assert nonexistent == ['not.txt', 'd.txt']
    assert err == ''
    assert out == ''


def test_unit_read_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('something\nhello\nhow are you?\n')
    (tmp_path / 'b.txt').write_text('interesting\nwhat is going on?\n\n')
    monkeypatch.chdir(tmp_path)
    read = grep.read_files(['a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert read == [['something\n', 'hello\n', 'how are you?\n'],
                    ['interesting\n', 'what is going on?\n', '\n']]
    assert err == ''
    assert out == ''


def test_unit_strip_lines(capsys):
    lines = ['hello, Anya!\n', '\nHow are you?\n', 'I hope\n you like this hw!\n\n']
    lines = grep.strip_lines(lines)
    out, err = capsys.readouterr()
    assert lines == ['hello, Anya!', '\nHow are you?', 'I hope\n you like this hw!']
    assert out == ''
    assert err == ''


def test_unit_filter_matched_lines(capsys):
    lines = ['hello yohoo!', 'how are you?', 'do you want?', 'do u want?']
    lines = grep.filter_matched_lines(lines, 'you', False, False, False)
    out, err = capsys.readouterr()
    assert lines == ['how are you?', 'do you want?']
    assert out == ''
    assert err == ''


def test_unit_filter_matched_lines_regex(capsys):
    lines = ['hello yohoo!', 'how are you?', 'do you want?', 'do u want?']
    lines = grep.filter_matched_lines(lines, 'you?', True)
    out, err = capsys.readouterr()
    assert lines == ['hello yohoo!', 'how are you?', 'do you want?']
    assert out == ''
    assert err == ''


# def test_unit_print_matched_lines_fir(capsys):
#     lines = ['hello!', 'how are you?']
#     grep.print_matched_lines(lines, 'Hey.txt', False, '{name}{counting}{text}')
#     out, err = capsys.readouterr()
#     assert out == 'Hey.txt:hello!\nHey.txt:how are you?\n'
#     assert err == ''
#
#
# def test_unit_print_matched_lines_sec(capsys):
#     lines = ['hello!', 'how are you?']
#     grep.print_matched_lines(lines, None, True, '{name}{counting}{text}')
#     out, err = capsys.readouterr()
#     assert out == '2\n'
#     assert err == ''
#
#
# def test_unit_get_arguments_first(capsys):
#     args = grep.parse_arguments(['needle', 'a.txt', 'b.txt', 'c.txt', '-E', '-c'])
#     out, err = capsys.readouterr()
#     assert args.pattern == 'needle'
#     assert args.regex
#     assert args.counting
#     assert args.files == ['a.txt', 'b.txt', 'c.txt']
#     assert out == ''
#     assert err == ''
#
#
# def test_unit_get_arguments_second(capsys):
#     args = grep.parse_arguments(['nope'])
#     out, err = capsys.readouterr()
#     assert args.pattern == 'nope'
#     assert not args.regex
#     assert not args.counting
#     assert not args.files
#     assert out == ''
#     assert err == ''
