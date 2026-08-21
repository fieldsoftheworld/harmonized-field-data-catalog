#!/usr/bin/env python3
"""Generate the published metadata for one dataset (or the catalog root).

Input is what ``fiboa publish`` left in ``staging/<id>/year=<Y>/`` — the
GeoParquet, the PMTiles and a ``collection.json`` with relative links — plus
``staging/<id>/converter.json`` (``converter_meta.py``) and the manifest
``datasets.yaml``. Output is everything under ``catalog/<id>/``:

    collection.json          one collection per dataset, partitioned by year
    year=<Y>/<id>-<Y>.json   one item per year, beside its data files
    styles/*.json            MapLibre styles chosen from the data
    README.md, AGENTS.md, llms.txt

and, with ``--root``, the catalog root (``catalog.json``, README, AGENTS, llms).

Every sentence written here is either copied from the converter / the fiboa
data survey / the specification (attested), or measured from the files
(derived, with the query in AGENTS.md). Nothing is guessed.

    python tools/catalogize.py nl          # one dataset
    python tools/catalogize.py --root      # the catalog root from all collections
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import sys
from pathlib import Path

import requests
import yaml

from common import (
    CATALOG_DIR,
    FILE_EXTENSION,
    PARQUET_TYPE,
    PARTITION_EXTENSION,
    PARTITION_KEY,
    PMTILES_TYPE,
    PORTOLAN_EXTENSION,
    PROCESSING_EXTENSION,
    PROJECTION_EXTENSION,
    ROOT,
    STAGING_DIR,
    STYLE_TYPE,
    TABLE_EXTENSION,
    TOOLS_DIR,
    WEB_MAP_LINKS_EXTENSION,
    Dataset,
    Manifest,
    catalog_year_dir,
    column_stats,
    duckdb_connect,
    file_stem,
    fmt_bytes,
    fmt_int,
    hcat_crops,
    parquet_collection_properties,
    parquet_crs,
    parse_link_str,
    partition_dir,
    publish_config,
    read_json,
    staging_year_dir,
    write_json,
    write_text,
)
from styles import field_size_style, hcat_style, outline_style, write_style

FIELD_DESCRIPTIONS = yaml.safe_load((TOOLS_DIR / "field_descriptions.yaml").read_text())
DATA_SURVEY_RAW = "https://raw.githubusercontent.com/fiboa/data-survey/main/data/{base}.md"
DATA_SURVEY_PAGE = "https://github.com/fiboa/data-survey/blob/main/data/{base}.md"
FIBOA_CLI_REPO = "https://github.com/fiboa/cli"
FIBOA_SPEC = "https://github.com/fiboa/specification"
CACHE_DIR = ROOT / "cache" / "data-survey"


# --- inputs -----------------------------------------------------------------------


class YearInput:
    def __init__(self, dataset_id: str, year: str):
        self.year = year
        self.dir = staging_year_dir(dataset_id, year)
        self.stac_path = self.dir / "collection.json"
        if not self.stac_path.exists():
            sys.exit(f"missing {self.stac_path}: run `fiboa publish {dataset_id} --variant {year}` first")
        self.stac = read_json(self.stac_path)
        self.data_asset = self.stac["assets"]["data"]
        self.visual_asset = self.stac["assets"].get("visual")
        # fiboa publish names files <id>[-<variant>]; take the names it wrote
        self.parquet = self.dir / Path(self.data_asset["href"]).name
        self.pmtiles = self.dir / Path(self.visual_asset["href"]).name if self.visual_asset else None
        if not self.parquet.exists():
            sys.exit(f"missing {self.parquet}")
        self.row_count = self.data_asset.get("table:row_count")
        self.bbox = self.stac["extent"]["spatial"]["bbox"][0]
        self.interval = self.stac["extent"]["temporal"]["interval"][0]
        self.crs = parquet_crs(self.parquet)
        self.collection_props = parquet_collection_properties(self.parquet)


def load_converter_meta(dataset_id: str) -> dict:
    path = STAGING_DIR / dataset_id / "converter.json"
    if not path.exists():
        sys.exit(f"missing {path}: run tools/build.py (it calls converter_meta.py)")
    return read_json(path)


def data_survey(dataset_id: str) -> tuple[str | None, dict[str, str]]:
    """(survey page URL, {source column: description}) from fiboa/data-survey.

    The survey's property tables describe the *source* columns; they are mapped
    to fiboa names through the converter's ``columns``. Cached under cache/.
    """
    base = dataset_id.replace("_", "-").upper()
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached = CACHE_DIR / f"{base}.md"
    text = None
    if cached.exists():
        text = cached.read_text(encoding="utf-8")
    else:
        try:
            r = requests.get(DATA_SURVEY_RAW.format(base=base), timeout=30)
            if r.ok:
                text = r.text
                cached.write_text(text, encoding="utf-8")
        except requests.RequestException:
            text = None
    if text is None:
        return None, {}
    props: dict[str, str] = {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and cells[0] and not cells[0].startswith("-") and cells[0] != "Property":
            name = cells[0].strip("`")
            desc = cells[-1]
            if desc and name not in props:
                props[name] = desc
    return DATA_SURVEY_PAGE.format(base=base), props


def describe_columns(table_columns: list[dict], meta: dict, survey_props: dict[str, str]) -> list[dict]:
    """table:columns with a description for every column we can attest."""
    spec = FIELD_DESCRIPTIONS["columns"]
    sources = FIELD_DESCRIPTIONS["sources"]
    reverse = {v: k for k, v in (meta.get("columns") or {}).items()}
    out = []
    for col in table_columns:
        name = col["name"]
        entry = dict(col)
        if name in spec:
            src = sources[spec[name]["source"]]
            entry["description"] = f"{spec[name]['description']} ([spec]({src}))"
        else:
            source_name = reverse.get(name, name)
            desc = survey_props.get(source_name) or survey_props.get(name)
            if desc:
                entry["description"] = (
                    f"{desc} (source column `{source_name}`, per the fiboa data survey)"
                    if source_name != name
                    else f"{desc} (per the fiboa data survey)"
                )
            else:
                entry["description"] = (
                    f"Carried over from the source column `{source_name}`; the publisher documents no meaning for it."
                    if source_name != name
                    else "Source-specific column; the publisher documents no meaning for it."
                )
        out.append(entry)
    return out


# --- builders -----------------------------------------------------------------------


def bbox_union(boxes: list[list[float]]) -> list[float]:
    return [
        min(b[0] for b in boxes),
        min(b[1] for b in boxes),
        max(b[2] for b in boxes),
        max(b[3] for b in boxes),
    ]


def bbox_polygon(b: list[float]) -> dict:
    return {
        "type": "Polygon",
        "coordinates": [[[b[0], b[1]], [b[2], b[1]], [b[2], b[3]], [b[0], b[3]], [b[0], b[1]]]],
    }


def year_interval(year: str, interval: list) -> tuple[str, str]:
    """Item interval: the data's own determination range when present, else the year."""
    start, end = interval if interval else (None, None)
    if start and end:
        return start, end
    return f"{year}-01-01T00:00:00Z", f"{year}-12-31T23:59:59Z"


