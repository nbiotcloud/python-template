Testing.

Just a simple and stupid command. We do not want to depend on the templates itself.

``
isort -l 120 create.py &&
black -l 120 create.py &&
pylint --max-line-length 120 create.py &&
python3 create.py myname "My Long Description" -y 1234 -u myuser -C testdata &&
echo PASS
``
