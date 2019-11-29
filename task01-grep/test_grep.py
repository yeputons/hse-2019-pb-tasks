#!/usr/bin/env python3
import io
import grep


def test_find_in_string_first():
    needle = 'kud'
    check_list = 'kudkuda'
    regex = False
    ans_value = grep.find_in_string(regex, needle, check_list)
    assert ans_value


def test_find_in_string_second():
    needle = '[0-9]'
    check_list = 'ku12dkuda'
    regex = True
    ans_value = grep.find_in_string(regex, needle, check_list)
    assert ans_value is not None


def test_find_in_string_first_false():
    needle = 'kud'
    check_list = 'kuergkrgfuda'
    regex = False
    ans_value = grep.find_in_string(regex, needle, check_list)
    assert not ans_value


def test_find_in_string_second_false():
    needle = '[0-9]'
    check_list = 'kudkuda'
    regex = True
    ans_value = grep.find_in_string(regex, needle, check_list)
    assert not ans_value


def test_print_answer_first(capsys):
    count = True
    file_name = 'gdgf.txt'
    check_list = ['kudkuda', 'asdvrk', 'vrjv', '348rfhu', 'i4398f']
    grep.print_answer(count, check_list, file_name)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'gdgf.txt5\n'


def test_print_answer_second(capsys):
    count = False
    file_name = 'gdgf.txt'
    check_list = ['kudkuda', 'asdvrk', 'vrjv', '348rfhu', 'i4398f']
    grep.print_answer(count, check_list, file_name)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'gdgf.txtkudkuda\ngdgf.txtasdvrk\ngdgf.txtvrjv\ngdgf.txt348rfhu\ngdgf.txti4398f\n'


def test_action_count_first(capsys):
    file_name = 'gdgf.txt'
    check_list = ['kudkuda', 'asdvrk', 'vrjv', '348rfhu', 'i4398f']
    grep.action_count(check_list, file_name)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'gdgf.txt5\n'


def test_action_count_second(capsys):
    file_name = ''
    check_list = ['kudkuda', 'asdvrk', 'vrjv', '348rfhu', 'i4398f']
    grep.action_count(check_list, file_name)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '5\n'


def test_create_right_list_true():
    regex = True
    input_list = ['rbrb', '1', 'ejhbv43njev43bfr', 'rrrjnb789', '245', '342645654', 'rebrhrh']
    right_list = []
    needle = '[0-9]'
    grep.create_right_list(regex, input_list, needle, right_list)
    assert right_list == ['1', 'ejhbv43njev43bfr', 'rrrjnb789', '245', '342645654']


def test_create_right_list_false():
    regex = False
    input_list = ['rbrb', 'b1rb', 'ejhbv4brb3njev43bfr',
                  'rrrjnb789', '245', '34264brb5654', 'rebrhrbrbrbrbrbrbrrbrbh']
    right_list = []
    needle = 'brb'
    grep.create_right_list(regex, input_list, needle, right_list)
    assert right_list == ['rbrb', 'ejhbv4brb3njev43bfr', '34264brb5654', 'rebrhrbrbrbrbrbrbrrbrbh']


def test_print_screen_first(capsys):
    right_list = ['rbrb', 'ejhbv4brb3njev43bfr', '34264brb5654', 'rebrhrbrbrbrbrbrbrrbrbh']
    file_name = 'petux.txt'
    grep.print_screen(right_list, file_name)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'petux.txtrbrb\npetux.txtejhbv4brb3njev43bfr' \
                  '\npetux.txt34264brb5654\npetux.txtrebrhrbrbrbrbrbrbrrbrbh\n'


def test_print_screen_second(capsys):
    right_list = ['rbrb', 'ejhbv4brb3njev43bfr', '34264brb5654', 'rebrhrbrbrbrbrbrbrrbrbh']
    file_name = ''
    grep.print_screen(right_list, file_name)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'rbrb\nejhbv4brb3njev43bfr\n34264brb5654\nrebrhrbrbrbrbrbrbrrbrbh\n'


def test_grep_terminal(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_grep_terminal_regex(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_grep_terminal_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_grep_terminal_count_regex(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needl133e\nneedle suf\nthe nee2dl 23\npref needle suf\n435345\n47n435 3584 345 345'))
    grep.main(['-c', '-E', '[0-9]'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


def test_grep_one_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_grep_one_file_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('nrevnazazrfbv dwcza\n azaz '
                                    'azaz azaz azaz\n5r39azaz ewjfnazldn\n dcjaz')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'azaz', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_grep_one_file_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('43 5y556h 56hgrkt\n brvjrgbnj '
                                    'rtinnjn rbntjb\ntyhnjh thrjgnk rjevn2 4')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '[0-9]', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '43 5y556h 56hgrkt\ntyhnjh thrjgnk rjevn2 4\n'


def test_grep_one_file_count_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('43 5y556h 56hgrkt\n brvjrgbnj '
                                    'rtinjn rbntjb\ntyhnjh thrjgnk rjevn2 4')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', '[0-9]', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_grep_few_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_grep_few_files_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_grep_few_files_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref need34le\nneedle suf\n35\nergvjne 546 mgrf')
    (tmp_path / 'b.txt').write_text('the needl\nprdg4ef needle suf\n5')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '[0-9]', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:prdg4ef needle suf\nb.txt:5\na.txt:pref ' \
                  'need34le\na.txt:35\na.txt:ergvjne 546 mgrf\n'


def test_grep_few_files_count_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref need34le\nneedle suf\n35\nergvjne 546 mgrf')
    (tmp_path / 'b.txt').write_text('the needl\nprdg4ef needle suf\n5')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', '[0-9]', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:2\na.txt:3\n'
