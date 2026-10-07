#!/usr/bin/env python3
"""The archive of every newest edition, from staging to the root catalog.

Builds a temp tree with one plain collection (in EPSG:3035, with crop columns)
and one parts collection (lon/lat, no crop columns, two parts), and checks:

- every latest file is an input, a parts collection with all its parts;
- each is reprojected to lon/lat and narrowed to the same columns, a missing
  column NULL and a missing ``collection`` the collection id;
- tylertoo tiles them into one archive, and root_tiles.json records it;
- catalogize links it from the root (a pmtiles link; no asset, which Portolan
  forbids on a catalog) and writes the README section from those facts;
- upload_data.py --root uploads exactly that one file, to the prefix root.

Needs duckdb with the spatial extension and tylertoo, so it SKIPs where those
are missing (CI installs only the validators).

Run: python tests/test_root_tiles.py
"""
import importlib.util
import sys
import tempfile
from pathlib import Path

if not all(importlib.util.find_spec(m) for m in ("duckdb", "requests", "tylertoo")):
    print("SKIP: duckdb/requests/tylertoo not installed; run in the pixi environment")
    raise SystemExit(0)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fixtures import point_tooling_at, write_parquet  # noqa: E402

import catalogize  # noqa: E402
import root_tiles  # noqa: E402
import upload_data  # noqa: E402
from common import ROOT_TILES, duckdb_connect, quote, write_json  # noqa: E402

errors: list[str] = []


def check(ok: bool, message: str) -> None:
    if not ok:
        errors.append(message)


def to_3035(path: Path) -> None:
    """Rewrite a lon/lat fixture in EPSG:3035 with a crop column and no ``collection``."""
    tmp = path.with_suffix(".tmp")
    duckdb_connect().execute(
        f"""COPY (SELECT id, ST_Transform(geometry, 'EPSG:4326', 'EPSG:3035', always_xy := true) AS geometry,
                  "metrics:area", 'W' AS "crop:code"
            FROM read_parquet({quote(path)})) TO {quote(tmp)} (FORMAT parquet)"""
    )
    # duckdb writes no CRS for a transformed geometry; state it as GeoParquet does
    import json

    import pyarrow.parquet as pq

    table = pq.read_table(tmp)
    geo = json.loads(table.schema.metadata[b"geo"])
    geo["columns"]["geometry"]["crs"] = {"id": {"authority": "EPSG", "code": 3035}}
    pq.write_table(table.replace_schema_metadata({**table.schema.metadata, b"geo": json.dumps(geo).encode()}), path)
    tmp.unlink()


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    point_tooling_at(root, catalogize, root_tiles, upload_data)
    root_tiles.WORK_DIR = root / "staging" / "_root_tiles"
    root_tiles.PMTILES = root / "staging" / ROOT_TILES
    (root_tiles.WORK_DIR / "tmp").mkdir(parents=True)

    write_json(root / "catalog" / "aa" / "collection.json", {"id": "aa", "assets": {"data": {"href": "./latest/aa.parquet"}}})
    write_json(root / "catalog" / "pp" / "collection.json", {"id": "pp", "assets": {}})
    to_3035(write_parquet(root / "staging" / "aa" / "latest" / "aa.parquet", 10.0, [2024] * 50))
    write_parquet(root / "staging" / "pp" / "latest" / "pp_one.parquet", 11.0, [2024] * 20)
    write_parquet(root / "staging" / "pp" / "latest" / "pp_two.parquet", 12.0, [2024] * 30)

    found = root_tiles.inputs()
    check([(c, f.name) for c, f in found] == [("aa", "aa.parquet"), ("pp", "pp_one.parquet"), ("pp", "pp_two.parquet")], f"inputs: {found}")

    prepared = [(c, root_tiles.prepare(c, f)) for c, f in found]
    con = duckdb_connect()
    schemas = {tuple(r[0] for r in con.execute(f"DESCRIBE SELECT * FROM read_parquet({quote(p)})").fetchall()) for _, p in prepared}
    check(len(schemas) == 1, f"one schema over all inputs, got {schemas}")
    aa = con.execute(f"""SELECT any_value(collection), min(bbox.xmin), any_value("crop:code") FROM read_parquet({quote(prepared[0][1])})""").fetchone()
    check(aa[0] == "aa" and abs(aa[1] - 10.0) < 1e-6 and aa[2] == "W", f"aa reprojected to lon/lat with its crop column: {aa}")
    pp = con.execute(f"""SELECT any_value(collection), count("crop:code") FROM read_parquet({quote(prepared[1][1])})""").fetchone()
    check(pp == ("pp", 0), f"pp: collection filled in, missing crop column NULL: {pp}")

    root_tiles.tile(prepared)
    facts = catalogize.read_json(root / "root_tiles.json")
    check((root / "staging" / ROOT_TILES).stat().st_size == facts["file:size"], "root_tiles.json records the archive's size")
    check(facts["features"] == 100 and [i["rows"] for i in facts["inputs"]] == [50, 20, 30], f"facts: {facts['features']} features, {facts['inputs']}")

    catalog = {"stac_extensions": [], "links": []}
    readme = catalogize.root_tiles(catalog, "https://example.org/hfd", "https://example.org/repo")
    check("assets" not in catalog, "no asset on the catalog (rashid PTL-AST-005)")
    check([(link["href"], link["pmtiles:layers"]) for link in catalog["links"] if link["rel"] == "pmtiles"] == [(f"./{ROOT_TILES}", ["fields"])], "pmtiles link with layer fields")
    check((root / "catalog" / ROOT_TILES).is_symlink(), "archive linked into catalog/ for the link gate")
    check(any("2 collections (3 files)" in line and "100 features" in line for line in readme), f"README section from the facts: {readme[:3]}")

    uploads = upload_data.collect_root("hfd")
    check([u.key for u in uploads] == [f"hfd/{ROOT_TILES}"], f"upload --root: {[u.key for u in uploads]}")

for e in errors:
    print(f"FAIL: {e}")
print(f"{'FAILED' if errors else 'ok'}: root tiles")
raise SystemExit(1 if errors else 0)
