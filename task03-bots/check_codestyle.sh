#!/bin/bash
flake8_flags="--max-line-length=100"
pylint_flags="--max-line-length=100 --disable=invalid-name,missing-docstring,global-statement,too-many-lines,R --enable=simplifiable-if-statement,redefined-variable-type"
mypy_flags="--ignore-missing-imports"
for file in `find . -type f -name "*.py"`
do
   flake8 $flake8_flags $file;
done

flake8 $flake8_flags `find . -type f -name "*.py"`
pylint $pylint_flags `find . -type f -name "*.py"`
mypy $mypy_flags `find . -type f -name "*.py"`