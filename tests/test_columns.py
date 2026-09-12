#!/usr/bin/env python3
"""Every item's `table:columns` describes its own file.

A column whose value is constant in one edition is stored once in the file's
collection metadata and is not a column there, so the editions of one dataset
do not agree on their column list. The items used to be stamped with the newest
edition's list: de_sh's 2023 and 2025 items claimed seven columns and omitted
`determination:datetime`, which both of those files carry.

Run: python3 tests/test_columns.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from catalogize import union_columns  # noqa: E402

errors = []


def check(ok, what):
    if not ok:
        errors.append(what)


def item(*names):
    return {"properties": {"table:columns": [{"name": n, "type": "string"} for n in names]}}


# oldest first, as the builder passes them
editions = [item("id", "geometry", "determination:datetime"), item("id", "geometry")]
names = [c["name"] for c in union_columns(editions)]

check(names == ["id", "geometry", "determination:datetime"], f"newest first, then the rest: {names}")
check(len(union_columns([item("id"), item("id")])) == 1, "a column is listed once")
check(union_columns([]) == [], "no editions, no columns")

one = union_columns([item("id", "geometry")])
check([c["name"] for c in one] == ["id", "geometry"], "a single edition is itself")

# the union keeps the newest edition's description of a column both carry
newest = {"properties": {"table:columns": [{"name": "id", "type": "string", "description": "new"}]}}
oldest = {"properties": {"table:columns": [{"name": "id", "type": "string", "description": "old"}]}}
check(union_columns([oldest, newest])[0]["description"] == "new", "the newest description wins")

if errors:
    print("\n".join(f"error  {e}" for e in errors))
    raise SystemExit(1)
print("OK: the collection lists every edition's columns, newest first")
