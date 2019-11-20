#!/usr/bin/env python3

import grep


def test_match_ignore_case():
    assert grep.match('AAb', 'AAbtrg', {grep.IGNORE_CASE: True})
    assert grep.match('Aab', 'aABte', {grep.IGNORE_CASE: True})
    assert not grep.match('Aab', 'aAb', {grep.IGNORE_CASE: False})
    assert grep.match('', '', {})
    assert grep.match('aaa', 'AaA', {grep.REGEX: True, grep.IGNORE_CASE: True})
    assert grep.match('aa?a', 'AA', {grep.REGEX: True, grep.IGNORE_CASE: True})
    assert not grep.match(
        'ab?a', 'aBba', {grep.REGEX: True, grep.IGNORE_CASE: True})
