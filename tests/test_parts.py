#!/usr/bin/env python3
"""A collection with parts is staged and catalogized per part.

Builds a two-part ``ch`` in a temp tree without fiboa-cli (convert, validate,
describe and the tiles are stood in for by tests/fixtures.py) and checks what
the plan promises:

- a part without years is filed under the most frequent year in its data;
- every part edition gets its own item, with its source's license,
  attribution, providers and via;
- latest/<part>.parquet is the newest edition of each part;
- the collection is `other` with one license link per distinct license, lists
  every source as a provider and the host last, and shows one PMTiles;
- output left from an earlier layout (the national ch-2025 item) is removed;
- upload_data.py picks up the new files and none of the staged records;
- rashid finds nothing blocking in the result, when it is installed.

Needs duckdb with the spatial extension, so it SKIPs where that is missing
(CI installs only the validators).

Run: python tests/test_parts.py
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

if not all(importlib.util.find_spec(m) for m in ("duckdb", "requests")):
    print("SKIP: duckdb/requests not installed; run in the pixi environment")
    raise SystemExit(0)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fixtures import converter_meta, point_tooling_at, write_parquet, write_staged_stac  # noqa: E402

import build  # noqa: E402
import catalogize  # noqa: E402
import common  # noqa: E402
import upload_data  # noqa: E402
from common import Manifest, determination_years, publish_config, write_json  # noqa: E402

errors: list[str] = []


def check(ok: bool, what: str) -> None:
    if not ok:
        errors.append(what)


TERMS = "https://example.org/bb/terms"
FIBOA = "https://fiboa.org/specification/v0.3.0/schema.yaml"
HCAT = "https://fiboa.org/hcat-extension/v0.3.0/schema.yaml"
CROP = "https://fiboa.org/crop-extension/v0.2.0/schema.yaml"
PARTS = {
    # a source without variants: its current state, mostly 2026 with some 2025
    "ch_aa": {
        "x0": 7.0,
        "years": [2026] * 4 + [2025] * 2,
        "meta": converter_meta("ch_aa", "Switzerland, Aa", "Kanton Aa, via geodienste.ch <https://example.org/aa>", "Kanton Aa — Nutzungsflächen", "CC-BY-4.0"),
        "provider": {"name": "Kanton Aa, via geodienste.ch", "roles": ["producer", "licensor"], "url": "https://example.org/aa"},
        "license": ("CC-BY-4.0", None),
        "extensions": [HCAT, FIBOA],
    },
    # a source with variants and its own terms; a year that is the same for
    # every row is stored in the file metadata, not as a column
    "ch_bb": {
        "x0": 8.0,
        "meta": converter_meta("ch_bb", "Switzerland, Bb", "Kanton Bb <https://example.org/bb>", "Quelle: Kanton Bb", f"Terms of use <{TERMS}>"),
        "provider": {"name": "Kanton Bb", "roles": ["producer", "licensor"], "url": "https://example.org/bb"},
        "license": ("other", TERMS),
        "extensions": [FIBOA, CROP],
    },
}
SURVEY = """# Switzerland

## Overview

The usage areas of the cantons, each under its own terms.
Zürich keeps [earlier years](CH-ZH.md).

