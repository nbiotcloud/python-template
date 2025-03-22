# MIT License
#
# Copyright (c) 2023-2025 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Test Baking."""

import os
from pathlib import Path
from shutil import copytree
from subprocess import run

from test2ref import assert_paths, assert_refdata


def test_default(cookies):
    """Default Value Testing."""
    result = cookies.bake(extra_context={"year": "2023"})

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project_path.name == "example-project"

    replacements = [(result.project_path.parent, "PRJPARENT")]
    assert_refdata(test_default, result.project_path, replacements=replacements)


def test_myname(cookies):
    """Default Value Testing."""
    extra_context = {
        "name": "myname",
        "description": "my description",
        "year": "2024",
        "user": "myuser",
    }
    result = cookies.bake(extra_context=extra_context)

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project_path.name == "myname"

    replacements = [(result.project_path.parent, "PRJPARENT")]
    assert_refdata(test_myname, result.project_path, replacements=replacements)


def test_default_build(tmp_path):
    """Build Default One."""
    path = Path(__file__).parent / "refdata" / "test_bake" / "test_default"
    copytree(path, tmp_path, dirs_exist_ok=True)

    # disable --use-current-year
    precommitconfigfile = tmp_path / ".pre-commit-config.yaml"
    precommitconfig = precommitconfigfile.read_text()
    precommitconfigpatched = precommitconfig.replace("          - --use-current-year\n", "")
    precommitconfigfile.write_text(precommitconfigpatched)

    env = dict(os.environ)
    env["VIRTUAL_ENV"] = str(tmp_path / ".venv")

    run(["git", "init", "."], check=True, cwd=tmp_path)
    run(["git", "add", "."], check=True, cwd=tmp_path)
    result = run(["make", "all"], cwd=tmp_path, check=False, env=env)
    run(["make", "distclean"], cwd=tmp_path, check=False)

    precommitconfigfile.write_text(precommitconfig)

    assert_paths(path, tmp_path, excludes=(".git",))
    assert result.returncode == 0