def iso_mtime(path: Path) -> str:
    return dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def link_data_file(src: Path, dst: Path) -> None:
    """Symlink a staged data file into catalog/ so local gates can resolve it.

    The symlink is gitignored (``*.parquet``/``*.pmtiles``); uploads come from
    staging/ through upload_data.py, never from catalog/.
    """
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.is_symlink() or dst.exists():
        dst.unlink()
    dst.symlink_to(os.path.relpath(src, dst.parent))


def build_items(ds: Dataset, meta: dict, years: list[YearInput], public_base: str, table_columns: list[dict]) -> list[dict]:
    items = []
    for y in years:
        stem = file_stem(ds.id, y.year)
        start, end = year_interval(y.year, y.interval)
        parquet_name = y.parquet.name
        pmtiles_name = y.pmtiles.name if y.pmtiles else None
        item = {
            "type": "Feature",
            "stac_version": "1.1.0",
            "stac_extensions": [FILE_EXTENSION, TABLE_EXTENSION, PROJECTION_EXTENSION, PROCESSING_EXTENSION],
            "id": stem,
            "geometry": bbox_polygon(y.bbox),
            "bbox": y.bbox,
            "properties": {
                "title": f"{meta['short_name']} — {y.year}",
                "description": (
                    f"Field boundaries of the {y.year} edition of this dataset, one GeoParquet file "
                    f"(`{parquet_name}`, {fmt_int(y.row_count)} fields) and its PMTiles. "
                    f"Partition `{PARTITION_KEY}={y.year}` of the collection's hive layout."
                ),
                "datetime": None,
                "start_datetime": start,
                "end_datetime": end,
                PARTITION_KEY: int(y.year),
                "proj:code": y.crs,
                "table:columns": table_columns,
                "table:primary_geometry": "geometry",
                "table:row_count": y.row_count,
                "processing:software": y.data_asset.get("processing:software", {}),
            },
            "collection": ds.id,
            "assets": {
                "data": {
                    "href": f"./{parquet_name}",
                    "type": PARQUET_TYPE,
                    "title": f"{meta['short_name']} {y.year} (GeoParquet)",
                    "roles": ["data"],
                    "file:size": y.data_asset["file:size"],
                    "file:checksum": y.data_asset["file:checksum"],
                    "proj:code": y.crs,
                },
            },
            "links": [
                {"rel": "root", "href": "../../catalog.json", "type": "application/json"},
                {"rel": "parent", "href": "../collection.json", "type": "application/json"},
                {"rel": "collection", "href": "../collection.json", "type": "application/json"},
            ],
        }
        if y.visual_asset:
            item["assets"]["visual"] = {
                "href": f"./{pmtiles_name}",
                "type": PMTILES_TYPE,
                "title": f"{meta['short_name']} {y.year} (PMTiles)",
                "roles": ["visual"],
                "file:size": y.visual_asset["file:size"],
                "file:checksum": y.visual_asset["file:checksum"],
            }
        items.append(item)
    return items


def license_fields(base: dict) -> tuple[str, list[dict]]:
    """(license, license links) — SPDX id, or 'other' with a link to the terms."""
    lic = base.get("license") or "other"
    links = [link for link in base.get("links", []) if link.get("rel") == "license"]
    for link in links:
        link.setdefault("type", "text/html")
    if lic != "other":
        if not re.match(r"^[A-Za-z0-9.+-]+$", lic):
            lic = "other"
        else:
            lic = lic.upper() if lic.lower().startswith(("cc", "dl-de")) else lic
    return lic, links


