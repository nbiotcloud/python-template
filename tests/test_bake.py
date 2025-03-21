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
    env = dict(os.environ)
    env["VIRTUAL_ENV"] = str(tmp_path / ".venv")
    run(["git", "init", "."], check=True, cwd=tmp_path)
    run(["git", "add", "."], check=True, cwd=tmp_path)
    result = run(["make", "all"], cwd=tmp_path, check=False, env=env)
    run(["make", "distclean"], cwd=tmp_path, check=False)
    assert_paths(path, tmp_path, excludes=(".git",))
    assert result.returncode == 0
