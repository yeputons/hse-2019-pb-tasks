#!/usr/bin/env python3
import io
import grep


# Проверка корректности работы функции print_in_format
# в случае одного файла и стандартного потока ввода
def test_unit_print_in_format_one_argument(monkeypatch, tmp_path, capsys):
    (tmp_path / 'in.txt').write_text('This is a simple test')
    monkeypatch.chdir(tmp_path)
    file = open('in.txt', 'r')
    grep.print_in_format(file, 'second argument', 1)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'second argument\n'
    file.close()


# Проверка корректности работы функции print_in_format в случае нескольких файлов
def test_unit_print_in_format_more_than_one_argument(monkeypatch, tmp_path, capsys):
    p = tmp_path / 'in.text'
    p.write_text('This is a simple test')
    monkeypatch.chdir(tmp_path)
    file = open('in.text', 'r')
    grep.print_in_format(file, 'second argument', 5)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'in.text:second argument\n'
    file.close()


# Проверка корректности работы функции search_print_count в случае только флага -c
def test_unit_count_not_regex(capsys):
    test_text = 'This is a simple test trompompop\n' \
                'the main idea tram\n' \
                'is to find out pom pam\n' \
                'whether this function para\n' \
                'is working properly pam pam\n'
    grep.search_print_count('is', [io.StringIO(test_text)], False, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


# Проверка корректности работы функции search_print_count в случае флагов -c -E
def test_unit_count_regex(capsys):
    test_text = 'This is a simple test trompompop\n' \
                'the main idea tram\n' \
                'is to find out pom pam\n' \
                'whether this function para\n' \
                'is working properly pam pam\n'
    grep.search_print_count('pa?o?m', [io.StringIO(test_text)], True, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


# Проверка корректности работы функции search_print_count работы в случае отсутствия флагов
def test_unit_print(monkeypatch, tmp_path, capsys):
    file_path = tmp_path / 'in.txt'
    file_path.write_text('No hay nadie como tu en todo el mundo\n'
                         'no hay nadie como tu mi amor\n'
                         'mejita yo te queiro\n')
    monkeypatch.chdir(tmp_path)
    file = open('in.txt', 'r')
    grep.search_print_count('mejita', [file], False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'mejita yo te queiro\n'
    file.close()


def test_unit_extract_args(monkeypatch, tmp_path):
    (tmp_path / 'in.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'a.txt').write_text('This is a simple test')
    monkeypatch.chdir(tmp_path)
    result = grep.extract_args(['-c', '-E', 'needle?', 'in.txt', 'a.txt'])
    expected_names = ['in.txt', 'a.txt']
    assert result.c
    assert result.regex
    assert result.needle == 'needle?'
    for i, name in enumerate(expected_names):
        assert result.files[i].name == name


# Проверка корректности работы в случае стандартного потока ввода и отсутсвия флагов
def test_integrate_stdin_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


# Проверка корректности работы в случае стандартного потока ввода и флага -E
def test_integrate_stdin_regex_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


# Проверка корректности работы в случае стандартного потока ввода и флага -c
def test_integrate_stdin_grep_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


# Проверка корректности работы в случае одного файла и отсутсвия флагов
def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


# Проверка корректности работы в случае нескольких файлов и отсутствия флагов
def test_integrate_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


# Проверка корректности работы в случае нескольких файлов и флага -c
def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


# Проверка корректности работы в случае стандартного потока ввода и флага -c
def test_integrate_stdin_grep_regex_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nnedle suf\nthe needl\npref ne*edl?e suf\npref neeeeeede'))
    grep.main(['-c', 'ne*edl?e'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


# Проверка корректности работы в случае нескольких файлов и флага -E
def test_integrate_files_regex_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'ne*d?le', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


# Проверка корректности работы в случае нескольких файлов и флагов -c -E
def test_integrate_files_grep_regex_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '-c', 'n*edle?', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:2\na.txt:2\n'
