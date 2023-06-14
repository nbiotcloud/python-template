#!/bin/bash

set -e

# Create/Enter Python Environment
if [ ! -e .venv ];
then
    python3 -m venv .venv
    source .venv/bin/activate
    pip install tox "poetry>=1.4" "crashtest==0.4.1" isort black pylint
else
    source .venv/bin/activate
fi

isort -l 120 create.py
black -l 120 create.py
pylint --max-line-length 120 create.py
rm -rf testdata
python3 create.py myname "My Long Description" -y 1234 -u myuser -C testdata/myname
(cd testdata/myname && black . --check)
(cd testdata/myname && isort . --check)
(cd testdata/myname && tox)

