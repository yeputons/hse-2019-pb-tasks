#!/usr/bin/env python3
from typing import Dict
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


def print_ans_file_names(capsys):
    grep.print_ans_lines({'a.txt': ['ptpyppytyp', 'pyt'],
                          'b.txt': ['pt`dsv>04pyt/-f'], 'c.txt': []},
                         ['a.txt', 'b.txt', 'c.txt'], True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nb.txt\n'

    grep.print_ans_lines({'a.txt': ['ptpyppytyp', 'pyt'],
                          'b.txt': ['pt`dsv>04pyt/-f'], 'c.txt': []},
                         ['a.txt', 'b.txt', 'c.txt'], False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'c.txt\n'
