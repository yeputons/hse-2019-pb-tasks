#!/usr/bin/env python3
"""plug"""
import io
import grep


def test_integrate_stdin_grep(monkeypatch, capsys):
    """plug"""
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_integrate_stdin_regex_grep(monkeypatch, capsys):
    """plug"""
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_integrate_stdin_grep_count(monkeypatch, capsys):
    """plug"""
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_stdin_grep_regex_count(monkeypatch, capsys):
    """plug"""
    monkeypatch.setattr('sys.stdin', io.StringIO(
        '112\nWWW\nSU35\nF'))
    grep.main(['-c', '-E', '[0-9]'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    """plug"""
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_integrate_files_grep(tmp_path, monkeypatch, capsys):
    """plug"""
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    """plug"""
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_integrate_file_grep_count(tmp_path, monkeypatch, capsys):
    """plug"""
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_files_regex_grep(tmp_path, monkeypatch, capsys):
    """plug"""
    (tmp_path / 'a.txt').write_text('112\nmiu\n')
    (tmp_path / 'b.txt').write_text('one-two-three\n123')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '[0-9]', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:123\na.txt:112\n'


def test_integrate_file_regex_grep(tmp_path, monkeypatch, capsys):
    """plug"""
    (tmp_path / 'a.txt').write_text('wronganswer4\njunkz\npython')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '[0-9]', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'wronganswer4\n'


def test_integrate_file_count_regex_grep(tmp_path, monkeypatch, capsys):
    """plug"""
    (tmp_path / 'a.txt').write_text('wronganswer4\njunkz\npython')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', '[0-9]', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_integrate_files_count_regex_grep(tmp_path, monkeypatch, capsys):
    """plug"""
    (tmp_path / 'a.txt').write_text('wronganswer4\njunkz\npython')
    (tmp_path / 'b.txt').write_text('LeBron\nJames\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', '[0-9]', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:1\nb.txt:0\n'


def test_init_arguments():
    """plug"""
    args = grep.init_arguments(['task', 'input.txt', '-E', '-c'])
    assert args.pattern == 'task'
    assert args.files == ['input.txt']
    assert args.regex
    assert args.count


def test_translate_to_str_re_e():
    """plug"""
    test_string = '[0-9]\\d'
    is_regular = True
    result_string = grep.translate_str_to_re(test_string, is_regular)
    assert result_string == '[0-9]\\d'


def test_translate_to_str_not_e():
    """plug"""
    test_string = 'master'
    is_regular = False
    result_string = grep.translate_str_to_re(test_string, is_regular)
    assert result_string == 'master'


def test_filter_list():
    """plug"""
    list_ = ['grep', 'clear', 'history', 'bot']
    pattern = 'r'
    result_list = grep.filter_list(pattern, list_)
    assert result_list == ['grep', 'clear', 'history']


def test_strip():
    """plug"""
    list_ = ['plov\n', 'lavash\n', 'pomidor\n']
    result_list = grep.strip(list_)
    assert result_list == ['plov', 'lavash', 'pomidor']


def test_process_flag_c():
    """plug"""
    result_arr = ['aada', 'adss']
    new_result = grep.process_flag_c(result_arr)
    assert new_result == ['2']


def test_print_grep_result_without_file_or_with_only_one_file(capsys):
    """plug"""
    ans_list = ['a', 'ab', 'abc', 'abcd', 'abcde']
    output_format = ''
    grep.print_grep_results(ans_list, output_format)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a\nab\nabc\nabcd\nabcde\n'


def test_print_grep_results_with_more_than_one_file(capsys):
    """plug"""
    ans_list = ['112', 'shkaf']
    output_format = 'input.txt:'
    grep.print_grep_results(ans_list, output_format)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'input.txt:112\ninput.txt:shkaf\n'


def test_full_processing_result():
    word_list = ['google', 'yandex', 'mail', 'bing']
    pattern = 'a'
    flags = {'c': False}
    result = grep.full_processing_result(word_list, pattern, flags)
    assert result == ['yandex', 'mail']
