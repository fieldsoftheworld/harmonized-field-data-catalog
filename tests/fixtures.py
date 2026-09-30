"""Tiny staged datasets for tests that run the tooling end to end on a temp tree.

Writes what build.py would leave in staging/ — GeoParquet, the staged STAC
record, the converter metadata — without fiboa-cli, and points the tooling at
the temp tree. Needs duckdb with the spatial extension (the pixi environment).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import common  # noqa: E402
from common import PARQUET_TYPE, duckdb_connect, file_facts, parquet_row_count, quote, write_json  # noqa: E402


def write_parquet(path: Path, x0: float, years: list[int], hoist_year: bool = False) -> Path:
    """One small square field per entry of ``years``, in a row eastward from (x0, 47).

    ``hoist_year`` stores a year that is the same for every row once in the
    ``collection`` metadata instead of as a column, as vecorel does.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    values = ", ".join(f"({i}, {y})" for i, y in enumerate(years))
    date = "" if hoist_year else ', make_timestamp(y, 1, 1, 0, 0, 0) AS "determination:datetime"'
    kv = f", KV_METADATA {{collection: '{json.dumps({'determination:datetime': f'{years[0]}-01-01T00:00:00Z'})}'}}" if hoist_year else ""
    x = f"({x0} + i * 0.001)"
    duckdb_connect().execute(
        f"""COPY (
          SELECT 'f' || i AS id,
                 ST_MakeEnvelope({x}, 47, {x} + 0.0008, 47.0008) AS geometry,
                 {{'xmin': CAST({x} AS DOUBLE), 'ymin': 47.0::DOUBLE, 'xmax': CAST({x} + 0.0008 AS DOUBLE), 'ymax': 47.0008::DOUBLE}} AS bbox,
                 6000.0 + i AS "metrics:area",
                 '3301010100' AS "hcat:code", 'winter_common_soft_wheat' AS "hcat:name"{date}
          FROM (VALUES {values}) t(i, y)
        ) TO {quote(path)} (FORMAT parquet{kv})"""
    )
    return path


def write_staged_stac(path: Path, collection_id: str, parquet: Path, license: str, provider: dict, license_link: str | None = None) -> None:
    """The record build.describe() leaves beside a staged file."""
    con = duckdb_connect()
    columns = [{"name": r[0], "type": r[1].lower()} for r in con.execute(f"DESCRIBE SELECT * FROM read_parquet({quote(parquet)}, hive_partitioning = false)").fetchall()]
    xmin, ymin, xmax, ymax = con.execute(
        f"SELECT min(bbox.xmin), min(bbox.ymin), max(bbox.xmax), max(bbox.ymax) FROM read_parquet({quote(parquet)})"
    ).fetchone()
    links = [{"rel": "license", "href": license_link, "title": "Terms of use"}] if license_link else []
    write_json(path, {
        "type": "Collection",
        "stac_version": "1.1.0",
        "id": collection_id,
        "license": license,
        "providers": [provider],
        "extent": {"spatial": {"bbox": [[xmin, ymin, xmax, ymax]]}, "temporal": {"interval": [[None, None]]}},
        "links": links,
        "fiboa_version": "0.3.0",
        "assets": {
            "data": {
                "href": f"./{parquet.name}",
                "type": PARQUET_TYPE,
                "roles": ["data"],
                "table:columns": columns,
                "table:row_count": parquet_row_count(parquet),
                "processing:software": {"fiboa-cli": "0.0.0"},
                **file_facts(parquet),
            }
        },
    })


def converter_meta(converter_id: str, short_name: str, provider: str, attribution: str, license: str) -> dict:
    return {
        "id": converter_id,
        "cli_id": converter_id,
        "short_name": short_name,
        "title": f"Field boundaries for {short_name}",
        "description": f"The fields of {short_name}.",
        "provider": provider,
        "attribution": attribution,
        "license": license,
        "variants": [],
        "sources": {"": [f"https://example.org/{converter_id}.zip"]},
        "columns": {"geometry": "geometry", "flaeche_m2": "metrics:area"},
        "extensions": [],
        "ec_mapping_csv": None,
        "area_is_in_ha": False,
        "area_calculate_missing": False,
    }


def point_tooling_at(root: Path, *modules) -> None:
    """Point common and the given tool modules at root/staging and root/catalog."""
    for module in (common, *modules):
        if hasattr(module, "STAGING_DIR"):
            module.STAGING_DIR = root / "staging"
        if hasattr(module, "CATALOG_DIR"):
            module.CATALOG_DIR = root / "catalog"
