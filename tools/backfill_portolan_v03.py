#!/usr/bin/env python3
"""One-time backfill: apply the Portolan v0.3.0 migration to already-committed
``catalog/**/*.json`` without re-deriving facts from data.

Why this exists instead of a plain ``tools/build.py <id>`` rebuild: this
machine cannot download the hundreds of GB of source GeoParquet/PMTiles that a
real rebuild would stage (see the Slurm/bandwidth constraints in the migration
PR). ``tools/catalogize.py`` and ``tools/catalogize_parts.py`` are already
fixed so that the *next* real build produces this output directly — see
``PORTOLAN_EXTENSION`` in ``tools/common.py`` and the new
``item_data_description`` / ``item_visual_description`` helpers and the
``thumbnail_asset`` / collection ``visual`` asset literals in
``tools/catalogize.py`` and ``tools/catalogize_parts.py``.

This script reconstructs the identical strings those functions now produce,
using only fields already present in the committed JSON (title, year,
basemap choice inferred from the existing title text) — no parquet/PMTiles
read, no network. Run once; a future real rebuild is idempotent with it.

Also applies PORTO-FMT-066 (``storage:schemes``, added to this PR after a
sibling migration's rashid run showed a local ``--no-data`` pass cannot
prove a live partition listing actually works): every collection's
``storage:schemes`` and ``stac_extensions`` are set to match
``common.storage_schemes()`` / ``common.STORAGE_EXTENSION``, which read the
real `catalog.publish.yaml` — this one touches config, unlike the
text-only patches above.

    python3 tools/backfill_portolan_v03.py           # dry run, prints a diff summary
    python3 tools/backfill_portolan_v03.py --write   # writes catalog/**/*.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_DIR = ROOT / "catalog"
TOOLS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_DIR))

import common  # noqa: E402

OLD_SCHEMA_RE = re.compile(r"https://schemas\.portolan-sdi\.org/portolan/v[\d.]+/schema\.json")
NEW_SCHEMA = "https://schemas.portolan-sdi.org/portolan/v0.3.0/schema.json"


def ensure_extension(extensions: list[str], ext: str) -> tuple[list[str], bool]:
    if ext in extensions:
        return extensions, False
    return [*extensions, ext], True


def bump_schema_uri(extensions: list[str]) -> tuple[list[str], bool]:
    changed = False
    out = []
    for ext in extensions:
        if OLD_SCHEMA_RE.fullmatch(ext) and ext != NEW_SCHEMA:
            out.append(NEW_SCHEMA)
            changed = True
        else:
            out.append(ext)
    return out, changed


def thumbnail_description(title: str) -> str:
    if "over a light basemap" in title:
        return "Static JPEG image rendered from the collection's default style over a light OpenStreetMap/CARTO basemap."
    return "Static JPEG image rendered from the collection's default style, with no basemap."


def collection_visual_description(title: str) -> str:
    if title.endswith("of every source (PMTiles)"):
        return (
            "PMTiles vector tiles of the newest edition of every source feeding this collection, "
            "for rendering this collection's styles (`styles/`) in a web map. The underlying "
            "GeoParquet is each item's `data` asset and this collection's `partition:glob`."
        )
    m = re.search(r"\((\d{4})\)\s*\(PMTiles\)$", title)
    year = m.group(1) if m else None
    return (
        f"PMTiles vector tiles of the {year} edition, for rendering this collection's styles "
        f"(`styles/`) in a web map. The underlying GeoParquet is the `data` asset and `partition:glob`."
        if year
        else (
            "PMTiles vector tiles of the latest edition, for rendering this collection's styles "
            "(`styles/`) in a web map. The underlying GeoParquet is the `data` asset and `partition:glob`."
        )
    )


def item_data_description(short_name: str, year: str) -> str:
    return (
        f"GeoParquet file for the {year} edition of {short_name}, partition "
        f"`year={year}` of the collection. Converted with fiboa-cli into the fiboa schema."
    )


def item_visual_description(short_name: str, year: str) -> str:
    return f"PMTiles vector tiles of the {year} edition of {short_name}, generated from this item's `data` asset."


def short_name_from_asset_title(title: str, year: str, suffix: str) -> str | None:
    marker = f" {year} ({suffix})"
    if title.endswith(marker):
        return title[: -len(marker)]
    return None


def patch_collection(doc: dict, schemes: dict) -> bool:
    changed = False
    if "stac_extensions" in doc:
        doc["stac_extensions"], c = bump_schema_uri(doc["stac_extensions"])
        changed |= c

    assets = doc.get("assets", {})
    thumb = assets.get("thumbnail")
    if thumb and not thumb.get("description"):
        thumb["description"] = thumbnail_description(thumb.get("title", ""))
        changed = True

    visual = assets.get("visual")
    if visual and not visual.get("description"):
        visual["description"] = collection_visual_description(visual.get("title", ""))
        changed = True

    # PORTO-FMT-066: every collection with a partition:glob needs a
    # storage:schemes entry naming the proxy as custom-s3, or a client (and
    # rashid's --data pass) assumes AWS S3's hostname template and the glob
    # listing is denied.
    if "partition:glob" in doc and doc.get("storage:schemes") != schemes:
        doc["storage:schemes"] = schemes
        doc["stac_extensions"], c = ensure_extension(doc.get("stac_extensions", []), common.STORAGE_EXTENSION)
        changed = True

    return changed


def patch_catalog_root(doc: dict) -> bool:
    if "stac_extensions" not in doc:
        return False
    doc["stac_extensions"], changed = bump_schema_uri(doc["stac_extensions"])
    return changed


def patch_item(doc: dict) -> bool:
    changed = False
    year = str(doc.get("properties", {}).get("year") or "")
    assets = doc.get("assets", {})

    data = assets.get("data")
    if data and not data.get("description") and year:
        short_name = short_name_from_asset_title(data.get("title", ""), year, "GeoParquet")
        if short_name:
            data["description"] = item_data_description(short_name, year)
            changed = True

    visual = assets.get("visual")
    if visual and not visual.get("description") and year:
        short_name = short_name_from_asset_title(visual.get("title", ""), year, "PMTiles")
        if short_name:
            visual["description"] = item_visual_description(short_name, year)
            changed = True

    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    schemes = common.storage_schemes(common.publish_config())

    touched: list[Path] = []
    unpatched_assets: list[str] = []
    unpatched_schemes: list[str] = []

    for path in sorted(CATALOG_DIR.rglob("*.json")):
        rel = path.relative_to(CATALOG_DIR)
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if not isinstance(doc, dict):
            continue

        if rel == Path("catalog.json"):
            changed = patch_catalog_root(doc)
        elif path.name == "collection.json":
            changed = patch_collection(doc, schemes)
        elif doc.get("type") == "Feature":
            changed = patch_item(doc)
        else:
            changed = False

        if changed:
            touched.append(path)
            if args.write:
                path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        # Report anything that still looks unpatched after this pass (either
        # because it was already fine, or the title didn't match the
        # expected template, so nothing was guessed) — checked against the
        # patched in-memory doc, not the pre-patch bytes on disk.
        for name, asset in doc.get("assets", {}).items():
            if name in ("thumbnail", "visual", "data") and not asset.get("description"):
                unpatched_assets.append(f"{rel}: asset '{name}'")
        if path.name == "collection.json" and "partition:glob" in doc and doc.get("storage:schemes") != schemes:
            unpatched_schemes.append(str(rel))

    mode = "would patch" if not args.write else "patched"
    print(f"{mode} {len(touched)} file(s)")
    ok = True
    if unpatched_assets:
        ok = False
        print(f"\n{len(unpatched_assets)} asset(s) still missing a description (title did not match the expected template):")
        for u in unpatched_assets[:50]:
            print(f"  {u}")
        if len(unpatched_assets) > 50:
            print(f"  ... and {len(unpatched_assets) - 50} more")
    if unpatched_schemes:
        ok = False
        print(f"\n{len(unpatched_schemes)} collection(s) still missing the storage:schemes entry:")
        for u in unpatched_schemes[:50]:
            print(f"  {u}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
