#!/usr/bin/env python3
"""Python Project Creator."""
import argparse
import datetime
import pathlib
import re

_RE_NAME = re.compile(r"^[a-z][a-z0-9]+$")


def create(name: str, description: str, path: pathlib.Path, user: str = None, year: str = None):
    """Create New Python Project From Template Directory."""
    if not _RE_NAME.match(name):
        raise ValueError(f"Invalid name: {name}")
    meta = {
        "name": name,
        "name_underline": "=" * len(name),
        "description": description,
        "description_underline": "=" * len(description),
        "user": user or "nbiotcloud",
        "year": year or datetime.datetime.now().year,
    }
    tplpath = pathlib.Path(__file__).parent / "templates"
    _create(tplpath, path, meta)


def _create(tplpath, dstpath, meta):
    for abstplpath in tplpath.iterdir():
        relpath = abstplpath.relative_to(tplpath)
        absdstpath = pathlib.Path(str(dstpath / relpath).format(**meta))
        if abstplpath.is_file():
            print(f"Creating {absdstpath!s}")
            # Render single file
            absdstpath.parent.mkdir(parents=True, exist_ok=True)
            tpl = abstplpath.read_text(encoding="utf-8")
            out = tpl.format(**meta)
            absdstpath.write_text(out, encoding="utf-8")
        elif abstplpath.is_dir():
            # Process subfolder
            _create(abstplpath, absdstpath, meta)
        else:
            assert False


def main():
    """Command Line Interface."""
    parser = argparse.ArgumentParser(prog="create", description="Create Python Project")
    parser.add_argument("name", help="Project Name. Lowercase letters and numbers only. No dashes. No underscore")
    parser.add_argument("description")
    parser.add_argument("--path", "-C", help="Target Directory. 'name' by default")
    parser.add_argument("--user", "-u", help="User. 'nbiotcloud' by default")
    parser.add_argument("--year", "-y", help="Year. Current year by default")
    args = parser.parse_args()
    create(args.name, args.description, path=pathlib.Path(args.path or args.name), user=args.user, year=args.year)


if __name__ == "__main__":
    main()
