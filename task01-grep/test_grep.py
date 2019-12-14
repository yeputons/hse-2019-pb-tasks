#!/usr/bin/env python3
import io
import grep


def test_unit_print_formatted_lines_count(monkeypatch, tmp_path, capsys):
    (tmp_path / 'a.txt').write_text('Shes got a red coat with a hood.\n')
    monkeypatch.chdir(tmp_path)
    f = open('a.txt', 'r')
    grep.print_formatted_lines(['She loves the coat.',
                                'Shes got a red coat with a hood.'], f, 1, False, False, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_unit_print_formatted_lines(monkeypatch, tmp_path, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle sufer')
    monkeypatch.chdir(tmp_path)
    f = open('a.txt', 'r')
    grep.print_formatted_lines(['She loves the coat.'], f, 1, False, False, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'She loves the coat.\n'


def test_unit_print_formatted_lines_only_name_of_file(monkeypatch, tmp_path, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    f = open('a.txt', 'r')
    grep.print_formatted_lines(['She loves the coat.'], f, 1, False, True, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_unit_check_line_regex_inversion():
    a = 'We ve known each other for so long'
    assert not grep.check_line('v+', a, True, False, False, True)


def test_unit_check_line_regex_whole_line():
    a = 'V'
    assert not grep.check_line('v+', a, True, True, False, False)


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


def test_integrate_stdin_regex_iflag_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'We ve known each other for so long\n'
        'Your hearts been aching but youre too shy to say it\n'
        'Inside we both know whats been going on\n'))
    grep.main(['-Ei', 'v+'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'We ve known each other for so long\n'


def test_integrate_stdin_grep_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_stdin_grep_count_inversion(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'This is the story of Little Red Riding Hood.\n'
        'Shes got a red coat with a hood.\n'
        'She loves the coat.\n'
        'She wears it every day.\n'
        'Shes very happy today.\n'
        'Its her coat.\n'
        'qweqwcoatqweiu'))
    grep.main(['-cv', 'coat'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_stdin_grep_regex_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        ';asjjpqw\nrandomstringvvv\nnoletterin\nonevinthisstring\nlkasjloija'))
    grep.main(['-c', '-E', 'v+'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_stdin_grep_ignore_case_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO('ASD\nasd\nAsD\naSd'))
    grep.main(['-ci', 'Asd'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_integrate_file_empty_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_integrate_file_grep_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('We ve known each other for so long\n'
                                    'Your hearts been aching but youre too shy to\n'
                                    'Inside we both know whats been going on\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'v+', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'We ve known each other for so long\n'


def test_integrate_file_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text(
        'This is the story of Little Red Riding Hood.\n'
        'Shes got a red coat with a hood.\n'
        'She loves the coat.\n'
        'She wears it every day.\n'
        'Shes very happy today.\n'
        'Its her coat.\n'
        'qweqwcoatqweiu')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'coat', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


def test_integrate_file_grep_regex_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text(';asjjpqw\nrandomstringvvv\n'
                                    'noletterin\nonevinthisstring\nlkasjloija')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'v+', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_file_empty_grep_regex_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'v+', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '0\n'


def test_integrate_file_grep_whole_line_file_no_line(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('We ve known each other for so long\n'
                                    'Your hearts been aching but youre too shy to\n'
                                    'Inside we both know whats been going on\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-x', '-L', 'We ve known each other for so long\n', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


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


def test_integrate_files_grep_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('We ve known each other for so long\n'
                                    'Your hearts been aching but youre too shy to\n')
    (tmp_path / 'b.txt').write_text('Shes got a red coat with a hood.\n'
                                    'She loves the coat.\n'
                                    'She wears it every day.\n')
    (tmp_path / 'c.txt').write_text('noletter\n'
                                    'weoiriojjsdoif\n'
                                    'oiuasueoianlkns\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'v+', 'a.txt', 'b.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:We ve known each other for so long\n' \
                  'b.txt:She loves the coat.\nb.txt:She wears it every day.\n'


def test_integrate_files_grep_regex_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('noletterin\nonevinthisstring\nlkasjloija')
    (tmp_path / 'b.txt').write_text('noa\nimeennoe\nalkdl\nasjdop')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'v+', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:0\na.txt:1\n'


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


def test_integrate_files_grep_regex_inverted(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('We ve known each other for so longd\n'
                                    'Your hearts been aching but youre too shy to\n')
    (tmp_path / 'b.txt').write_text('Shes got a red coat with a hosod.\n'
                                    'She loves the coat.\n'
                                    'She wears it every day.\n')
    (tmp_path / 'c.txt').write_text('noletterf\n'
                                    'weoiriojjsdoiff\n'
                                    'oiuasueoianlknsf\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '-v', 'v+', 'a.txt', 'b.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:Your hearts been aching but youre too shy to\n' \
                  'b.txt:Shes got a red coat with a hosod.\nc.txt:noletterf\n' \
                  'c.txt:weoiriojjsdoiff\nc.txt:oiuasueoianlknsf\n'
