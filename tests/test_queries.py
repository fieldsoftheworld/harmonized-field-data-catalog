#!/usr/bin/env python3
"""The tested queries in the generated docs return what they claim.

- md_query refuses a query without rows: an empty result reads as a broken recipe;
- with `collections`, it refuses a result that misses a collection or names one too many;
- every_collection reads a collection from catalog/ where its data is linked there and
  from the bucket otherwise (also where a link points nowhere), so the root queries see every collection in any checkout;
- the point recipe starts from a field, not from the centre of the bounding box, takes
  lon/lat, and buffers by 0.005° instead of 500 where the CRS is in degrees.

Needs duckdb with the spatial extension, so it SKIPs where that is missing.

Run: python tests/test_queries.py
"""
import importlib.util
import sys
import tempfile
from pathlib import Path

if not all(importlib.util.find_spec(m) for m in ("duckdb", "requests", "pyproj")):
    print("SKIP: duckdb/requests/pyproj not installed; run in the pixi environment")
    raise SystemExit(0)

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from fixtures import write_parquet  # noqa: E402

import catalogize  # noqa: E402
from common import duckdb_connect, quote  # noqa: E402

errors: list[str] = []


def check(ok: bool, what: str) -> None:
    if not ok:
        errors.append(what)


def raises(fn, *args, **kwargs) -> str:
    try:
        fn(*args, **kwargs)
    except RuntimeError as exc:
        return str(exc)
    return ""


tmp = Path(tempfile.mkdtemp())

# -- md_query ------------------------------------------------------------------------
shown = "SELECT 1 AS n WHERE false;"
check("no rows" in raises(catalogize.md_query, shown, "https://example.org", run=shown), "an empty result is accepted")
rows = "SELECT * FROM (VALUES ('a', 1), ('b', 2)) t(collection, fields)"
check(catalogize.md_query(rows, "https://example.org", run=rows, collections=["a", "b"]).count("\n-- ") == 3, "a complete result is not rendered")
message = raises(catalogize.md_query, rows, "https://example.org", run=rows, collections=["a", "b", "c"])
check("2 of 3" in message and "missing: c" in message, f"a missing collection is not reported: {message!r}")
message = raises(catalogize.md_query, rows, "https://example.org", run=rows, collections=["a"])
check("not in the catalog: b" in message, f"an extra collection is not reported: {message!r}")

# -- every_collection ----------------------------------------------------------------
catalogize.CATALOG_DIR = tmp / "catalog"
write_parquet(catalogize.CATALOG_DIR / "here" / "latest" / "here.parquet", 5.0, [2025])
config = {"write_prefix": "s3://bucket/prefix"}
sources = catalogize.every_collection(["here", "there"], "latest/*.parquet", config)
check(quote(f"{(catalogize.CATALOG_DIR / 'here').as_posix()}/latest/*.parquet") in sources, f"a linked collection is not read locally: {sources}")
check("'s3://bucket/prefix/there/latest/*.parquet'" in sources, f"an unlinked collection is not read from the bucket: {sources}")
broken = catalogize.CATALOG_DIR / "stale" / "latest" / "stale.parquet"
broken.parent.mkdir(parents=True)
broken.symlink_to(tmp / "nowhere.parquet")
check("'s3://bucket/prefix/stale/latest/*.parquet'" in catalogize.every_collection(["stale"], "latest/*.parquet", config), "a broken link is read locally")
catalogize.REMOTE = True
check("'s3://bucket/prefix/here/latest/*.parquet'" in catalogize.every_collection(["here"], "latest/*.parquet", config), "--remote still reads catalog/")
catalogize.REMOTE = False

# -- point recipe --------------------------------------------------------------------
# Two fields far apart, in lon/lat: the centre of their bounding box has no field near it.
two = tmp / "two.parquet"
duckdb_connect().execute(
    f"""COPY (SELECT * FROM (VALUES ('west', ST_MakeEnvelope(5.000, 52.0, 5.001, 52.001), 6000.0),
                                    ('east', ST_MakeEnvelope(6.000, 52.0, 6.001, 52.001), 6000.0))
              t(id, geometry, "metrics:area")) TO {quote(two)} (FORMAT parquet)"""
)
bbox = [5.0, 52.0, 6.001, 52.001]
lon, lat = catalogize.field_point(two, "EPSG:4326", bbox)
check(5.0 <= lon <= 5.001 and 52.0 <= lat <= 52.001, f"the point ({lon}, {lat}) is not inside the nearest field")
sentence, sql = catalogize.point_recipe(two, two.as_posix(), "EPSG:4326", bbox, has_area=True)
check("0.005°" in sentence and "), 0.005))" in sql, f"a CRS in degrees is buffered by 500: {sql}")
check(f"ST_Point({lon:.4f}, {lat:.4f})" in sql and "always_xy := true" in sql, f"the point is not given in lon/lat: {sql}")
found = duckdb_connect().execute(sql.split("\n", 1)[1]).fetchall()
check([r[0] for r in found] == ["west"], f"the recipe finds {found}, not the west field")

# The same field in a projected CRS: 500 m.
rd = tmp / "rd.parquet"
duckdb_connect().execute(
    f"""COPY (SELECT 'f' AS id, ST_MakeEnvelope(155000, 463000, 155100, 463100) AS geometry, 10000.0 AS "metrics:area")
        TO {quote(rd)} (FORMAT parquet)"""
)
sentence, sql = catalogize.point_recipe(rd, rd.as_posix(), "EPSG:28992", [5.38, 52.15, 5.40, 52.17], has_area=True)
check("500 m" in sentence and "), 500))" in sql, f"a projected CRS is not buffered by 500 m: {sql}")
found = duckdb_connect().execute(sql.split("\n", 1)[1]).fetchall()
check(len(found) == 1, f"the projected recipe finds {found}")

if errors:
    print("FAIL:\n  " + "\n  ".join(errors))
    raise SystemExit(1)
print("ok: tested queries")