## Data
"""

tmp = Path(tempfile.mkdtemp())
try:
    point_tooling_at(tmp, build, catalogize, upload_data)
    real = common.Manifest.load()
    manifest_path = tmp / "datasets.yaml"
    manifest_path.write_text(json.dumps({
        "catalog": real.catalog,
        "host": real.host,
        "datasets": {
            "ch": {
                "title": "Field boundaries for Switzerland",
                "boundaries": "declared",
                "keywords": ["Switzerland"],
                "via": "https://example.org/geodienste",
                "parts": {"ch_aa": None, "ch_bb": {"years": ["2024", "2025"], "notes": "Bb note."}},
            }
        },
    }))
    manifest = Manifest.load(manifest_path)
    ds = manifest.datasets["ch"]

    # -- build: stand in for fiboa-cli and the tilers
    converted, tiled = [], {}

    def fake_convert(converter_id, parquet, variant=None):
        converted.append((converter_id, variant))
        part = PARTS[converter_id]
        years = part.get("years") or [int(variant)] * (3 if variant == "2024" else 5)
        write_parquet(parquet, part["x0"], years, hoist_year="years" not in part)

    def fake_describe(part_id, parquet, pmtiles, stac_file):
        lic, link = PARTS[part_id]["license"]
        write_staged_stac(stac_file, part_id, parquet, lic, PARTS[part_id]["provider"], link, PARTS[part_id]["extensions"])

    def fake_meta(converter_id, out):
        write_json(out, PARTS[converter_id]["meta"])

    def fake_pmtiles(sources, pmtiles, layer, attribution=None):
        tiled.update(sources=sources, layer=layer, attribution=attribution)
        pmtiles.parent.mkdir(parents=True, exist_ok=True)
        pmtiles.write_bytes(b"PMTiles" + bytes(120))

    build.convert, build.describe, build.converter_meta, build.make_pmtiles = fake_convert, fake_describe, fake_meta, fake_pmtiles
    build.run = lambda cmd, **kwargs: None  # fiboa validate
    jumps = build.prepare(ds, None, skip_convert=False)

    staging = tmp / "staging" / "ch"
    check(sorted(converted) == [("ch_aa", None), ("ch_bb", "2024"), ("ch_bb", "2025")], f"conversions: {converted}")
    check((staging / "year=2026" / "ch_aa-2026.parquet").is_file(), "ch_aa is not filed under 2026, its most frequent year")
    check(not (staging / "tmp" / "ch_aa.parquet").exists(), "the temporary conversion is left behind")
    check(determination_years(staging / "year=2026" / "ch_aa-2026.parquet") == [("2026", 4), ("2025", 2)], "years of a mixed file")
    check(determination_years(staging / "year=2025" / "ch_bb-2025.parquet") == [("2025", 5)], "a year stored in the file metadata is not read")
    check(ds.editions() == [("ch_bb", "2024"), ("ch_bb", "2025"), ("ch_aa", "2026")], f"editions: {ds.editions()}")
    check(ds.latest_per_part() == {"ch_aa": "2026", "ch_bb": "2025"}, f"latest per part: {ds.latest_per_part()}")
    check([p.name for p in tiled.get("sources", [])] == ["ch_aa-2026.parquet", "ch_bb-2025.parquet"], f"tiles are not the newest edition of every part: {tiled}")
    check(tiled.get("layer") == "ch", "tile layer is not the collection id")
    check(tiled.get("attribution") == "Kanton Aa — Nutzungsflächen; Quelle: Kanton Bb", f"tile attribution: {tiled.get('attribution')}")
    check(any("ch/ch_bb 2025" in j for j in jumps), f"the row-count check does not run per part: {jumps}")

    # a staged snapshot is reused, not converted again
    converted.clear()
    build.stage_part_snapshot("ch", "ch_aa")
    check(converted == [], "a staged snapshot was converted again")

    # -- catalogize, over output left by the national build
    old = tmp / "catalog" / "ch" / "year=2025" / "ch-2025.json"
    old.parent.mkdir(parents=True)
    old.write_text("{}")
    (tmp / "catalog" / "ch" / "thumbnail.jpg").write_bytes(b"\xff\xd8\xff\xd9")  # thumbnail.py renders the real one
    survey_url = "https://github.com/fiboa/data-survey/blob/main/data/CH.md"
    catalogize.survey_text = lambda dataset_id: (survey_url, SURVEY)
    catalogize.catalogize("ch", manifest)
    catalogize.build_root(manifest, publish_config()["public_base"].rstrip("/"), manifest.catalog["human_base"].rstrip("/"))

    cdir = tmp / "catalog" / "ch"
    check(not old.exists(), "the national ch-2025 item is left behind")
    coll = json.loads((cdir / "collection.json").read_text())
    items = {p.name: json.loads(p.read_text()) for p in cdir.glob("year=*/*.json")}
    check(sorted(items) == ["ch_aa-2026.json", "ch_bb-2024.json", "ch_bb-2025.json"], f"items: {sorted(items)}")

    aa, bb = items.get("ch_aa-2026.json", {}), items.get("ch_bb-2025.json", {})
    check(aa.get("properties", {}).get("license") == "CC-BY-4.0", "ch_aa item license")
    check(bb.get("properties", {}).get("license") == "other", "ch_bb item license")
    check(any(link["rel"] == "license" and link["href"] == TERMS for link in bb.get("links", [])), "ch_bb item has no link to its terms")
    check(aa.get("properties", {}).get("attribution") == "Kanton Aa — Nutzungsflächen", "ch_aa item attribution")
    check([p["name"] for p in aa.get("properties", {}).get("providers", [])] == ["Kanton Aa, via geodienste.ch"], "ch_aa item providers")
    check([p["name"] for p in bb.get("properties", {}).get("providers", [])] == ["Kanton Bb"], "ch_bb item providers")
    check({"rel": "via", "href": "https://example.org/aa", "type": "text/html", "title": "Original source (publisher page)"} in aa.get("links", []), "ch_aa item via")
    check(aa.get("collection") == "ch" and aa.get("properties", {}).get("year") == 2026, "ch_aa item collection/year")
    check("4 fields are from 2026, 2 from 2025" in aa.get("properties", {}).get("description", ""), "a mixed file is not noted in its item")
    check("Bb note." in bb.get("properties", {}).get("description", ""), "part notes are not in the item")

    for part_id, year in (("ch_aa", "2026"), ("ch_bb", "2025")):
        link = cdir / "latest" / f"{part_id}.parquet"
        check(link.is_symlink() and link.resolve().samefile(staging / f"year={year}" / f"{part_id}-{year}.parquet"), f"latest/{part_id}.parquet is not its {year} edition")
    check((cdir / "latest" / "ch.pmtiles").resolve() == (staging / "latest" / "ch.pmtiles").resolve(), "latest/ch.pmtiles is not linked")

    check(coll["license"] == "other", "collection license")
    license_links = sorted(link["href"] for link in coll["links"] if link["rel"] == "license")
    check(license_links == sorted(["https://spdx.org/licenses/CC-BY-4.0.html", TERMS]), f"collection license links: {license_links}")
    names = [p["name"] for p in coll["providers"]]
    check(names == ["Kanton Aa, via geodienste.ch", "Kanton Bb", real.host["name"]], f"collection providers: {names}")
    check(coll["title"] == "Field boundaries for Switzerland", "collection title is not the manifest's")
    check(coll["description"].startswith("The usage areas of the cantons, each under its own terms. Zürich keeps [earlier years](https://github.com/fiboa/data-survey/blob/main/data/CH-ZH.md)."), "description is not the survey overview with absolute links")
    check("fed by 2 fiboa-cli converters" in coll["description"], "description does not say how many sources")
    check(coll["assets"]["visual"]["href"] == "./latest/ch.pmtiles", "visual asset")
    check(any(link["rel"] == "pmtiles" and link["href"] == "./latest/ch.pmtiles" for link in coll["links"]), "pmtiles link")
    check(not any("data" in a.get("roles", []) for a in coll["assets"].values()), "the collection carries no data asset; its items do")
    extensions = coll.get("vecorel_extensions")
    check(extensions == {"ch": sorted([CROP, FIBOA, HCAT])}, f"the extensions of every part, under the collection id: {extensions}")
    check(coll["table:row_count"] == 6 + 5, f"row count of the newest editions: {coll['table:row_count']}")
    check(len([link for link in coll["links"] if link["rel"] == "item"]) == 3, "item links")
    check(coll.get("via") is None and {"rel": "via", "href": "https://example.org/geodienste", "type": "text/html", "title": "Original source (publisher page)"} in coll["links"], "collection via")
    for doc in ("README.md", "AGENTS.md", "llms.txt"):
        check((cdir / doc).is_file(), f"missing {doc}")
    agents = (cdir / "AGENTS.md").read_text()
    check("-- 2026 | ch_aa | 6" in agents, "the per-edition query did not run over the local files")

    # the data upload picks up every part edition, latest per part and the tiles, not the records
    keys = sorted(u.key for u in upload_data.collect("ch", "p"))
    check(keys == [
        "p/ch/latest/ch.pmtiles", "p/ch/latest/ch_aa.parquet", "p/ch/latest/ch_bb.parquet",
        "p/ch/year=2024/ch_bb-2024.parquet", "p/ch/year=2025/ch_bb-2025.parquet", "p/ch/year=2026/ch_aa-2026.parquet",
    ], f"upload keys: {keys}")

    if shutil.which("rashid"):
        result = subprocess.run(["rashid", "check", str(tmp / "catalog"), "--no-data", "--json"], capture_output=True, text=True)
        findings = json.loads(result.stdout).get("findings", [])
        for f in findings:
            if f.get("severity") == "error":
                errors.append(f"rashid {f.get('rule_id')} {f.get('path')}: {f.get('message')}")
    else:
        print("note: rashid not installed; conformance of the parts output not checked")
finally:
    if not os.environ.get("KEEP_TMP"):
        shutil.rmtree(tmp, ignore_errors=True)
    else:
        print(f"kept {tmp}")

if errors:
    print("\n".join(f"error  {e}" for e in errors))
    raise SystemExit(1)
print("OK: a parts collection is staged and catalogized per part")
