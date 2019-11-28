#!/bin/bash
flake8_flags="--max-line-length=100"
pylint_flags="--max-line-length=100 --disable=invalid-name,missing-docstring,global-statement,too-many-lines,R --enable=simplifiable-if-statement,redefined-variable-type"
mypy_flags="--ignore-missing-imports"
files=`find . -type f -name "*.py"`

flake8 $flake8_flags $files
pylint $pylint_flags $files
mypy $mypy_flags $files