def build_collection(
    ds: Dataset,
    meta: dict,
    years: list[YearInput],
    items: list[dict],
    manifest: Manifest,
    public_base: str,
    human_base: str,
    table_columns: list[dict],
    style_assets: dict,
    survey_url: str | None,
) -> dict:
    latest = years[-1]
    base = latest.stac
    lic, license_links = license_fields(base)
    provider_name, provider_url = parse_link_str(meta.get("provider"))
    via = ds.via or provider_url
    glob = f"{public_base}/{ds.id}/{PARTITION_KEY}=*/*.parquet"
    year_list = ", ".join(y.year for y in years)
    collection_url = f"{human_base}/{ds.id}"

    access = (
        f"\n\nThis collection holds {len(years)} edition{'s' if len(years) != 1 else ''} "
        f"({year_list}), one GeoParquet file per year under `{PARTITION_KEY}=<year>/` (hive layout). "
        f"Read them all at once with the partition glob `{glob}`; the `data` asset is a copy of the "
        f"latest edition ({latest.year}). Geometries are kept in the source CRS ({latest.crs}). "
        f"Converted with [fiboa-cli]({FIBOA_CLI_REPO}) into the [fiboa]({FIBOA_SPEC}) schema; "
        f"tested queries are in the collection's [AGENTS.md]({collection_url}/AGENTS.md)."
    )

    providers = list(base.get("providers") or [])
    if not providers and provider_name:
        providers = [{"name": provider_name, "roles": ["producer", "licensor"], **({"url": provider_url} if provider_url else {})}]
    host = dict(manifest.host)
    providers.append(host)

    collection = {
        "type": "Collection",
        "stac_version": "1.1.0",
        "stac_extensions": [
            PORTOLAN_EXTENSION,
            FILE_EXTENSION,
            TABLE_EXTENSION,
            PROJECTION_EXTENSION,
            PROCESSING_EXTENSION,
            WEB_MAP_LINKS_EXTENSION,
            PARTITION_EXTENSION,
        ],
        "id": ds.id,
        "title": meta["title"],
        "description": meta["description"] + access,
        "keywords": sorted(set(["field boundaries", "agriculture", "fiboa", *ds.keywords])),
        "license": lic,
        "providers": providers,
        "extent": {
            "spatial": {"bbox": [bbox_union([y.bbox for y in years])]},
            "temporal": {
                "interval": [
                    [
                        min(year_interval(y.year, y.interval)[0] for y in years),
                        max(year_interval(y.year, y.interval)[1] for y in years),
                    ]
                ]
            },
        },
        "summaries": {"proj:code": sorted({y.crs for y in years if y.crs})},
        "table:columns": table_columns,
        "table:primary_geometry": "geometry",
        "table:row_count": latest.row_count,
        "partition:scheme": "hive",
        "partition:strategy": "temporal",
        "partition:keys": [
            {
                "name": PARTITION_KEY,
                "type": "int32",
                "description": "Edition year of the source dataset (the converter variant). Not a column in the files; DuckDB adds it with hive_partitioning=true.",
            }
        ],
        "partition:file_count": len(years),
        "partition:glob": glob,
        "assets": {
            "data": {
                "href": f"./latest/{ds.id}.parquet",
                "type": PARQUET_TYPE,
                "title": f"{meta['short_name']} — latest edition ({latest.year}) (GeoParquet)",
                "description": f"Byte-identical copy of `{partition_dir(latest.year)}/{latest.parquet.name}`, kept at a stable path so `*/latest/*.parquet` selects the newest edition of every collection.",
                "roles": ["data"],
                "file:size": latest.data_asset["file:size"],
                "file:checksum": latest.data_asset["file:checksum"],
                "proj:code": latest.crs,
            },
            **style_assets,
        },
        "links": [
            {"rel": "root", "href": "../catalog.json", "type": "application/json"},
            {"rel": "parent", "href": "../catalog.json", "type": "application/json"},
            *license_links,
            {"rel": "agents", "href": "./AGENTS.md", "type": "text/markdown", "title": "Guidance for AI agents"},
            {"rel": "describedby", "href": "./README.md", "type": "text/markdown", "title": "Human-readable documentation"},
            {"rel": "llms", "href": "./llms.txt", "type": "text/markdown", "title": "Agent/LLM usage guide"},
        ],
        "updated": iso_mtime(latest.parquet),
    }
    for key in ("fiboa_version", "vecorel_version", "vecorel_extensions"):
        if key in base:
            collection[key] = base[key]
    if meta.get("attribution"):
        collection["attribution"] = meta["attribution"]

    if latest.visual_asset:
        pm = f"./{partition_dir(latest.year)}/{latest.pmtiles.name}"
        collection["assets"]["visual"] = {
            "href": pm,
            "type": PMTILES_TYPE,
            "title": f"{meta['short_name']} — latest edition ({latest.year}) (PMTiles)",
            "roles": ["visual"],
            "file:size": latest.visual_asset["file:size"],
            "file:checksum": latest.visual_asset["file:checksum"],
        }
        collection["links"].append(
            {"rel": "pmtiles", "href": pm, "type": PMTILES_TYPE, "title": "Web map tiles", "pmtiles:layers": [ds.id]}
        )

    thumb = CATALOG_DIR / ds.id / "thumbnail.jpg"
    if thumb.exists():
        import hashlib

        digest = hashlib.sha256(thumb.read_bytes()).hexdigest()
        collection["assets"]["thumbnail"] = {
            "href": "./thumbnail.jpg",
            "type": "image/jpeg",
            "title": "Preview of the default style over a light basemap. © OpenStreetMap contributors © CARTO.",
            "roles": ["thumbnail"],
            "file:size": thumb.stat().st_size,
            "file:checksum": "1220" + digest,
        }

    if via:
        collection["links"].append({"rel": "via", "href": via, "type": "text/html", "title": "Original source (publisher page)"})
    if survey_url:
        collection["links"].append({"rel": "related", "href": survey_url, "type": "text/html", "title": "fiboa data survey entry for this source"})
    collection["links"].append({"rel": "related", "href": f"{FIBOA_CLI_REPO}/blob/main/fiboa_cli/datasets/{meta['cli_id']}.py", "type": "text/html", "title": "Converter source code (fiboa-cli)"})
    for y, item in zip(years, items):
        collection["links"].append(
            {
                "rel": "item",
                "href": f"./{partition_dir(y.year)}/{file_stem(ds.id, y.year)}.json",
                "type": "application/geo+json",
                "title": item["properties"]["title"],
            }
        )
    return collection


