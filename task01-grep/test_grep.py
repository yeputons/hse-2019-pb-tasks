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


def test_integrate_stdin_grep_regex_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        '112\nWWW\nSU35\nF'))
    grep.main(['-c', '-E', '[0-9]'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


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


def test_integrate_file_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_files_regex_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('112\nmiu\n')
    (tmp_path / 'b.txt').write_text('one-two-three\n123')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '[0-9]', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:123\na.txt:112\n'


def test_integrate_file_regex_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('wronganswer4\njunkz\npython')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '[0-9]', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'wronganswer4\n'


def test_integrate_file_count_regex_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('wronganswer4\njunkz\npython')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', '[0-9]', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_integrate_files_count_regex_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('wronganswer4\njunkz\npython')
    (tmp_path / 'b.txt').write_text('LeBron\nJames\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', '[0-9]', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:1\nb.txt:0\n'


def test_integrate_all_keys_print_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-livx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_integrate_all_keys_print_not_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-Livx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_integrate_all_keys_count_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-civx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:3\na.txt:0\n'


def test_integrate_all_keys(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-ivx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:hello fo?o world\nb.txt:xfooyfoz\nb.txt:fooo\n'


def test_integrate_key_i(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:hello fo?o world\nb.txt:fooo\na.txt:fO\na.txt:FO\na.txt:FoO\n'


def test_integrate_key_v(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello foxo world\nxfoxoyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-v', '-E', 'foxo', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:fooo\na.txt:fO\na.txt:FO\na.txt:FoO\n'


def test_integrate_key_x(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfofofo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-x', '-E', 'fofofo', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:fofofo\n'


def test_integrate_key_big_l(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfrance\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-L', '-E', 'france', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_integrate_key_l(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nparmezano\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-l', '-E', 'parmezano', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_parse_arguments():
    args = grep.parse_arguments(['task', 'input.txt', '-E', '-c'])
    assert args.pattern == 'task'
    assert args.files == ['input.txt']
    assert args.regex
    assert args.count


def test_compile_pattern_regex_and_ignored():
    result_string = grep.compile_pattern(pattern='.', is_regex=True, ignored_case=True)
    assert result_string == re.compile('.', re.IGNORECASE)


def test_compile_pattern_only_regex():
    result_string = grep.compile_pattern(pattern='[0-9]\\d', is_regex=True, ignored_case=False)
    assert result_string == re.compile('[0-9]\\d')


def test_compile_pattern_only_ignored():
    result_string = grep.compile_pattern(pattern='master', is_regex=False, ignored_case=True)
    assert result_string == re.compile('master', re.IGNORECASE)


def test_compile_pattern_no_regex_no_ignored():
    result_string = grep.compile_pattern(pattern='master', is_regex=False, ignored_case=False)
    assert result_string == re.compile('master')


def test_rstrip_lines_right():
    lines = ['plov\n', 'lavash\n', 'pomidor\n']
    result_list = grep.rstrip_lines(lines)
    assert result_list == ['plov', 'lavash', 'pomidor']


def test_rstrip_lines_left():
    lines = ['\nplov', '\nlavash', '\npomidor']
    result_list = grep.rstrip_lines(lines)
    assert result_list == ['\nplov', '\nlavash', '\npomidor']


def test_read_files(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('mem\nory\n')
    (tmp_path / 'b.txt').write_text('lim\nit\n')
    monkeypatch.chdir(tmp_path)
    read = grep.read_files(['a.txt', 'b.txt'])
    assert read == [['mem\n', 'ory\n'],
                    ['lim\n', 'it\n']]


def test_is_matched_with_matched_and_inverted():
    assert not grep.is_matched(line='kek', pattern=re.compile('kek'), inverted=True, matched=True)


def test_is_matched_with_only_inverted():
    assert not grep.is_matched(line='kekek', pattern=re.compile('kek'),
                               inverted=True, matched=False)


def test_is_matched_with_only_matched():
    assert not grep.is_matched(line='kekek', pattern=re.compile('kek'),
                               inverted=False, matched=True)


def test_is_matched_not_matched_not_inverted():
    assert grep.is_matched(line='kekek', pattern=re.compile('kek'),
                           inverted=False, matched=False)


def test_filter_lines():
    assert grep.filter_lines(lines=['algebra', 'minecraft', 'dota'],
                             pattern=re.compile('alg'), inverted=True,
                             full_match=False) == ['minecraft', 'dota']


def test_filter_lines_more_interesting():
    assert grep.filter_lines(lines=['kEk', 'sdKEK', 'miu'], pattern=re.compile('kek', flags=re.I),
                             inverted=True, full_match=True) == ['sdKEK', 'miu']


def test_process_underprint_results_flag_l():
    assert grep.prepare_output_results(lines=['a', 'ab', 'ac', 'bc', 'abc'],
                                       source_name='file.txt', flag_count=False,
                                       file_with_str=True, file_without_str=False) == ['file.txt']


def test_process_underprint_results_flag_big_l():
    assert grep.prepare_output_results(lines=['a', 'ab', 'ac', 'bc', 'abc'],
                                       source_name='file.txt', flag_count=False,
                                       file_with_str=False, file_without_str=True) == []


def test_process_underprint_results_flag_c():
    assert grep.prepare_output_results(lines=['a', 'ab', 'ac', 'bc', 'abc'],
                                       source_name='file.txt', flag_count=True,
                                       file_with_str=False, file_without_str=False) \
                                        == ['file.txt:5']


def test_process_underprint_results_no_flags():
    assert grep.prepare_output_results(lines=['a', 'ab', 'ac', 'bc', 'abc'],
                                       source_name='file.txt', flag_count=False,
                                       file_with_str=False, file_without_str=False)\
                                        == ['file.txt:a', 'file.txt:ab', 'file.txt:ac',
                                            'file.txt:bc', 'file.txt:abc']


def test_print_grep_results(capsys):
    """plug"""
    results = ['a', 'ab', 'abc', 'abcd', 'abcde']
    grep.print_output_results(results)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a\nab\nabc\nabcd\nabcde\n'
