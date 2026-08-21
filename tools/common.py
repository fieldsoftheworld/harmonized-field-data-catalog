"""Shared helpers for the catalog tooling: configuration, the manifest, and
the facts that are read from the data files (never invented).

Nothing here writes to ``catalog/``; that is ``catalogize.py``'s job.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CATALOG_DIR = ROOT / "catalog"
STAGING_DIR = ROOT / "staging"
MANIFEST = ROOT / "datasets.yaml"
TOOLS_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(TOOLS_DIR))
from publish import load_config  # noqa: E402

PORTOLAN_EXTENSION = "https://schemas.portolan-sdi.org/portolan/v0.1.2/schema.json"
FILE_EXTENSION = "https://stac-extensions.github.io/file/v2.1.0/schema.json"
TABLE_EXTENSION = "https://stac-extensions.github.io/table/v1.2.0/schema.json"
PROJECTION_EXTENSION = "https://stac-extensions.github.io/projection/v2.0.0/schema.json"
PROCESSING_EXTENSION = "https://stac-extensions.github.io/processing/v1.2.0/schema.json"
WEB_MAP_LINKS_EXTENSION = "https://stac-extensions.github.io/web-map-links/v1.3.0/schema.json"
PARTITION_EXTENSION = "https://schemas.portolan-sdi.org/incubating/partition/v1.0.0/schema.json"

PARQUET_TYPE = "application/vnd.apache.parquet"
PMTILES_TYPE = "application/vnd.pmtiles"
STYLE_TYPE = "application/vnd.mapbox.style+json"

# Year partitions are written as hive directories: <id>/year=<Y>/<id>-<Y>.parquet
PARTITION_KEY = "year"


def partition_dir(year: str | int) -> str:
    return f"{PARTITION_KEY}={year}"


def file_stem(dataset_id: str, year: str | int) -> str:
    return f"{dataset_id}-{year}"


@dataclass
class Dataset:
    id: str
    years: list[str]
    keywords: list[str] = field(default_factory=list)
    via: str | None = None
    year_source: str | None = None
    notes: str | None = None

    @property
    def latest(self) -> str:
        return self.years[-1]


@dataclass
class Manifest:
    catalog: dict
    host: dict
    datasets: dict[str, Dataset]

    @classmethod
    def load(cls, path: Path = MANIFEST) -> "Manifest":
        raw = yaml.safe_load(path.read_text())
        datasets = {}
        for dataset_id, spec in (raw.get("datasets") or {}).items():
            spec = spec or {}
            if "years" in spec:
                years = [str(y) for y in spec["years"]]
            elif "year" in spec:
                years = [str(spec["year"])]
            else:
                sys.exit(f"datasets.yaml: {dataset_id} needs 'years' or 'year'")
            if years != sorted(years):
                sys.exit(f"datasets.yaml: {dataset_id} years must be ascending, newest last")
            datasets[dataset_id] = Dataset(
                id=dataset_id,
                years=years,
                keywords=list(spec.get("keywords") or []),
                via=spec.get("via"),
                year_source=spec.get("year_source"),
                notes=spec.get("notes"),
            )
        return cls(catalog=raw["catalog"], host=raw["host"], datasets=datasets)


def publish_config() -> dict[str, str]:
    return load_config()


def staging_year_dir(dataset_id: str, year: str) -> Path:
    return STAGING_DIR / dataset_id / partition_dir(year)


def catalog_year_dir(dataset_id: str, year: str) -> Path:
    return CATALOG_DIR / dataset_id / partition_dir(year)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


# --- facts read from the data --------------------------------------------------


def duckdb_connect():
    import duckdb

    con = duckdb.connect()
    con.execute("INSTALL spatial; LOAD spatial;")
    return con


def quote(path: Path | str) -> str:
    return "'" + str(path).replace("'", "''") + "'"


def parquet_crs(path: Path) -> str | None:
    """``EPSG:<code>`` from the GeoParquet ``geo`` metadata, or None."""
    con = duckdb_connect()
    rows = con.execute(
        f"SELECT key, value FROM parquet_kv_metadata({quote(path)})"
    ).fetchall()
    for key, value in rows:
        if bytes(key).decode() == "geo":
            geo = json.loads(bytes(value).decode())
            col = geo["columns"][geo["primary_column"]]
            crs = col.get("crs")
            if crs is None:
                return "EPSG:4326"  # GeoParquet default
            ident = crs.get("id") or {}
            if ident.get("authority") and ident.get("code"):
                return f"{ident['authority']}:{ident['code']}"
            return None
    return None


COLLECTION_META_SKIP = {"schemas", "schemas:custom", "title", "description", "license", "provider", "attribution", "collection"}


def parquet_collection_properties(path: Path) -> dict:
    """Properties stored once for the whole file in the GeoParquet ``collection``
    metadata (vecorel hoists columns that are constant for every row, e.g.
    ``admin:country_code`` or ``crop:code_list``)."""
    con = duckdb_connect()
    rows = con.execute(f"SELECT key, value FROM parquet_kv_metadata({quote(path)})").fetchall()
    for key, value in rows:
        if bytes(key).decode() == "collection":
            meta = json.loads(bytes(value).decode())
            return {k: v for k, v in meta.items() if k not in COLLECTION_META_SKIP}
    return {}


def parquet_columns(path: Path) -> list[str]:
    con = duckdb_connect()
    rows = con.execute(f"DESCRIBE SELECT * FROM read_parquet({quote(path)})").fetchall()
    return [r[0] for r in rows]


def column_stats(path: Path, column: str) -> dict | None:
    """count / min / quantiles for a numeric column, or None if absent."""
    if column not in parquet_columns(path):
        return None
    con = duckdb_connect()
    q = f'"{column}"'
    row = con.execute(
        f"SELECT count({q}), min({q}), max({q}), "
        f"quantile_cont({q}, 0.2), quantile_cont({q}, 0.4), quantile_cont({q}, 0.5), "
        f"quantile_cont({q}, 0.6), quantile_cont({q}, 0.8), quantile_cont({q}, 0.95) "
        f"FROM read_parquet({quote(path)})"
    ).fetchone()
    return {
        "count": row[0],
        "min": row[1],
        "max": row[2],
        "p20": row[3],
        "p40": row[4],
        "p50": row[5],
        "p60": row[6],
        "p80": row[7],
        "p95": row[8],
    }


def hcat_crops(path: Path) -> list[tuple[str, str | None, int, float]]:
    """(hcat:code, hcat:name, feature count, area in m²) per crop, largest area first."""
    columns = parquet_columns(path)
    if "hcat:code" not in columns:
        return []
    con = duckdb_connect()
    area = 'sum("metrics:area")' if "metrics:area" in columns else "0"
    name = 'any_value("hcat:name")' if "hcat:name" in columns else "NULL"
    rows = con.execute(
        f'SELECT CAST("hcat:code" AS VARCHAR) AS c, {name}, count(*), {area} '
        f'FROM read_parquet({quote(path)}) WHERE "hcat:code" IS NOT NULL '
        f"GROUP BY c ORDER BY 4 DESC, 3 DESC"
    ).fetchall()
    return [(r[0], r[1], int(r[2]), float(r[3] or 0)) for r in rows]


def hcat_groups(path: Path, digits: int = 6) -> list[tuple[str, int, float]]:
    """(group code prefix, feature count, area in m²) per HCAT group, largest first.

    The group is the first ``digits`` digits of the 10-digit ``hcat:code``.
    """
    columns = parquet_columns(path)
    if "hcat:code" not in columns:
        return []
    con = duckdb_connect()
    area = 'sum("metrics:area")' if "metrics:area" in columns else "0"
    rows = con.execute(
        f'SELECT substr(CAST("hcat:code" AS VARCHAR), 1, {digits}) AS g, count(*), {area} '
        f'FROM read_parquet({quote(path)}) WHERE "hcat:code" IS NOT NULL '
        f"GROUP BY g ORDER BY 3 DESC, 2 DESC"
    ).fetchall()
    return [(r[0], int(r[1]), float(r[2] or 0)) for r in rows]


def value_counts(path: Path, column: str, limit: int = 12) -> list[tuple[str, int]]:
    if column not in parquet_columns(path):
        return []
    con = duckdb_connect()
    rows = con.execute(
        f'SELECT CAST("{column}" AS VARCHAR), count(*) FROM read_parquet({quote(path)}) '
        f'WHERE "{column}" IS NOT NULL GROUP BY 1 ORDER BY 2 DESC LIMIT {int(limit)}'
    ).fetchall()
    return [(r[0], int(r[1])) for r in rows]


def humanize(name: str) -> str:
    """``winter_common_soft_wheat`` -> ``Winter common soft wheat``."""
    text = name.replace("_", " ").strip()
    return text[:1].upper() + text[1:]


def parse_link_str(value: str | None) -> tuple[str | None, str | None]:
    """``"Name <https://url>"`` -> (name, url); either may be None."""
    if not value:
        return None, None
    m = re.match(r"^\s*(.*?)\s*<\s*(https?://[^>\s]+)\s*>\s*$", value)
    if m:
        return (m.group(1) or None), m.group(2)
    if re.match(r"^https?://\S+$", value.strip()):
        return None, value.strip()
    return value.strip(), None


def fmt_int(n: int | float | None) -> str:
    return "—" if n is None else f"{int(n):,}"


def fmt_bytes(n: int | None) -> str:
    if n is None:
        return "—"
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"
