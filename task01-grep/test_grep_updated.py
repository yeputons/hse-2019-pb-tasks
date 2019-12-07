#!/usr/bin/env python3
from typing import Dict
import io
import grep


def test_unit_search_standard():
    search_flags: Dict[str, bool] = {'ignore_case': True, 'invert_ans': False,
                                     'full_match': False, 'regex': False}
    # only ignore_case flag
    assert grep.search('pYt', 'pTPypPytyP', search_flags)
    assert not grep.search('pYt', 'pTPypPyytyP', search_flags)
    search_flags['ignore_case'] = False

    # only full_match flag
    search_flags['full_match'] = True
    assert not grep.search('pyt', 'pytt', search_flags)
    assert grep.search('pyt', 'pyt', search_flags)
    search_flags['full_match'] = False

    # only invert_ans flag
    search_flags['invert_ans'] = True
    assert not grep.search('pyt', 'ptpyppytyp', search_flags)
    assert grep.search('pyt', 'ptpypptyp', search_flags)

    # ignore_case, full_match and invert_ans flags together
    search_flags['full_match'] = True
    search_flags['ignore_case'] = True
    assert grep.search('pYt', 'pTPypPytyP', search_flags)
    assert not grep.search('pyt', 'pyt', search_flags)
    assert not grep.search('Pyt', 'pYT', search_flags)


def test_unit_search_regex():
    search_flags: Dict[str, bool] = {'ignore_case': True, 'invert_ans': False,
                                     'full_match': False, 'regex': True}
    # only ignore_case flag
    assert grep.search('[P,a]yT+', 'pytT', search_flags)
    assert not grep.search('[P,a]yT+', 'pyytT', search_flags)
    search_flags['ignore_case'] = False

    # only full_match flag
    search_flags['full_match'] = True
    assert grep.search('[P,a]yT+', 'PyTT', search_flags)
    assert not grep.search('[P,a]yT+', 'PyTTPyTT', search_flags)
    search_flags['full_match'] = False

    # only invert_ans flag
    search_flags['invert_ans'] = True
    assert not grep.search('[P,a]yT+', 'pytPyTpyT', search_flags)
    assert grep.search('[P,a]yT+', 'pytPyyTpy', search_flags)

    # ignore_case, full_match and invert_ans flags together
    search_flags['full_match'] = True
    search_flags['ignore_case'] = True
    assert not grep.search('[P,a]yT+', 'pytT', search_flags)
    assert grep.search('[P,a]yT+', 'pytTpytT', search_flags)
    assert grep.search('[P,a]yT+', 'pyytT', search_flags)


def test_unit_search_in_lines_standard():
    search_flags: Dict[str, bool] = {'ignore_case': True, 'invert_ans': False,
                                     'full_match': False, 'regex': False}
    input_lines = [['a', 'pTPYpPyTyp'],
                   ['a', 'pTpyPPtYp'],
                   ['a', 'pYT'],
                   ['', 'pt`dsv>04pyT/-f'],
                   ['d', ' ']]
    answer = {'a': ['pTPYpPyTyp', 'pYT'], '': ['pt`dsv>04pyT/-f'], 'd': []}
    assert grep.search_in_lines('Pyt', input_lines, search_flags) == answer

    search_flags: Dict[str, bool] = {'ignore_case': False, 'invert_ans': True,
                                     'full_match': True, 'regex': False}
    input_lines = [['a', 'pyt'],
                   ['a', 'ptpypptyp'],
                   ['a', 'pytT'],
                   ['', 'pt`dsv>04pyt/-f'],
                   ['d', 'pyt']]
    answer = {'a': ['ptpypptyp', 'pytT'], '': ['pt`dsv>04pyt/-f'], 'd': []}
    assert grep.search_in_lines('pyt', input_lines, search_flags) == answer

    search_flags: Dict[str, bool] = {'ignore_case': True, 'invert_ans': True,
                                     'full_match': True, 'regex': False}
    input_lines = [['a', 'pyt'],
                   ['a', 'ptPYPPtyp'],
                   ['a', 'pYtT'],
                   ['', 'pt`dsv>04Pyt/-f'],
                   ['d', 'pyT']]
    answer = {'a': ['ptPYPPtyp', 'pYtT'], '': ['pt`dsv>04Pyt/-f'], 'd': []}
    assert grep.search_in_lines('Pyt', input_lines, search_flags) == answer


