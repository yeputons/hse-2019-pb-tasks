import io
import grep


def test_format_output_line_with_filename():
    assert grep.format_output_line('papers', 'please') == 'papers:please'


def test_format_output_line_without_filename():
    assert grep.format_output_line(None, 'please') == 'None:please'


def test_format_output_lines():
    assert grep.format_output_lines(['one', 'two', 'three'], 'src') ==\
           ['src:one', 'src:two', 'src:three']


def test_invert_inclusions():
    assert grep.invert_inclusions(['1', '228', '1337'], ['1', '2', '3', '228', '1337']) ==\
           ['2', '3']


def test_get_striped_lines():
    assert grep.get_striped_lines(['line\n', 'another line', 'line\n\n\n\n']) ==\
           ['line', 'another line', 'line']


def test_filter_lines_without_smth():
    assert grep.filter_lines(['aba', 'bbb', 'cc'], 'b') == ['aba', 'bbb']


def test_filter_lines_with_regex():
    assert grep.filter_lines(['caba', 'bbb', 'cc'], 'c*b', is_regex=True) == ['caba', 'bbb']


def test_exec_grep_without_smth():
    assert grep.exec_grep(['abbbb', 'file', 'main.cpp', 'main.cpp'], 'main.cpp') ==\
           ['main.cpp', 'main.cpp']


def test_exec_grep_with_counting_mode():
    assert grep.exec_grep(['abbbb', 'file', 'main.cpp', 'main.cpp'], 'main.cpp',
                          counting_mode=True) == ['2']


def test_exec_grep_with_source():
    assert grep.exec_grep(['abbbb', 'file', 'main.cpp', 'main.cpp'], 'main.cpp', source='gcc') ==\
           ['gcc:main.cpp', 'gcc:main.cpp']


def check_output(capsys, expected_output):
    out, err = capsys.readouterr()
    assert err == ''
    assert out == expected_output


def test_print_result_without_filenames(capsys):
    grep.print_result(['one', 'two', 'four', 'three'])
    check_output(capsys, 'one\ntwo\nfour\nthree\n')


def test_print_result_with_filenames(capsys):
    grep.print_result(['one.txt:one', 'two.txt:two', 'three.txt:four', 'four.txt:three'])
    check_output(capsys, 'one.txt:one\ntwo.txt:two\nthree.txt:four\nfour.txt:three\n')


def test_integrate_output_matched_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-l', 'needle', 'b.txt', 'a.txt'])
    check_output(capsys, 'b.txt\na.txt\n')


def test_integrate_output_unmatched_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    (tmp_path / 'badfile.txt').write_text('texttexttexttext\nndleee\n\n\nF')

    monkeypatch.chdir(tmp_path)
    grep.main(['-L', 'needle', 'b.txt', 'a.txt', 'badfile.txt'])
    check_output(capsys, 'badfile.txt\n')


def test_integrate_stdin_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['needle?'])
    check_output(capsys, 'pref needle?\nneedle? suf\npref needle? suf\n')


def test_integrate_stdin_regex_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-E', 'needle?'])
    check_output(capsys, 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n')


def test_integrate_stdin_grep_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', 'needle'])
    check_output(capsys, '3\n')


def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    check_output(capsys, 'pref needle suf\n')


def test_integrate_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'b.txt', 'a.txt'])
    check_output(capsys, '\n'.join(['b.txt:pref needle suf',
                                    'a.txt:pref needle',
                                    'a.txt:needle suf\n']))


def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    check_output(capsys, 'b.txt:1\na.txt:2\n')