def build_styles(ds: Dataset, meta: dict, latest: YearInput) -> tuple[dict, dict]:
    """Write styles/, return (style assets, facts used for the docs)."""
    if not latest.visual_asset:
        return {}, {}
    styles_dir = CATALOG_DIR / ds.id / "styles"
    if styles_dir.exists():
        shutil.rmtree(styles_dir)
    pm_rel = f"../{partition_dir(latest.year)}/{latest.pmtiles.name}"
    title = meta["short_name"]
    assets: dict = {}
    facts: dict = {}

    crops = hcat_crops(latest.parquet)
    hcat = hcat_style(crops, ds.id, pm_rel, title)
    area = column_stats(latest.parquet, "metrics:area")

    default_key = None
    if hcat:
        style, legend = hcat
        write_style(styles_dir / "hcat-crops.json", style)
        assets["style-hcat-crops"] = {
            "href": "./styles/hcat-crops.json",
            "type": STYLE_TYPE,
            "title": "Crops (HCAT)",
            "roles": ["style"],
            "description": style["metadata"]["description"],
        }
        facts["hcat_legend"] = legend
        default_key = "style-hcat-crops"
    if area and area["count"]:
        style = field_size_style(area, ds.id, pm_rel, title)
        write_style(styles_dir / "field-size.json", style)
        assets["style-field-size"] = {
            "href": "./styles/field-size.json",
            "type": STYLE_TYPE,
            "title": "Field size (ha)",
            "roles": ["style"],
            "description": style["metadata"]["description"],
        }
        facts["area"] = area
        default_key = default_key or "style-field-size"
    style = outline_style(ds.id, ds.id, pm_rel, title)
    write_style(styles_dir / "outline.json", style)
    assets["style-outline"] = {
        "href": "./styles/outline.json",
        "type": STYLE_TYPE,
        "title": "Field boundaries",
        "roles": ["style"],
        "description": style["metadata"]["description"],
    }
    default_key = default_key or "style-outline"
    assets[default_key]["roles"] = ["style", "default"]

    for key, asset in assets.items():
        path = styles_dir / Path(asset["href"]).name
        import hashlib

        asset["file:size"] = path.stat().st_size
        asset["file:checksum"] = "1220" + hashlib.sha256(path.read_bytes()).hexdigest()
    return assets, facts


# --- documentation ---------------------------------------------------------------------


def run_query(sql: str) -> str:
    """Run a DuckDB query and return a compact text rendering of the result."""
    con = duckdb_connect()
    rel = con.execute(sql)
    rows = rel.fetchall()
    cols = [d[0] for d in rel.description]
    lines = [" | ".join(cols)]
    for row in rows[:8]:
        lines.append(" | ".join(str(v) for v in row))
    if len(rows) > 8:
        lines.append(f"... {len(rows) - 8} more rows")
    return "\n".join(lines)


def localize(sql: str, public_base: str) -> str:
    """Point a published-URL query at staging/ so it can be run before upload."""
    return sql.replace(public_base, STAGING_DIR.as_posix())


def md_query(sql: str, public_base: str) -> str:
    """A fenced SQL block followed by the result it produced locally."""
    result = run_query(localize(sql, public_base))
    commented = "\n".join(f"-- {line}" for line in result.splitlines())
    return f"```sql\n{sql.strip()}\n{commented}\n```"


