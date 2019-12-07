import io
import grep


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


def test_integrate_stdin_grep_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


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
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_integrate_file_grep_regex_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', '-c', 'needle', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_integrate_stdin_grep_regex_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-E', '-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_file_grep_regex(tmp_path, monkeypatch, capsys):
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


# tests for every new flag
def test_integrate_stdin_reverse_strings(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneeeeedle suf\nthe needl\npref needle suf'))
    grep.main(['-v', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'neeeeedle suf\nthe needl\n'


def test_integrate_stdin_ignore_case(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nkekNEEDLE heh\nthe needl\npref needle suf'))
    grep.main(['-i', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle\nkekNEEDLE heh\npref needle suf\n'


def test_integrate_stdin_fullmatch_without_reg(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle\nthe needl\nneedle '))
    grep.main(['-x', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'needle\n'


def test_integrate_stdin_fullmatch_with_reg(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle\nthe needl\nnneedle\nnneedlek'))
    grep.main(['-E', '-x', 'n?eedle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'needle\n'


def test_integrate_files_output_files_only(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('NEEDLE\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needlekek\nneedle')
    (tmp_path / 'c.txt').write_text('NEEDLE;\nneedl ')
    monkeypatch.chdir(tmp_path)
    grep.main(['-l', 'needle', 'a.txt', 'b.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nb.txt\n'


def test_integrate_files_output_files_only_reversed(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('NEEDLE\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needlekek\nneedle')
    (tmp_path / 'c.txt').write_text('NEEDLE;\nneedl ')
    monkeypatch.chdir(tmp_path)
    grep.main(['-L', 'needle', 'a.txt', 'b.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'c.txt\n'


# end of every flag tests, start of tests for (almost) random flags combinations...
def test_integrate_stdin_all_flags(tmp_path, monkeypatch, capsys):
    (tmp_path / 'b.txt').write_text('the needle NEEDLE kekneedlekek\n'
                                    'pref suf\nsuf pref\nneedleneedleneedle')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', '-i', '-x', '-v', 'needle', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


def test_integrate_files_output_mode_normal(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('NEEDLE\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needlekek\nneedle')
    (tmp_path / 'c.txt').write_text('NEEDLE;\nneedl ')
    monkeypatch.chdir(tmp_path)
    grep.main(['-l', '-E', '-i', '-x', '-v', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\na.txt\nc.txt\n'


def test_integrate_files_output_mode_reversed(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('NEEDLE\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needlekek\nneedlekek\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-L', '-E', '-i', '-x', '-v', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '\n'


def test_integrate_files_output_mode_reversed_2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('NEEDLE\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needlekek\nneedle\n')
    (tmp_path / 'c.txt').write_text('NEEDLE\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-L', '-E', '-i', '-x', '-v', 'needle', 'b.txt', 'a.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'c.txt\n'


def test_integrate_files_fullmatch_without_regular(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('NEEDLE\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needlekek\nneedle\n')
    (tmp_path / 'c.txt').write_text('NEEDLE\n')
    monkeypatch.chdir(tmp_path)
    grep.main(['-i', '-x', '-v', 'needle', 'a.txt', 'b.txt', 'c.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:needle suf\nb.txt:the needlekek\n'
