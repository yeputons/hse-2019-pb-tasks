#!/usr/bin/env python3
import grep


def test_integrate_ignore_case_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('hello f?o world\nxfooyfoz\nfooo\n')
    (tmp_path / 'b.txt').write_text('fO\nFO\nFoO\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:fO\nb.txt:FO\nb.txt:FoO\na.txt:xfooyfoz\na.txt:fooo\n'


def test_integrate_ignore_case_count_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('hello f?o world\nxfooyfoz\nfooo\n')
    (tmp_path / 'b.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'c.txt').write_text('f\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-ic', '-E', 'fo?o', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:3\na.txt:2\n'


def test_integrate_inverse_answer_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('hello f?o world\n')
    (tmp_path / 'b.txt').write_text('abc\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-iv', '-E', 'fo', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:hello f?o world\nb.txt:abc\n'


def test_integrate_only_files_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('hello fo world\nxfooyfoz\nfooo\n')
    (tmp_path / 'b.txt').write_text('abc\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-ivl', '-E', 'fo', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_integrate_inverse_only_files_flag_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('hello fo world\nxfooyfoz\nfooo\n')
    (tmp_path / 'b.txt').write_text('abc\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-ivL', '-E', 'fo', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


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


def test_integrate_i_keys_count_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-civx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:3\na.txt:0\n'


def test_unit_parse_args_files_regex_ingnore_case():
    parsed_args = grep.parse_args(['-vicL', '-E', 'he?o', 'b.txt', 'a.txt'])
    assert parsed_args.count
    assert parsed_args.files == ['b.txt', 'a.txt']
    assert parsed_args.pattern == 'he?o'
    assert parsed_args.regex
    assert parsed_args.ignore_case
    assert parsed_args.inverse_answer
    assert parsed_args.inverse_only_files
    assert not parsed_args.only_files


def test_unit_compile_pattern_not_regex():
    compiled_pattern = grep.compile_pattern('CGSG*', is_pattern_regex=False,
                                            ignore_case=True)
    assert compiled_pattern.search('cgsg*')
    assert not compiled_pattern.search('cgsgforever')
    assert not compiled_pattern.search('cgsg')


def test_unit_compile_pattern_regex():
    compiled_pattern = grep.compile_pattern('CGSG*', is_pattern_regex=True,
                                            ignore_case=False)
    assert not compiled_pattern.search('cgsg*')
    assert compiled_pattern.search('CGSGforever')
    assert not compiled_pattern.search('CGGS')


def test_unit_filter_matched_lines_inverse_answer():
    lines = grep.filter_matched_lines(['hello f?o world', 'xfooyfoz', 'fooo'],
                                      grep.compile_pattern('fo'), inverse_answer=True)
    assert lines == ['hello f?o world']


def test_unit_strip_lines():
    lines = grep.strip_lines(['CGSG\n', 'CGSG\n\n'])
    assert lines == ['CGSG', 'CGSG']
