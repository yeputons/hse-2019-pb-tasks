import io
import argparse
import grep

input_first = 'it was very funny\n' \
              'he saw this object\n' \
              'summer was cold\n' \
              'saint clause was in my home\n'
input_second = 'yes, when i was a child\n' \
               'i had too many love\n' \
               'it was cool. and now\n' \
               'i remember about it with love'


# integrate test for standard input without flags
def test_integrate_first(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(input_first))
    grep.main(['was'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'it was very funny\n' \
                  'summer was cold\n' \
                  'saint clause was in my home\n'


# integrate test for standard input with flag -E
def test_integrate_second(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(input_first))
    grep.main(['-E', r'\s[c][a-z]*'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'summer was cold\n' \
                  'saint clause was in my home\n'


# integrate test for standard input with flag -c
def test_integrate_third(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(input_first))
    grep.main(['-c', 'was'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


# integrate test for standard input with flag -E and flag -c
def test_integrate_fourth(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(input_first))
    grep.main(['-c', '-E', r'\s[c][a-z]*'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


# integrate test for one file without flags
def test_integrate_fifth(tmp_path, monkeypatch, capsys):
    files = {'first.txt': input_first}

    for file in files:
        (tmp_path / file).write_text(files[file])
    monkeypatch.chdir(tmp_path)
    grep.main(['was', 'first.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'it was very funny\n' \
                  'summer was cold\n' \
                  'saint clause was in my home\n'


# integrate test for one file with flag -E
def test_integrate_sixth(tmp_path, monkeypatch, capsys):
    files = {'first.txt': input_first}

    for file in files:
        (tmp_path / file).write_text(files[file])
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', r'\s[c][a-z]*', 'first.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'summer was cold\n' \
                  'saint clause was in my home\n'


# integrate test for one file with flag -E
def test_integrate_seventh(tmp_path, monkeypatch, capsys):
    files = {'first.txt': input_first}

    for file in files:
        (tmp_path / file).write_text(files[file])
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'was', 'first.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


# integrate test for one file with flag -c and flag -E
def test_integrate_eighth(tmp_path, monkeypatch, capsys):
    files = {'first.txt': input_first}

    for file in files:
        (tmp_path / file).write_text(files[file])
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', r'\s[c][a-z]*', 'first.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


# integrate test for some files without flags
def test_integrate_ninth(tmp_path, monkeypatch, capsys):
    files = {'first.txt': input_first,
             'second.txt': input_second}

    for file in files:
        (tmp_path / file).write_text(files[file])
    monkeypatch.chdir(tmp_path)
    grep.main(['was', 'first.txt', 'second.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'first.txt:it was very funny\n' \
                  'first.txt:summer was cold\n' \
                  'first.txt:saint clause was in my home\n' \
                  'second.txt:yes, when i was a child\n' \
                  'second.txt:it was cool. and now\n'


# integrate test for some files with flag -E
def test_integrate_tenth(tmp_path, monkeypatch, capsys):
    files = {'first.txt': input_first,
             'second.txt': input_second}

    for file in files:
        (tmp_path / file).write_text(files[file])
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', r'\s[c][a-z]*', 'first.txt', 'second.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'first.txt:summer was cold\n' \
                  'first.txt:saint clause was in my home\n' \
                  'second.txt:yes, when i was a child\n' \
                  'second.txt:it was cool. and now\n'


# integrate test for some files with flag -c
def test_integrate_eleventh(tmp_path, monkeypatch, capsys):
    files = {'first.txt': input_first,
             'second.txt': input_second}

    for file in files:
        (tmp_path / file).write_text(files[file])
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'was', 'first.txt', 'second.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'first.txt:3\n' \
                  'second.txt:2\n'


# integrate test for some files with flag -c and flag -E
def test_integrate_twelfth(tmp_path, monkeypatch, capsys):
    files = {'first.txt': input_first,
             'second.txt': input_second}

    for file in files:
        (tmp_path / file).write_text(files[file])
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', r'\s[c][a-z]*', 'first.txt', 'second.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'first.txt:2\n' \
                  'second.txt:2\n'


# first white box test for function 'print_data'
# in this test we check the'if'
def test_print_data_first(capsys):
    data = [{'name': 'first.txt', 'lines': ['it was very funny', 'he saw this object']},
            {'name': 'second.txt', 'lines': ['summer was cold', 'saint clause was in my home']}]
    args = argparse.Namespace(count=True, name_with_str=False, name_without_str=False, full_find=False,
                              ignore_case=False, files=['first.txt', 'second.txt'], regex=True, substring='[s][g]+')

    grep.print_data(data, args)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'first.txt:2\n' \
                  'second.txt:2\n'


# second white box test for function 'print_data'
# in this test we check the'if'
def test_print_data_second(capsys):
    data = [{'name': '', 'lines': ['it was very funny', 'he saw this object']}]
    args = argparse.Namespace(count=True, name_with_str=False, name_without_str=False, full_find=False,
                              ignore_case=False, files=[], regex=True, substring='[s][g]+')

    grep.print_data(data, args)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


# third white box test for function 'print_data'
# in this test we check the 'else'
def test_print_data_third(capsys):
    data = [{'name': 'first.txt', 'lines': ['it was very funny']},
            {'name': 'second.txt', 'lines': ['saint clause was in my home']}]
    args = argparse.Namespace(count=False, name_with_str=False, name_without_str=False, full_find=False,
                              ignore_case=False, files=['first.txt', 'second.txt'], regex=True, substring='[s][g]+')

    grep.print_data(data, args)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'first.txt:it was very funny\n' \
                  'second.txt:saint clause was in my home\n'


# fourth white box test for function 'print_data'
# in this test we check the 'else'
def test_print_data_fourth(capsys):
    data = [{'name': 'first.txt', 'lines': ['it was very funny']}]
    args = argparse.Namespace(count=False, name_with_str=False, name_without_str=False, full_find=False,
                              ignore_case=False, files=['first.txt'], regex=True, substring='[s][g]+')

    grep.print_data(data, args)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'it was very funny\n'


# first white box test for function 'take_strings'
# in this test we check the 'if'
def test_take_string_first(monkeypatch):
    name_file = ''

    monkeypatch.setattr('sys.stdin', io.StringIO('my mother always said\n'
                                                 'life is like box a chocolates'))
    data = grep.take_strings(name_file)
    assert data == ['my mother always said\n',
                    'life is like box a chocolates']


# second white box test for function 'take_strings'
# in this test we check the 'else'
def test_take_string_second(tmp_path, monkeypatch):
    name_file = 'first.txt'

    (tmp_path / name_file).write_text('no one knows\n'
                                      'what is inside')
    monkeypatch.chdir(tmp_path)
    data = grep.take_strings(name_file)
    assert data == ['no one knows\n',
                    'what is inside']


# first white box test for function 'search'
# in this test we check the 'if'
def test_search_first(monkeypatch):
    args = argparse.Namespace(count=False, name_with_str=False, name_without_str=False, full_find=False,
                              ignore_case=False, files=[], regex=True, substring=r'\s[c][a-z]*')
    monkeypatch.setattr('sys.stdin', io.StringIO(input_first))

    data = grep.search(args)
    assert data[0]['name'] == ''
    assert data[0]['lines'] == ['summer was cold', 'saint clause was in my home']


# second white box test for function 'search'
# in this test we check the 'else'
def test_search_second(tmp_path, monkeypatch):
    args = argparse.Namespace(count=False, name_with_str=False, name_without_str=False, full_find=False,
                              ignore_case=False, files=['first.txt'], regex=False, substring=r'that')
    (tmp_path / 'first.txt').write_text('But is not\nthat enough?')
    monkeypatch.chdir(tmp_path)

    data = grep.search(args)
    assert data[0]['name'] == 'first.txt'
    assert data[0]['lines'] == ['that enough?']


# first white box test for function 'make_parameters'
def test_make_parameters_first():
    command = ['here', 'first.txt', 'second.txt']

    args = grep.make_parameters(command)
    assert args.files == ['first.txt', 'second.txt']
    assert args.substring == 'here'
    assert not args.regex
    assert not args.count


# second white box test for function 'make_parameters'
def test_make_parameters_second():
    command = ['-E', r'\s[z]+[t]']

    args = grep.make_parameters(command)
    assert args.files == []
    assert args.substring == r'\s[z]+[t]'
    assert args.regex
    assert not args.count


# third white box test for function 'make_parameters'
def test_make_parameters_third():
    command = ['-c', 'hope', 'first.txt']

    args = grep.make_parameters(command)
    assert args.files == ['first.txt']
    assert args.substring == 'hope'
    assert not args.regex
    assert args.count


# fourth white box test for function 'make_parameters'
def test_make_parameters_fourth():
    command = ['-c', '-E', '[0-9]+', 'first.txt', 'second.txt', 'third.txt']

    args = grep.make_parameters(command)
    assert args.files == ['first.txt', 'second.txt', 'third.txt']
    assert args.substring == '[0-9]+'
    assert args.regex
    assert args.count