def collection_docs(
    ds: Dataset,
    meta: dict,
    years: list[YearInput],
    collection: dict,
    manifest: Manifest,
    public_base: str,
    human_base: str,
    survey_url: str | None,
    style_facts: dict,
) -> None:
    latest = years[-1]
    cdir = CATALOG_DIR / ds.id
    provider_name, provider_url = parse_link_str(meta.get("provider"))
    prov_md = f"[{provider_name}]({provider_url})" if provider_url else (provider_name or "—")
    lic = collection["license"]
    lic_links = [link for link in collection["links"] if link["rel"] == "license"]
    lic_md = lic if lic != "other" else (f"other — [{lic_links[0].get('title') or 'license terms'}]({lic_links[0]['href']})" if lic_links else "other")
    if meta.get("license") and lic == "other":
        lic_md += f" (converter: `{meta['license']}`)"
    glob = collection["partition:glob"]
    latest_url = f"{public_base}/{ds.id}/latest/{ds.id}.parquet"
    columns = collection["table:columns"]
    hcat_cols = any(c["name"] == "hcat:code" for c in columns)
    software = latest.data_asset.get("processing:software", {})
    software_md = ", ".join(f"{k} {v}" for k, v in software.items()) or "fiboa-cli"

    # -- README.md
    lines = [f"# {meta['title']}", "", meta["description"], ""]
    lines += [
        f"- **Source data provider:** {prov_md}",
        f"- **License:** {lic_md}",
        f"- **Editions:** {', '.join(y.year for y in years)} (one GeoParquet per year)",
        f"- **Fields in the latest edition ({latest.year}):** {fmt_int(latest.row_count)}",
        f"- **Coordinate reference system:** {latest.crs} (as published by the source; not reprojected)",
        f"- **Converted with:** {software_md} ([converter]({FIBOA_CLI_REPO}/blob/main/fiboa_cli/datasets/{meta['cli_id']}.py))",
    ]
    if survey_url:
        lines.append(f"- **Data survey:** [{Path(survey_url).name}]({survey_url})")
    lines += ["", f"Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/{public_base.removeprefix('https://')}/{ds.id}/collection.json), or start from the [AGENTS.md]({human_base}/{ds.id}/AGENTS.md) for tested queries.", ""]
    lines += ["## Files", "", "| Year | Fields | GeoParquet | PMTiles | STAC item |", "|---|---:|---|---|---|"]
    for y in years:
        stem = file_stem(ds.id, y.year)
        base = f"{public_base}/{ds.id}/{partition_dir(y.year)}"
        pm = f"[{fmt_bytes(y.visual_asset['file:size'])}]({base}/{y.pmtiles.name})" if y.visual_asset else "—"
        lines.append(f"| {y.year} | {fmt_int(y.row_count)} | [{fmt_bytes(y.data_asset['file:size'])}]({base}/{y.parquet.name}) | {pm} | [{stem}.json]({base}/{stem}.json) |")
    lines += ["", f"The latest edition is also available at a stable path: [{ds.id}/latest/{ds.id}.parquet]({latest_url}). All editions together: `{glob}`.", ""]
    lines += ["## Columns", "", "| Column | Type | Description |", "|---|---|---|"]
    for c in columns:
        lines.append(f"| `{c['name']}` | {c['type']} | {c.get('description', '')} |")
    if latest.collection_props:
        lines += ["", "Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):", ""]
        for k, v in latest.collection_props.items():
            lines.append(f"- `{k}`: `{v}`")
    lines += ["", "## Access", "", "Query the published files in place with DuckDB; nothing needs downloading first.", ""]
    q1 = f"INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;\nSELECT count(*) AS fields, round(sum(\"metrics:area\") / 1e4) AS hectares\nFROM read_parquet('{latest_url}');" if any(c["name"] == "metrics:area" for c in columns) else f"INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;\nSELECT count(*) AS fields FROM read_parquet('{latest_url}');"
    lines += [md_query(q1, public_base), ""]
    lines += ["## Provenance", ""]
    lines.append(f"This catalog is a mirror: the data is produced and licensed by {prov_md} and republished here as cloud-native GeoParquet and PMTiles by {manifest.host['name']}. Each edition was downloaded from the source and converted with {software_md}:")
    lines.append("")
    for y in years:
        urls = meta.get("sources", {}).get(y.year) or meta.get("sources", {}).get("") or []
        lines.append(f"- {y.year}: converted {iso_mtime(y.parquet)[:10]} from " + (", ".join(f"<{u}>" for u in urls) if urls else "a manually obtained file"))
    lines += ["", "The conversion is deterministic and lives in [fiboa-cli]({0}); changes to how a column is mapped are made there, not in this catalog.".format(FIBOA_CLI_REPO), "", "## License", "", f"{lic_md}. " + (f"Attribution: {meta['attribution']}" if meta.get("attribution") else f"Attribute the data to {provider_name or 'the source data provider'}.")]
    write_text(cdir / "README.md", "\n".join(lines))

    # -- AGENTS.md
    a = [f"# Agent guidance — {meta['title']}", ""]
    a.append(f"{meta['short_name']} field boundaries in the [fiboa]({FIBOA_SPEC}) schema, {len(years)} edition{'s' if len(years) != 1 else ''} ({', '.join(y.year for y in years)}). Every claim below is quoted from the source, the converter, or measured from the published files; each query was run before it was written down, and its output follows it as comments.")
    a += ["", "## Access", ""]
    a.append(f"- Latest edition, stable path: `{latest_url}`")
    a.append(f"- One edition: `{public_base}/{ds.id}/{PARTITION_KEY}=<year>/<file>.parquet`, e.g. `{public_base}/{ds.id}/{partition_dir(latest.year)}/{latest.parquet.name}`")
    a.append(f"- All editions (hive partitioned): `{glob}` — read with `hive_partitioning = true` to get a `{PARTITION_KEY}` column.")
    if latest.pmtiles:
        a.append(f"- PMTiles for maps: `{public_base}/{ds.id}/{partition_dir(latest.year)}/{latest.pmtiles.name}`, layer `{ds.id}`; MapLibre styles in `styles/`.")
    a += ["", "## Quirks that produce silently wrong answers", ""]
    a.append(f"- **CRS is {latest.crs}, not WGS84.** `ST_Area`/`ST_Distance` return units of that CRS; transform with `ST_Transform` if you need lon/lat, or use `metrics:area`.")
    area_src = next((k for k, v in (meta.get("columns") or {}).items() if v == "metrics:area"), None)
    if area_src and meta.get("area_calculate_missing"):
        a.append(f"- **`metrics:area` is in square metres** (source column `{area_src}`{', hectares × 10 000' if meta.get('area_is_in_ha') else ''}; where the source value is missing or 0 the converter computed it from the geometry, in EPSG:6933 when the CRS is not metric). Divide by 10 000 for hectares.")
    elif area_src:
        a.append(f"- **`metrics:area` is in square metres**, taken from the source column `{area_src}`{' (hectares × 10 000)' if meta.get('area_is_in_ha') else ''}. Divide by 10 000 for hectares.")
    elif any(c["name"] == "metrics:area" for c in columns):
        a.append("- **`metrics:area` is in square metres**, computed by the converter from the geometry (EPSG:6933 when the CRS is not metric). Divide by 10 000 for hectares.")
    a.append(f"- **`{PARTITION_KEY}` is the edition, not the observation date.** It is the year of the source publication (the converter variant). `determination:datetime`, where present, is the source's own date for a field.")
    id_src = next((k for k, v in (meta.get("columns") or {}).items() if v == "id"), None)
    a.append(f"- **`id` is only guaranteed unique within one edition** (fiboa requires uniqueness per file; it is {'the source column `' + id_src + '`' if id_src else 'assigned by the converter'}). Whether an id persists across editions is not verified here; do not join editions on it without checking.")
    if hcat_cols:
        a.append(f"- **`hcat:code` is hierarchical.** The first 4/6/8 digits are increasingly specific crop groups; compare prefixes, not equality, to aggregate (see the crop query below). Source crops without a mapping in the converter's HCAT table (`{meta.get('ec_mapping_csv')}`) have `NULL`.")
    if latest.collection_props:
        a.append("- **Some fiboa properties are not columns.** Values constant for the whole file are stored once in the GeoParquet `collection` key-value metadata: " + ", ".join(f"`{k}` = `{v}`" for k, v in latest.collection_props.items()) + f" ({latest.year} edition). Read them with `parquet_kv_metadata()` in DuckDB or `pyarrow.parquet.ParquetFile(f).schema_arrow.metadata[b'collection']`; they differ per edition where the source does.")
    if ds.notes:
        a.append(f"- {ds.notes}")
    a += ["", "## Tested queries", ""]
    a.append("Fields and hectares per edition, through the partition glob:")
    a.append("")
    area_expr = 'round(sum("metrics:area") / 1e4) AS hectares' if any(c["name"] == "metrics:area" for c in columns) else "0 AS hectares"
    q = f"INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;\nSELECT {PARTITION_KEY}, count(*) AS fields, {area_expr}\nFROM read_parquet('{glob}', hive_partitioning = true)\nGROUP BY {PARTITION_KEY} ORDER BY {PARTITION_KEY};"
    a += [md_query(q, public_base), ""]
    if hcat_cols:
        a.append("Largest crop groups in the latest edition (HCAT level 3 = first 6 digits):")
        a.append("")
        q = f"SELECT substr(CAST(\"hcat:code\" AS VARCHAR), 1, 6) AS hcat_group, mode(\"hcat:name\") AS most_common_name,\n       count(*) AS fields, round(sum(\"metrics:area\") / 1e4) AS hectares\nFROM read_parquet('{latest_url}')\nWHERE \"hcat:code\" IS NOT NULL\nGROUP BY 1 ORDER BY hectares DESC LIMIT 5;"
        a += [md_query(q, public_base), ""]
    a.append("Fields around a point, transforming the point into the data's CRS instead of the data into WGS84:")
    a.append("")
    cx = (latest.bbox[0] + latest.bbox[2]) / 2
    cy = (latest.bbox[1] + latest.bbox[3]) / 2
    q = f"INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;\nSELECT id, round(\"metrics:area\") AS m2\nFROM read_parquet('{latest_url}')\nWHERE ST_Intersects(geometry, ST_Buffer(ST_Transform(ST_Point({cy:.4f}, {cx:.4f}), 'EPSG:4326', '{latest.crs}'), 500))\nLIMIT 5;"
    try:
        a += [md_query(q, public_base), ""]
    except Exception as exc:  # noqa: BLE001 — a failed recipe is not shipped
        print(f"note: spatial query skipped for {ds.id}: {exc}")
    a += ["## Related collections", "", f"Every collection in this catalog shares the fiboa core columns, so the same queries work across countries; `{public_base}/*/latest/*.parquet` with `union_by_name = true` reads the newest edition of all of them (see the catalog [AGENTS.md]({human_base}/AGENTS.md)).", "", "## Structure", "", "Assets and structural links resolve relative to the object that carries them; there is no `self` link. Source: this collection is generated by [tools/catalogize.py]({0}/blob/main/tools/catalogize.py) in the catalog repository — fix documentation there.".format(manifest.catalog["repository"])]
    write_text(cdir / "AGENTS.md", "\n".join(a))

    # -- llms.txt
    l = [f"# {meta['title']}", "", f"{meta['short_name']} field boundaries ({', '.join(y.year for y in years)}) as fiboa GeoParquet + PMTiles, mirrored by {manifest.host['name']} from {provider_name or 'the source'}. License: {lic}.", ""]
    l.append(f"- Latest: {latest_url}")
    l.append(f"- All editions: {glob} (hive_partitioning=true adds `{PARTITION_KEY}`)")
    l.append(f"- CRS {latest.crs}; `metrics:area` in m²; `{PARTITION_KEY}` = edition, `id` unique per edition only.")
    l.append(f"- Columns: {', '.join(c['name'] for c in columns)}")
    l.append(f"- Docs: {human_base}/{ds.id}/README.md, agent guide {human_base}/{ds.id}/AGENTS.md, STAC {public_base}/{ds.id}/collection.json")
    write_text(cdir / "llms.txt", "\n".join(l))


