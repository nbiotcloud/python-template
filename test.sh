#!/bin/bash

set -e

# Create/Enter Python Environment
if [ ! -e .venv ];
then
    python3 -m venv .venv
    source .venv/bin/activate
    pip install tox "poetry>=1.4" nox pre-commit
else
    source .venv/bin/activate
fi

pre-commit run --all-files
rm -rf testdata
python3 create.py myname "My Long Description" -C testdata/myname
