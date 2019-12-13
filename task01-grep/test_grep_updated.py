#!/usr/bin/env python3
import grep


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


def test_integrate_all_keys_print_not_files_grep_empty(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    (tmp_path / 'c.txt').write_text('')
    monkeypatch.chdir(tmp_path)
    grep.main(['-Livx', '-E', 'fo?o', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nc.txt\n'


def test_integrate_all_keys_print_files_grep_empty(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    (tmp_path / 'c.txt').write_text('')
    monkeypatch.chdir(tmp_path)
    grep.main(['-livx', '-E', 'fo?o', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_integrate_all_keys_print_files_grep_empty_2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    (tmp_path / 'c.txt').write_text('\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-livx', '-E', 'fo?o', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\nc.txt\n'


def test_integrate_invert_ignore_register_print_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    (tmp_path / 'c.txt').write_text('')
    monkeypatch.chdir(tmp_path)
    grep.main(['-lix', '-E', 'fo?o', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_integrate_substr_full_match_print_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFreoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz2\nfooo2\n')
    (tmp_path / 'c.txt').write_text('')
    monkeypatch.chdir(tmp_path)
    grep.main(['-lix', 'fo', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_unit_output_detected_files_names(capsys):
    input_files = ['a.txt', 'b.txt', 'c.txt']
    input_lines = [['oh', 'my', 'god', '', ' ', 'end'], [], ['']]
    grep.output(input_files, input_lines, need_detected_file_names=True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nc.txt\n'


def test_unit_output_undetected_files_names(capsys):
    input_files = ['a.txt', 'b.txt', 'c.txt', 'd']
    input_lines = [['oh', 'my', 'god', '', ' ', 'end'], [], [''], []]
    grep.output(input_files, input_lines, need_undetected_file_names=True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\nd\n'


def test_unit_detect_lines_substring():
    input_lines = [['Cry', "don't cry"], ['cRack', 'hehe'], ['car', 'rC']]
    detection_func = grep.get_detection_func('cR', ignore_register=True)
    out = grep.detect_requested_lines(detection_func, input_lines)
    assert out == [['Cry', "don't cry"], ['cRack'], []]


def test_unit_detect_lines_substring_invert():
    input_lines = [['Cry', "don't cry"], ['cRack', 'hehe'], ['car', 'rC']]
    detection_func = grep.get_detection_func('cR', ignore_register=True, invert_detection=True)
    out = grep.detect_requested_lines(detection_func, input_lines)
    assert out == [[], ['hehe'], ['car', 'rC']]


def test_unit_detect_lines_substring_full_match():
    input_lines = [['Cry', "don't cry"], ['cRack', 'hehe'], ['car', 'rC'], ['cR']]
    detection_func = grep.get_detection_func('cR', ignore_register=True,
                                             invert_detection=True, need_full_match=True)
    out = grep.detect_requested_lines(detection_func, input_lines)
    assert out == [['Cry', "don't cry"], ['cRack', 'hehe'], ['car', 'rC'], []]


def test_unit_detect_lines_regex():
    input_lines = [['Cry', "don't cry"], ['cRack', 'hehe'], ['car', 'rC'], [], ['rrc']]
    detection_func = grep.get_detection_func('c', need_regex=True, ignore_register=True)
    out = grep.detect_requested_lines(detection_func, input_lines)
    assert out == [['Cry', "don't cry"], ['cRack'], ['car', 'rC'], [], ['rrc']]


def test_unit_detect_lines_regex_invert():
    input_lines = [['Cry', "don't cry"], ['cRack', 'hehe'], ['car', 'rC']]
    detection_func = grep.get_detection_func('c', need_regex=True,
                                             ignore_register=True, invert_detection=True)
    out = grep.detect_requested_lines(detection_func, input_lines)
    assert out == [[], ['hehe'], []]


def test_unit_detect_lines_regex_full_match():
    input_lines = [['Cry', "don't cry"], ['cRack', 'hehe'], ['car', 'rC'], [], ['rrc']]
    detection_func = grep.get_detection_func('c.*', need_regex=True,
                                             ignore_register=True, need_full_match=True)
    out = grep.detect_requested_lines(detection_func, input_lines)
    assert out == [['Cry'], ['cRack'], ['car'], [], []]


def test_unit_detect_lines_substring_register_full_match():
    input_lines = [['Cry', "don't cry"], ['cRack', 'hehe', ''], ['car', 'rC', 'cR']]
    detection_func = grep.get_detection_func('cR', need_full_match=True)
    out = grep.detect_requested_lines(detection_func, input_lines)
    assert out == [[], [], ['cR']]


def test_unit_detect_lines_regex_register():
    input_lines = [['Cry', "don't cry"], ['cRack', 'hehe'], ['car', 'rC', ''], [], ['rrc']]
    detection_func = grep.get_detection_func('c.', need_regex=True)
    out = grep.detect_requested_lines(detection_func, input_lines)
    assert out == [["don't cry"], ['cRack'], ['car'], [], []]


def test_unit_detect_lines_regex_register_invert():
    input_lines = [['Cry', "don't cry"], ['cRack', 'hehe'], ['car', 'rC', ''], [], ['rrc', 'same']]
    detection_func = grep.get_detection_func('.c', need_regex=True, invert_detection=True)
    out = grep.detect_requested_lines(detection_func, input_lines)
    assert out == [['Cry'], ['hehe'], ['car', 'rC', ''], [], ['same']]


def test_unit_detect_lines_substring_register_full_match_invert():
    input_lines = [['Cry', "don't cry"], ['cRack', 'hehe', '', 'Cr'],
                   ['car', 'rC', 'cR'], [''], [], ['cR']]
    detection_func = grep.get_detection_func('cR', need_full_match=True, invert_detection=True)
    out = grep.detect_requested_lines(detection_func, input_lines)
    assert out == [['Cry', "don't cry"], ['cRack', 'hehe', '', 'Cr'],
                   ['car', 'rC'], [''], [], []]
