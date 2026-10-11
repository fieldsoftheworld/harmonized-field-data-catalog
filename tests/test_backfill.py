#!/usr/bin/env python3
"""A dataset with ``backfill`` takes the years its own source lacks from another converter.

Builds a ``fr`` whose own converter has 2017 and 2019 and whose ``ec_fr``
backfills 2015 and 2018, in a temp tree without fiboa-cli (convert, validate,
describe and the tiles are stood in for by tests/fixtures.py), and checks:

- every year is converted by its own converter and filed as ``fr-<Y>``;
- only the newest year is tiled, as layer ``fr``, and is ``latest``;
- a backfilled item carries its source's license, attribution, providers, via
  and converter link; the dataset's own items stay as they were;
- the collection keeps the dataset's own license, names the backfill source as
  a provider and says which editions it supplies, as do the docs;
- upload_data.py picks up every edition under the dataset's own name;
- rashid finds nothing blocking in the result, when it is installed.

Needs duckdb with the spatial extension, so it SKIPs where that is missing.

Run: python tests/test_backfill.py
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
from common import Manifest, publish_config, write_json  # noqa: E402

errors: list[str] = []


def check(ok: bool, what: str) -> None:
    if not ok:
        errors.append(what)


TERMS = "https://example.org/fr/terms"
CONVERTERS = {
    "fr": {
        "meta": converter_meta("fr", "France", "IGN <https://example.org/ign>", "IGN", f"Open Licence <{TERMS}>"),
        "provider": {"name": "IGN", "roles": ["producer", "licensor"], "url": "https://example.org/ign"},
        "license": ("other", TERMS),
    },
    "ec_fr": {
        "meta": converter_meta("ec_fr", "France - EuroCrops", "JRC <https://example.org/jrc>", "European Commission, JRC", "CC-BY-4.0"),
        "provider": {"name": "JRC", "roles": ["producer", "licensor"], "url": "https://example.org/jrc"},
        "license": ("CC-BY-4.0", None),
    },
}

tmp = Path(tempfile.mkdtemp())
try:
    point_tooling_at(tmp, build, catalogize, upload_data)
    real = common.Manifest.load()
    manifest_path = tmp / "datasets.yaml"
    manifest_path.write_text(json.dumps({
        "catalog": real.catalog,
        "host": real.host,
        "datasets": {
            "fr": {
                "years": ["2017", "2019"],
                "boundaries": "declared",
                "keywords": ["France"],
                "backfill": {"ec_fr": {"years": ["2015", "2018"], "notes": "EC note."}},
            }
        },
    }))
    manifest = Manifest.load(manifest_path)
    ds = manifest.datasets["fr"]
    check(ds.years == ["2015", "2017", "2018", "2019"], f"years: {ds.years}")
    check([ds.converter(y) for y in ds.years] == ["ec_fr", "fr", "ec_fr", "fr"], "converter per year")

    # -- build: stand in for fiboa-cli and the tilers
    converted, described, tiled = [], [], []

    def fake_convert(converter_id, parquet, variant=None):
        converted.append((converter_id, variant))
        write_parquet(parquet, 2.0, [int(variant)] * (4 if converter_id == "fr" else 3))

    def fake_describe(converter_id, parquet, pmtiles, stac_file, layer=None):
        described.append((converter_id, parquet.name))
        c = CONVERTERS[converter_id]
        lic, link = c["license"]
        write_staged_stac(stac_file, converter_id, parquet, lic, c["provider"], link)

    def fake_meta(converter_id, out):
        write_json(out, CONVERTERS[converter_id]["meta"])

    def fake_pmtiles(sources, pmtiles, layer, attribution=None):
        tiled.append((Path(sources).name, layer))
        pmtiles.write_bytes(b"PMTiles" + bytes(120))

    build.convert, build.describe, build.converter_meta, build.make_pmtiles = fake_convert, fake_describe, fake_meta, fake_pmtiles
    build.run = lambda cmd, **kwargs: None  # fiboa validate
    build.prepare(ds, None, skip_convert=False)

    staging = tmp / "staging" / "fr"
    check(converted == [("ec_fr", "2015"), ("fr", "2017"), ("ec_fr", "2018"), ("fr", "2019")], f"conversions: {converted}")
    check(described == [("ec_fr", "fr-2015.parquet"), ("fr", "fr-2017.parquet"), ("ec_fr", "fr-2018.parquet"), ("fr", "fr-2019.parquet")], f"described: {described}")
    check(tiled == [("fr-2019.parquet", "fr")], f"tiles: {tiled}")
    check((staging / "converter.json").is_file() and (staging / "converters" / "ec_fr.json").is_file(), "converter metadata")

    # -- catalogize
    (tmp / "catalog" / "fr").mkdir(parents=True)
    (tmp / "catalog" / "fr" / "thumbnail.jpg").write_bytes(b"\xff\xd8\xff\xd9")
    catalogize.survey_text = lambda dataset_id: (None, None)
    catalogize.catalogize("fr", manifest)
    catalogize.build_root(manifest, publish_config()["public_base"].rstrip("/"), manifest.catalog["human_base"].rstrip("/"))

    cdir = tmp / "catalog" / "fr"
    coll = json.loads((cdir / "collection.json").read_text())
    items = {p.name: json.loads(p.read_text()) for p in cdir.glob("year=*/*.json")}
    check(sorted(items) == ["fr-2015.json", "fr-2017.json", "fr-2018.json", "fr-2019.json"], f"items: {sorted(items)}")

    ec, own = items.get("fr-2015.json", {}), items.get("fr-2017.json", {})
    props = ec.get("properties", {})
    check(ec.get("collection") == "fr" and props.get("year") == 2015, "backfilled item collection/year")
    check(props.get("license") == "CC-BY-4.0", "backfilled item license")
    check(any(link["rel"] == "license" and link["href"] == "https://spdx.org/licenses/CC-BY-4.0.html" for link in ec.get("links", [])), "backfilled item license link")
    check(props.get("attribution") == "European Commission, JRC", "backfilled item attribution")
    check([p["name"] for p in props.get("providers", [])] == ["JRC"], "backfilled item providers")
    check({"rel": "via", "href": "https://example.org/jrc", "type": "text/html", "title": "Original source (publisher page)"} in ec.get("links", []), "backfilled item via")
    check(any(link["rel"] == "related" and link["href"].endswith("/ec_fr.py") for link in ec.get("links", [])), "backfilled item converter link")
    check("EC note." in props.get("description", "") and "`ec_fr`" in props.get("description", ""), "backfilled item description")
    check(props.get("title") == "France — 2015", f"backfilled item title: {props.get('title')}")
    check("license" not in own.get("properties", {}) and "providers" not in own.get("properties", {}), "the dataset's own items take the collection's terms")

    check(coll["license"] == "other" and any(link["rel"] == "license" and link["href"] == TERMS for link in coll["links"]), "collection license is the dataset's own")
    names = [p["name"] for p in coll["providers"]]
    check(names == ["IGN", "JRC", real.host["name"]], f"collection providers: {names}")
    check("The 2015 and 2018 editions, which the source above does not offer, come from Field boundaries for France - EuroCrops (JRC, converter `ec_fr`), under CC-BY-4.0" in coll["description"], "collection description does not name the backfill")
    check(coll["assets"]["data"]["href"] == "./latest/fr.parquet" and "(2019)" in coll["assets"]["data"]["title"], "data asset is not the newest year")
    check((staging / "year=2019" / "fr-2019.pmtiles").is_file() and not list(staging.glob("year=201[578]/*.pmtiles")), "only the newest year has tiles")
    latest = cdir / "latest" / "fr.parquet"
    check(latest.resolve().read_bytes() == (staging / "year=2019" / "fr-2019.parquet").read_bytes(), "latest/fr.parquet is not 2019")

    readme, agents = (cdir / "README.md").read_text(), (cdir / "AGENTS.md").read_text()
    check("converter `ec_fr`" in readme and "https://example.org/ec_fr.zip" in readme, "README does not name the backfill and its source")
    check("Not every edition comes from the same source." in agents, "AGENTS.md does not warn about the backfill")

    keys = sorted(u.key for u in upload_data.collect("fr", "p"))
    check(keys == [
        "p/fr/latest/fr.parquet",
        "p/fr/year=2015/fr-2015.parquet", "p/fr/year=2017/fr-2017.parquet",
        "p/fr/year=2018/fr-2018.parquet", "p/fr/year=2019/fr-2019.parquet", "p/fr/year=2019/fr-2019.pmtiles",
    ], f"upload keys: {keys}")

    if shutil.which("rashid"):
        result = subprocess.run(["rashid", "check", str(tmp / "catalog"), "--no-data", "--json"], capture_output=True, text=True)
        for f in json.loads(result.stdout).get("findings", []):
            if f.get("severity") == "error":
                errors.append(f"rashid {f.get('rule_id')} {f.get('path')}: {f.get('message')}")
    else:
        print("note: rashid not installed; conformance of the backfill output not checked")
finally:
    if not os.environ.get("KEEP_TMP"):
        shutil.rmtree(tmp, ignore_errors=True)
    else:
        print(f"kept {tmp}")

if errors:
    print("\n".join(f"error  {e}" for e in errors))
    raise SystemExit(1)
print("OK: backfilled editions are converted by their own converter and carry their own terms")
