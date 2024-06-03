#!/bin/bash

set -e

# Create/Enter Python Environment
if [ ! -e .venv ];
then
    python3 -m venv .venv
    source .venv/bin/activate
    pip install tox "poetry>=1.4" isort black pylint nox
else
    source .venv/bin/activate
fi

isort -l 120 create.py
black -l 120 create.py
pylint --max-line-length 120 create.py
rm -rf testdata
python3 create.py myname "My Long Description" -C testdata/myname