def test_unit_search_in_lines_regex():
    search_flags: Dict[str, bool] = {'ignore_case': True, 'invert_ans': False,
                                     'full_match': False, 'regex': True}
    input_lines = [['a', 'pTPYpPyttyp'],
                   ['a', 'pTpyPPtYp'],
                   ['a', 'AYT'],
                   ['', 'pt`dsv>04pyT/-f'],
                   ['d', 'PyyT']]
    answer = {'a': ['pTPYpPyttyp', 'AYT'], '': ['pt`dsv>04pyT/-f'], 'd': []}
    assert grep.search_in_lines('[P,a]yT+', input_lines, search_flags) == answer

    search_flags: Dict[str, bool] = {'ignore_case': False, 'invert_ans': True,
                                     'full_match': True, 'regex': True}
    input_lines = [['a', 'PyTT'],
                   ['a', 'ptpypptyp'],
                   ['a', 'pytT'],
                   ['', 'pt`dsv>04pyt/-f'],
                   ['d', 'ayT']]
    answer = {'a': ['ptpypptyp', 'pytT'], '': ['pt`dsv>04pyt/-f'], 'd': []}
    assert grep.search_in_lines('[P,a]yT+', input_lines, search_flags) == answer

    search_flags: Dict[str, bool] = {'ignore_case': True, 'invert_ans': True,
                                     'full_match': True, 'regex': True}
    input_lines = [['a', 'AyTT'],
                   ['a', 'ptpypptyp'],
                   ['a', 'pytT'],
                   ['', 'pt`dsv>04pyt/-f'],
                   ['d', 'ayT']]
    answer = {'a': ['ptpypptyp'], '': ['pt`dsv>04pyt/-f'], 'd': []}
    assert grep.search_in_lines('[P,a]yT+', input_lines, search_flags) == answer


def test_unit_print_ans_file_names(capsys):
    grep.print_ans_file_names({'a.txt': ['ptpyppytyp', 'pyt'],
                               'b.txt': ['pt`dsv>04pyt/-f'], 'c.txt': []},
                              ['a.txt', 'b.txt', 'c.txt'], True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nb.txt\n'

    grep.print_ans_file_names({'a.txt': ['ptpyppytyp', 'pyt'],
                               'b.txt': ['pt`dsv>04pyt/-f'], 'c.txt': []},
                              ['a.txt', 'b.txt', 'c.txt'], False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'c.txt\n'


def test_integrate_stdin_standard_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneeDLe? suf\nthe needl\npref Needle? suf'))
    grep.main(['-i', 'Needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneeDLe? suf\npref Needle? suf\n'

    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle?\nthe needle suf\nneedle?'))
    grep.main(['-x', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'needle?\nneedle?\n'

    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle?\nthe needl\npref neeDLe? suf'))
    grep.main(['-ivx', 'Needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nthe needl\npref neeDLe? suf\n'

    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle?\nthe needl\npref neeDLe? suf'))
    grep.main(['-civx', 'Needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_stdin_regex_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneeDLe? suf\nthe needl\npref Needle? suf'))
    grep.main(['-i', '-E', 'Needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneeDLe? suf\nthe needl\npref Needle? suf\n'

    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle?\nthe needle suf\nneedl'))
    grep.main(['-x', '-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'needl\n'

    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle?\nneedl\npref neeDLe? suf'))
    grep.main(['-ivx', '-E', 'Needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle?\npref neeDLe? suf\n'

    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle?\nneedl\npref neeDLe? suf'))
    grep.main(['-civx', '-E', 'Needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_files_standard_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref nEEdle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', 'Needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref nEEdle suf\na.txt:pref needle\na.txt:needle suf\n'

    (tmp_path / 'a.txt').write_text('needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-x', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:needle\n'

    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('needLe\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-civx', 'Needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'

    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    (tmp_path / 'c.txt').write_text('the needl\npref eedle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-l', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\na.txt\n'

    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    (tmp_path / 'c.txt').write_text('the needl\npref eedle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-L', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'c.txt\n'

    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('needLe\npref needle suf')
    (tmp_path / 'c.txt').write_text('needLe\nneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-livx', 'Needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\na.txt\n'

    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('needLe\npref needle suf')
    (tmp_path / 'c.txt').write_text('needLe\nneedle\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-Livx', 'Needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'c.txt\n'


def test_integrate_files_regex_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('neeedle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref nEEdle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', '-E', 'Needle?', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:the needl\nb.txt:pref nEEdle suf\na.txt:needle suf\n'

    (tmp_path / 'a.txt').write_text('needl\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-x', '-E', 'needle?', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:needl\n'

    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('needL\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-civx', '-E', 'Needle?', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'

    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    (tmp_path / 'c.txt').write_text('the needl\npref eedle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-l', '-E', 'needle?', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\na.txt\nc.txt\n'

    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needl suf')
    (tmp_path / 'c.txt').write_text('the nedle\npref eedle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-L', '-E', 'needle?', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'c.txt\n'

    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('needLe\npref needle suf')
    (tmp_path / 'c.txt').write_text('needLe\nneedl\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-livx', '-E', 'Needle?', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\na.txt\n'

    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('needLe\npref needle suf')
    (tmp_path / 'c.txt').write_text('needLe\nneedl\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-Livx', '-E', 'Needle?', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'c.txt\n'
