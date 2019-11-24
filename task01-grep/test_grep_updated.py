#!/usr/bin/env python3

import grep


def test_get_value():
    assert not grep.get_value({'aa': False}, 'aa')
    assert grep.get_value({'aa': True}, 'aa')
    assert not grep.get_value({'bb': True}, 'aa')
    assert not grep.get_value({'bb': False}, 'aa')


def test_match_ignore_case():
    assert grep.match('AAb', 'AAbtrg', {grep.IGNORE_CASE: True})
    assert grep.match('Aab', 'aABte', {grep.IGNORE_CASE: True})
    assert not grep.match('Aab', 'aAb', {grep.IGNORE_CASE: False})
    assert grep.match('', '', {})
    assert grep.match('aaa', 'AaA', {grep.REGEX: True, grep.IGNORE_CASE: True})
    assert grep.match('aa?a', 'AA', {grep.REGEX: True, grep.IGNORE_CASE: True})
    assert not grep.match(
        'ab?a', 'aBba', {grep.REGEX: True, grep.IGNORE_CASE: True})


def test_search_needle_in_src_inverted():
    needle = 'abab'
    src = []
    assert grep.search_needle_in_src(
        needle, src, {grep.REGEX: False, grep.INVERTED: True}) == []
    src = ['qababr', 'qadbab', 'quabab']
    assert grep.search_needle_in_src(
        needle, src, {grep.REGEX: False, grep.INVERTED: True}) == ['qadbab']
    needle = '[1]'
    src = ['[2 ghs', ']] req', '[1e]', 'pp[1]asf']
    assert grep.search_needle_in_src(
        needle, src, {grep.REGEX: False, grep.INVERTED: False}) == ['pp[1]asf']
    needle = 'a'
    src = ['rtt', 'pq', 'cnb']
    assert grep.search_needle_in_src(
        needle, src, {grep.REGEX: True, grep.INVERTED: True}) == src


def test_match_full_match():
    assert grep.match('AAA', 'AAA', {grep.FULL_MATCH: True})
    assert grep.match(
        'AAA', 'aaa', {grep.FULL_MATCH: True, grep.IGNORE_CASE: True})
    assert grep.match('AA?A', 'AA', {grep.FULL_MATCH: True, grep.REGEX: True})
    assert not grep.match('AAA', 'AAB', {grep.FULL_MATCH: True})
    assert not grep.match(
        'AAA', 'aaaa', {grep.FULL_MATCH: True, grep.IGNORE_CASE: True})
    assert grep.match(
        'Aa*t', 'aaaaaat', {grep.FULL_MATCH: True, grep.REGEX: True, grep.IGNORE_CASE: True})


def test_file_name_found(capsys):
    grep.print_search_result({'aa.txt': ['asf', 'af', 'qwe'], 'bb.txt': [
        'fs', 'aff', 'qr']}, {grep.FILE_NAMES_FOUND: True})
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'aa.txt\nbb.txt\n'
    grep.print_search_result({}, {grep.FILE_NAMES_FOUND: True})
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_file_name_not_found(capsys):
    grep.print_search_result({'aa.txt': [], 'bb.txt': ['afsa']}, {
                             grep.FILE_NAMES_NOT_FOUND: True})
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'aa.txt\n'
