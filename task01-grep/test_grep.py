import io
import grep


def test_filter_lines_0():
    assert grep.filter_lines(['line', 'lion', 'life', 'wolf'], 'li') == ['line', 'lion', 'life']


def test_filter_lines_1():
    assert grep.filter_lines(['line', 'lion', 'life', 'wolf'], '..', True) ==\
        ['line', 'lion', 'life', 'wolf']


def test_filter_lines_2():
    assert grep.filter_lines(['line', 'lion', 'life', 'wolf'], '..') == []


def test_filter_lines_3():
    assert grep.filter_lines(['line', 'lion', 'wolf'], '..', True) == ['line', 'lion', 'wolf']


def test_filter_lines_4():
    assert grep.filter_lines(['lion', 'wolf'], 'on') == ['lion']


def test_filter_lines_5():
    assert grep.filter_lines(['lion', 'wolf'], 'on', True) == ['lion']

# Не, ну ты их разнёс на разные функции, конечно, а остальные комментарии проигнорировал.
# Тесты не должны зваться *_число. Ещё раз. Мораль такая: Хочется по назвнию теста чётко понимать, о чём он и почему.
# Например, в твоих случаях: test_filter_lines_0 можно бы назвать test_filter_lines_no_regex_key,
# а test_filter_lines_2 назвать test_filter_lines_no_regex_key_regex_like_needle, чтобы было понятно, а зачем они.
# И опять же. тесты 1 и 3 чем отличаются вообще? А тесты 0 и 4? Это whitebox тесты. Там ты знаешь,
# как изнутри работает код. Если хочешь тестировать на префиксы и суффиксы, сделай, например,
# ['lion', 'io', 'ion', 'radio'], 'io' и всё.
# А писал бы нормальные имена, заметил бы, что пишешь одно и то же.


def test_format_output_lines():
    assert grep.format_output_lines(['cat', 'dog'], 'src.txt') == ['src.txt:cat', 'src.txt:dog']


def test_format_output_line():
    assert grep.format_output_line('gg.txt', 'GGWP') == 'gg.txt:GGWP'


def test_exec_grep_0():
    assert grep.exec_grep(['line', 'lion', 'life', 'wolf'], 'li') == ['line', 'lion', 'life']


def test_exec_grep_1():
    assert grep.exec_grep(['line', 'lion', 'life', 'wolf'], '..', True) ==\
        ['line', 'lion', 'life', 'wolf']


def test_exec_grep_2():
    assert grep.exec_grep(['line', 'lion', 'life', 'wolf'], '..') == []


def test_exec_grep_3():
    assert grep.exec_grep(['line, lion, life', 'wolf'], '..', False, True, 'src.txt') ==\
        ['src.txt:0']


def test_exec_grep_4():
    assert grep.exec_grep(['line', 'lion', 'wolf'], '..', True, True) == ['3']


def test_exec_grep_5():
    assert grep.exec_grep(['lion', 'wolf'], 'on') == ['lion']


def test_exec_grep_6():
    assert grep.exec_grep(['lion', 'wolf'], 'on', True) == ['lion']


def check_output(capsys, expected_output):
    out, err = capsys.readouterr()
    assert err == ''
    assert out == expected_output


def test_print_result_0(capsys):
    grep.print_result(['one', 'two', 'four', 'three'])
    check_output(capsys, 'one\ntwo\nfour\nthree\n')


def test_print_result_1(capsys):
    grep.print_result(['one.txt:one', 'two.txt:two', 'three.txt:four', 'four.txt:three'])
    check_output(capsys, 'one.txt:one\ntwo.txt:two\nthree.txt:four\nfour.txt:three\n')


def test_get_striped_lines():
    assert grep.get_striped_lines(['line\n', 'another line', 'line\n\n\n\n']) ==\
        ['line', 'another line', 'line']


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