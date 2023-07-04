#!/usr/bin/env python3
"""Python Project Creator."""
import argparse
import datetime
import re
from pathlib import Path
from typing import Optional

VERSION = "1.1.0"

_RE_NAME = re.compile(r"^[a-z][a-z0-9]+$")
_RE_DESCR = re.compile(r'description = "(?P<descr>.*)"')


def create(name: str, path: Path, description: str = None, user: str = None, year: str = None, force: bool = False):
    """Create New Python Project From Template Directory."""
    # pylint: disable=too-many-arguments
    if not _RE_NAME.match(name):
        raise ValueError(f"Invalid name: {name}")
    pyprojectpath = path / "pyproject.toml"
    if not description:
        description = _detect_description(pyprojectpath)
    if not description:
        raise ValueError("Description required")
    meta = {
        "name": name,
        "name_underline": "=" * len(name),
        "description": description,
        "description_underline": "=" * len(description),
        "user": user or "nbiotcloud",
        "year": year or datetime.datetime.now().year,
        "templateversion": VERSION,
    }
    basepath = Path(__file__).parent
    if not pyprojectpath.exists() or force:
        tplpaths = [basepath / "templates", basepath / "templates-update"]
    else:
        tplpaths = [basepath / "templates-update"]
    _create(tplpaths, path, meta)


def _detect_description(pyprojectpath: Path) -> Optional[str]:
    if pyprojectpath.exists():
        with open(pyprojectpath, encoding="utf-8") as file:
            for line in file:
                match = _RE_DESCR.match(line.rstrip())
                if match:
                    return match.group("descr")
    return None


def _create(tplpaths, dstpath, meta):
    for tplpath in tplpaths:
        for abstplpath in tplpath.iterdir():
            relpath = abstplpath.relative_to(tplpath)
            absdstpath = Path(str(dstpath / relpath).format(**meta))
            if abstplpath.is_file():
                print(f"Creating {absdstpath!s}")
                # Render single file
                absdstpath.parent.mkdir(parents=True, exist_ok=True)
                tpl = abstplpath.read_text(encoding="utf-8")
                out = tpl.format(**meta)
                absdstpath.write_text(out, encoding="utf-8")
            elif abstplpath.is_dir():
                # Process subfolder
                _create([abstplpath], absdstpath, meta)
            else:
                assert False


def main():
    """Command Line Interface."""
    parser = argparse.ArgumentParser(prog="create", description="Create Python Project")
    parser.add_argument("name", help="Project Name. Lowercase letters and numbers only. No dashes. No underscore")
    parser.add_argument("description", nargs="?")
    parser.add_argument("--path", "-C", help="Target Directory. 'name' by default")
    parser.add_argument("--user", "-u", help="User. 'nbiotcloud' by default")
    parser.add_argument("--year", "-y", help="Year. Current year by default")
    parser.add_argument("--force", action="store_true", help="Overwrite all files.")
    args = parser.parse_args()
    create(
        args.name,
        Path(args.path or args.name),
        description=args.description,
        user=args.user,
        year=args.year,
        force=args.force,
    )


if __name__ == "__main__":
    main()
