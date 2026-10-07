#!/usr/bin/env python3
"""Tile the newest edition of every collection into one PMTiles archive.

Inputs are the ``latest/`` files catalogize put in place, one per collection
(one per part for a collection with parts), in the order of the collections:

    staging/<id>/latest/<id>.parquet          (or every latest/*.parquet of a parts collection)
      -> staging/_root_tiles/<stem>.parquet   OGC:CRS84, the columns in COLUMNS
      -> staging/harmonized-field-data.pmtiles, one layer ``fields``
      +  root_tiles.json                       the facts catalogize writes about it (in git, so
                                               the root can be regenerated without the archive)

tylertoo reads lon/lat or Web Mercator only, and needs one schema across all
inputs, so each file is reprojected and narrowed to COLUMNS first: a column a
collection lacks is NULL, a missing ``collection`` is the collection id. This
does not change the data; it selects and reprojects what the collections hold.

    python tools/root_tiles.py               # prepare what changed, then tile
    python tools/root_tiles.py --prepare     # prepare only

Work files live in ``staging/_root_tiles/`` (the overview is ~100 GB for every
collection) and are reused while they are newer than their source.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from common import (
    CATALOG_DIR,
    ROOT_TILES,
    ROOT_TILES_FACTS,
    ROOT_TILES_LAYER,
    STAGING_DIR,
    duckdb_connect,
    file_facts,
    parquet_crs,
    parquet_row_count,
    quote,
    read_json,
    write_json,
)

WORK_DIR = STAGING_DIR / "_root_tiles"
PMTILES = STAGING_DIR / ROOT_TILES

# name, type: the columns most collections share (fiboa core and the crop/hcat extensions)
COLUMNS = [
    ("collection", "VARCHAR"),
    ("id", "VARCHAR"),
    ("metrics:area", "FLOAT"),
    ("crop:code", "VARCHAR"),
    ("crop:name", "VARCHAR"),
    ("hcat:code", "UINTEGER"),
    ("hcat:name_en", "VARCHAR"),
]
LONLAT = {"EPSG:4326", "OGC:CRS84"}

# tylertoo's default of 10 000 rows per row group overflows Parquet's limit of
# 32 767 row groups in the overview of ~170 M features over 12 zoom levels.
OVERVIEW_OPTS = {"max_zoom": 14, "row_group_size": 50_000}
PARALLEL = 6


def inputs() -> list[tuple[str, Path]]:
    """(collection id, staged latest parquet) for every published collection."""
    found = []
    for path in sorted(CATALOG_DIR.glob("*/collection.json")):
        cid = read_json(path)["id"]
        latest = STAGING_DIR / cid / "latest"
        files = [latest / f"{cid}.parquet"] if "data" in read_json(path)["assets"] else sorted(latest.glob("*.parquet"))
        missing = [f for f in files if not f.exists()] or ([] if files else [latest / "*.parquet"])
        if missing:
            sys.exit(f"missing {missing[0]}: run `tools/build.py {cid}` first")
        found += [(cid, f) for f in files]
    return found


def projjson(src: Path) -> str:
    """The GeoParquet CRS as PROJJSON, for a CRS without an authority code
    (us_usda_cropland's Albers on NAD83); PROJ, and so ST_Transform, reads it as is."""
    con = duckdb_connect()
    for key, value in con.execute(f"SELECT key, value FROM parquet_kv_metadata({quote(src)})").fetchall():
        if bytes(key).decode() == "geo":
            geo = json.loads(bytes(value).decode())
            crs = geo["columns"][geo["primary_column"]].get("crs")
            if crs:
                return json.dumps(crs)
    sys.exit(f"{src}: no CRS in the GeoParquet metadata")


def prepare(cid: str, src: Path) -> Path:
    """Reproject one file to OGC:CRS84 and narrow it to COLUMNS."""
    dst = WORK_DIR / src.name
    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return dst
    crs = parquet_crs(src) or projjson(src)
    con = duckdb_connect()
    con.execute(f"SET temp_directory = {quote(WORK_DIR / 'tmp')}; SET memory_limit = '8GB'; SET threads = 8")
    present = {r[0] for r in con.execute(f"DESCRIBE SELECT * FROM read_parquet({quote(src)})").fetchall()}
    cols = []
    for name, typ in COLUMNS:
        expr = f'CAST("{name}" AS {typ})' if name in present else f"CAST(NULL AS {typ})"
        if name == "collection":
            expr = f"COALESCE({expr}, {quote(cid)})"
        cols.append(f'{expr} AS "{name}"')
    geom = "geometry" if crs in LONLAT else f"ST_Transform(geometry, {quote(crs)}, 'EPSG:4326', always_xy := true)"
    tmp = dst.with_suffix(".part")
    con.execute(
        f"COPY (SELECT {', '.join(cols)}, g AS geometry, "
        "struct_pack(xmin := ST_XMin(g), ymin := ST_YMin(g), xmax := ST_XMax(g), ymax := ST_YMax(g)) AS bbox "
        f"FROM (SELECT *, {geom} AS g FROM read_parquet({quote(src)}))) "
        f"TO {quote(tmp)} (FORMAT parquet, COMPRESSION zstd, ROW_GROUP_SIZE 100000)"
    )
    tmp.rename(dst)
    print(f"  prepared {dst.name} ({'PROJJSON' if crs.startswith('{') else crs}, {len(present & {c for c, _ in COLUMNS})}/{len(COLUMNS)} columns)", flush=True)
    return dst


def tile(prepared: list[tuple[str, Path]]) -> None:
    from importlib.metadata import version

    import tylertoo

    overview = WORK_DIR / "overview.parquet"
    part = PMTILES.with_suffix(".part")
    spill = WORK_DIR / "tmp"
    print(f"tylertoo {version('tylertoo')}: overview of {len(prepared)} file(s)", flush=True)
    convert = tylertoo.overview([str(p) for _, p in prepared], str(overview), spill_dir=str(spill), **OVERVIEW_OPTS)
    print("tylertoo: export", flush=True)
    export = tylertoo.export_pmtiles(str(overview), str(part), layer_name=ROOT_TILES_LAYER)
    part.rename(PMTILES)
    overview.unlink()

    print("checksum", flush=True)
    write_json(ROOT_TILES_FACTS, {
        "built": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tylertoo": version("tylertoo"),
        "options": OVERVIEW_OPTS,
        "layer": ROOT_TILES_LAYER,
        "columns": [name for name, _ in COLUMNS],
        "inputs": [{"collection": cid, "file": p.name, "rows": parquet_row_count(p)} for cid, p in prepared],
        "features": convert["input_features"],
        "empty_zooms": [z["zoom"] for z in convert.get("skipped_empty_levels", [])],
        "zooms": [{k: z[k] for k in ("zoom", "tile_count", "level_feature_count", "oversized_tiles")} for z in export["zooms"]],
        "tiles": export["total_tiles"],
        "oversized_tiles": export["oversized_tiles"],
        **file_facts(PMTILES),
    })
    print(f"wrote {PMTILES} and {ROOT_TILES_FACTS.name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--prepare", action="store_true", help="reproject and narrow the inputs, do not tile")
    args = parser.parse_args()

    (WORK_DIR / "tmp").mkdir(parents=True, exist_ok=True)
    os.environ["TMPDIR"] = str(WORK_DIR / "tmp")  # /tmp is often a small partition
    found = inputs()
    print(f"{len(found)} input file(s) from {len({c for c, _ in found})} collection(s)", flush=True)
    with ThreadPoolExecutor(PARALLEL) as pool:
        prepared = list(zip([c for c, _ in found], pool.map(lambda f: prepare(*f), found)))
    if not args.prepare:
        tile(prepared)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
