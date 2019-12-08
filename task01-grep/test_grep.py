#!/usr/bin/env python3
import io
import grep


def test_is_matching_str():
    assert grep.is_matching('abcdef', pattern='abcd', is_inverse=False, is_full_match=False)


def test_is_matching_regex():
    assert grep.is_matching('abcd', pattern='a*', is_inverse=False, is_full_match=False)


def test_filter_matching_lines():
    # непредсказуемый тест
    assert grep.filter_matching_lines(['failfail', 'dfsbfs'], 'f*', is_full_match=False,
                                      is_inverse=False) \
           == ['failfail', 'dfsbfs']


def test_format_output():
    assert grep.format_output(['gay', 'loh'], False, False, False, 'MISHAGAY.txt') \
           == ['MISHAGAY.txt:gay', 'MISHAGAY.txt:loh']


def test_grep_from_raw():
    assert grep.grep_from_raw(['Wee want to sleep', 'Slepp? Are you sure?'],
                              'sle?p', False, False,
                              False, False, False, None) == []


def test_strip_lines():
    assert grep.strip_lines(['one\n', 'two', 'three\n\n']) == ['one', 'two', 'three']


def check_output(capsys, expected_output):
    out, err = capsys.readouterr()
    assert err == ''
    assert out == expected_output


def test_print_answer_str(capsys):
    grep.print_answer(['one', 'two', 'three'])
    check_output(capsys, 'one\ntwo\nthree\n')


def test_print_answer_format(capsys):
    grep.print_answer(['one.txt:one', 'two.txt:two', 'three.txt:three'])
    check_output(capsys, 'one.txt:one\ntwo.txt:two\nthree.txt:three\n')


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