# --- root -------------------------------------------------------------------------------


def build_root(manifest: Manifest, public_base: str, human_base: str) -> None:
    collections = []
    for path in sorted(CATALOG_DIR.glob("*/collection.json")):
        collections.append(read_json(path))
    if not collections:
        print("note: no collections yet; root catalog will have no children")
    cat = manifest.catalog
    repo = cat["repository"]
    n_fields = sum(c.get("table:row_count") or 0 for c in collections)
    countries = sorted({c["id"].split("_")[0].upper() for c in collections})
    description = (
        f"Official, non-AI field boundary datasets — typically published by governments from their agricultural "
        f"subsidy registers (IACS/LPIS), cadastres and statistics — harmonized into the [fiboa]({FIBOA_SPEC}) schema "
        f"with [fiboa-cli]({FIBOA_CLI_REPO}) and republished as cloud-native GeoParquet and PMTiles. "
        f"{len(collections)} collections ({', '.join(countries)}), {fmt_int(n_fields)} fields in their latest editions. "
        f"Each collection is one source dataset, partitioned by edition year; `*/latest/*.parquet` reads the newest "
        f"edition of every collection. Hosted by [{manifest.host['name']}]({manifest.host['url']}) on "
        f"[Source Cooperative]({human_base}); the metadata is maintained in the "
        f"[harmonized-field-data-catalog repository]({repo}), where corrections are welcome as pull requests. "
        f"Start at the catalog [AGENTS.md]({human_base}/AGENTS.md) for cross-dataset queries."
    )
    root = {
        "type": "Catalog",
        "stac_version": "1.1.0",
        "stac_extensions": [PORTOLAN_EXTENSION],
        "id": cat["id"],
        "title": cat["title"],
        "description": description,
        "links": [
            {"rel": "root", "href": "./catalog.json", "type": "application/json", "title": cat["title"]},
            *[
                {"rel": "child", "href": f"./{c['id']}/collection.json", "type": "application/json", "title": c["title"]}
                for c in collections
            ],
            {"rel": "about", "href": human_base, "type": "text/html", "title": "Dataset home page on Source Cooperative"},
            {"rel": "vcs", "href": repo, "type": "text/html", "title": "Source repository"},
            {"rel": "issues", "href": f"{repo}/issues", "type": "text/html", "title": "Issue tracker"},
            {"rel": "agents", "href": "./AGENTS.md", "type": "text/markdown", "title": "Guidance for AI agents"},
            {"rel": "describedby", "href": "./README.md", "type": "text/markdown", "title": "Human-readable documentation"},
            {"rel": "llms", "href": "./llms.txt", "type": "text/markdown", "title": "Agent/LLM usage guide"},
        ],
        "updated": max([c.get("updated", "") for c in collections] or [dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")]),
    }
    write_json(CATALOG_DIR / "catalog.json", root)

    # README.md
    r = [f"# {cat['title']}", "", description, "", "## Collections", "", "| Collection | Source data provider | Editions | Fields (latest) | License | Docs |", "|---|---|---|---:|---|---|"]
    for c in collections:
        years = [str(link["title"]).rsplit(" ", 1)[-1] for link in c["links"] if link["rel"] == "item"]
        producer = next((p for p in c.get("providers", []) if "producer" in p.get("roles", [])), {})
        prov = f"[{producer.get('name', '—')}]({producer['url']})" if producer.get("url") else producer.get("name", "—")
        r.append(f"| [{c['title']}]({human_base}/{c['id']}) | {prov} | {', '.join(years)} | {fmt_int(c.get('table:row_count'))} | {c['license']} | [README]({human_base}/{c['id']}/README.md) · [agents]({human_base}/{c['id']}/AGENTS.md) |")
    r += ["", "## Access", "", "Everything is static files on object storage: query them in place with DuckDB, GeoPandas or any GeoParquet reader, and render the PMTiles with MapLibre. Newest edition of every collection:", ""]
    q = f"INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;\nSELECT regexp_extract(filename, '/([^/]+)/latest/', 1) AS collection, count(*) AS fields\nFROM read_parquet('{public_base}/*/latest/*.parquet', union_by_name = true, filename = true)\nGROUP BY 1 ORDER BY 1;"
    r += [md_query(q, public_base), ""]
    r += ["## License", "", "Each collection carries the license of its source data provider (see the table and each `collection.json`). The catalog metadata, styles and tooling are Apache-2.0, in the [repository]({0}).".format(repo), "", "## Provenance", "", f"A mirror: every collection links its original source (`rel: via`) and the fiboa data survey entry describing it, and records the fiboa-cli version that converted it. Conversion logic lives in [fiboa-cli]({FIBOA_CLI_REPO}); this repository only orchestrates publication. Previously published at [source.coop/fiboa/data](https://source.coop/fiboa/data)."]
    write_text(CATALOG_DIR / "README.md", "\n".join(r))

    # AGENTS.md
    a = [f"# Agent guidance — {cat['title']}", "", "**One rule survives every edit to this file.** Every claim here is quoted from a source or measured from the data; every query below was run before it was written down and its output follows as comments.", ""]
    a += ["## What this catalog holds", "", f"{len(collections)} collections, one per source dataset, all in the [fiboa]({FIBOA_SPEC}) schema (`id`, `geometry`, `bbox`, optional `metrics:area` in m², `determination:datetime`, crop columns where the source has them). Public root: `{public_base}/catalog.json`. Each collection is hive-partitioned by edition: `<collection>/year=<Y>/<collection>-<Y>.parquet`, with the newest edition copied to `<collection>/latest/<collection>.parquet`.", ""]
    a += ["## How to read it", "", "Newest edition of every collection in one query (schemas differ per source, hence `union_by_name`):", "", md_query(q, public_base), ""]
    q2 = f"SELECT {PARTITION_KEY}, regexp_extract(filename, '/([^/]+)/{PARTITION_KEY}=', 1) AS collection, count(*) AS fields\nFROM read_parquet('{public_base}/*/{PARTITION_KEY}=*/*.parquet', hive_partitioning = true, union_by_name = true, filename = true)\nGROUP BY 1, 2 ORDER BY 2, 1;"
    a += ["Every edition of every collection:", "", md_query(q2, public_base), ""]
    a += ["## Join keys", "", "There are none. `id` is unique within one edition of one collection only; collections do not share identifiers and editions are not tracked across years. Spatial joins are the only bridge, and each collection is in its own CRS (`proj:code` on the collection and the `data` asset), so transform before joining.", ""]
    a += ["## Quirks that produce silently wrong answers", "", "- Geometries are in the source CRS, not WGS84. `summaries.proj:code` per collection.", "- `metrics:area` is square metres; `year` is the edition (publication) year, not an observation date.", "- Crop columns differ per source: `crop:code`/`crop:name` are the source's own code list; `hcat:code`/`hcat:name` (where present) are the harmonized EuroCrops HCAT taxonomy, hierarchical by digit prefix.", "- Some sources publish field *blocks* (reference parcels) rather than crop fields; the collection description says which.", ""]
    a += ["## Structure", "", f"Assets and structural links resolve relative to the object that carries them; catalogs carry no `self` link. Generated by [tools/catalogize.py]({repo}/blob/main/tools/catalogize.py); fix documentation there."]
    write_text(CATALOG_DIR / "AGENTS.md", "\n".join(a))

    # llms.txt
    l = [f"# {cat['title']}", "", f"Official (non-AI) field boundaries harmonized to fiboa, {len(collections)} collections, GeoParquet + PMTiles on Source Cooperative. Root: {public_base}/catalog.json. Agent guide: {human_base}/AGENTS.md.", ""]
    for c in collections:
        l.append(f"- {c['id']}: {c['title']} — {public_base}/{c['id']}/latest/{c['id']}.parquet (license {c['license']}, CRS {', '.join(c.get('summaries', {}).get('proj:code', []))})")
    l += ["", f"All newest editions: {public_base}/*/latest/*.parquet (union_by_name=true). Per-edition: {public_base}/<id>/year=*/*.parquet (hive_partitioning=true)."]
    write_text(CATALOG_DIR / "llms.txt", "\n".join(l))


# --- main -------------------------------------------------------------------------------


def catalogize(dataset_id: str, manifest: Manifest) -> None:
    if dataset_id not in manifest.datasets:
        sys.exit(f"{dataset_id} is not in datasets.yaml")
    ds = manifest.datasets[dataset_id]
    config = publish_config()
    public_base = config["public_base"].rstrip("/")
    human_base = manifest.catalog["human_base"].rstrip("/")
    meta = load_converter_meta(ds.id)
    years = [YearInput(ds.id, y) for y in ds.years]
    latest = years[-1]

    # data files: symlink into catalog/ (gitignored) so local gates resolve them
    for y in years:
        link_data_file(y.parquet, catalog_year_dir(ds.id, y.year) / y.parquet.name)
        if y.visual_asset:
            link_data_file(y.pmtiles, catalog_year_dir(ds.id, y.year) / y.pmtiles.name)
    latest_copy = STAGING_DIR / ds.id / "latest" / f"{ds.id}.parquet"
    latest_copy.parent.mkdir(parents=True, exist_ok=True)
    if latest_copy.exists() or latest_copy.is_symlink():
        latest_copy.unlink()
    os.link(latest.parquet, latest_copy)
    link_data_file(latest_copy, CATALOG_DIR / ds.id / "latest" / f"{ds.id}.parquet")

    survey_url, survey_props = data_survey(ds.id)
    table_columns = describe_columns(latest.data_asset.get("table:columns", []), meta, survey_props)
    style_assets, style_facts = build_styles(ds, meta, latest)
    items = build_items(ds, meta, years, public_base, table_columns)
    collection = build_collection(ds, meta, years, items, manifest, public_base, human_base, table_columns, style_assets, survey_url)

    for y, item in zip(years, items):
        write_json(catalog_year_dir(ds.id, y.year) / f"{item['id']}.json", item)
    write_json(CATALOG_DIR / ds.id / "collection.json", collection)
    collection_docs(ds, meta, years, collection, manifest, public_base, human_base, survey_url, style_facts)
    print(f"catalogized {ds.id}: {len(years)} edition(s), {len(style_assets)} style(s), {len(table_columns)} columns")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("datasets", nargs="*", help="dataset ids from datasets.yaml")
    parser.add_argument("--root", action="store_true", help="(re)generate the catalog root")
    args = parser.parse_args()
    manifest = Manifest.load()
    config = publish_config()
    for dataset_id in args.datasets:
        catalogize(dataset_id, manifest)
    if args.root or args.datasets:
        build_root(manifest, config["public_base"].rstrip("/"), manifest.catalog["human_base"].rstrip("/"))
        print("catalog root regenerated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
