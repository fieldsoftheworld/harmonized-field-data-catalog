#!/usr/bin/env python3
"""The manifest and the published tree agree.

datasets.yaml is the list of what this catalog publishes; catalog/ is what is
published. A collection in one but not the other is a mistake either way:
metadata that was never built, or a collection nobody intends to maintain.

Also checks the manifest's own rules (years/year or parts, never both), and
what catalogize.py promises: one item per edition (per part edition), hive
partition directories, a partition glob under the public base, and a host
provider last. Dependency-free apart from PyYAML (CI installs it).

Run: python3 tests/test_manifest.py
"""
import json
import re
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from common import Manifest  # noqa: E402
from publish import load_config  # noqa: E402

config = load_config()
CATALOG = ROOT / config["publish_dir"]
manifest = yaml.safe_load((ROOT / "datasets.yaml").read_text())
errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def rejects(yaml_text: str) -> str | None:
    """The loader's exit message for a manifest, or None if it loads."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "datasets.yaml"
        path.write_text(HEADER + yaml_text)
        try:
            Manifest.load(path)
        except SystemExit as exc:
            return str(exc)
    return None


# the loader enforces the manifest's shape; these are the rules datasets.yaml documents
HEADER = "catalog: {}\nhost: {}\ndatasets:\n"
PARTS = """\
  ch:
    title: Field boundaries for Switzerland
    boundaries: declared
    parts:
      ch_ag:
      ch_zh: {years: ['2024', '2025'], notes: n}
"""
if rejects(PARTS) is not None:
    err(f"a parts dataset is rejected: {rejects(PARTS)}")
if rejects(PARTS.replace("    parts:", "    years: ['2025']\n    parts:")) is None:
    err("a dataset with both years and parts loads")
if rejects(PARTS.replace("    parts:", "    year: 2025\n    parts:")) is None:
    err("a dataset with both year and parts loads")
if rejects(PARTS.replace("    title: Field boundaries for Switzerland\n", "")) is None:
    err("a parts dataset without a title loads")
if rejects(PARTS.replace("['2024', '2025']", "['2025', '2024']")) is None:
    err("a part with descending years loads")
if rejects(PARTS.replace("notes: n", "variant: x")) is None:
    err("a part with an unknown key loads")
if rejects("  nl:\n    years: ['2025']\n    boundaries: declared\n    title: T\n") is None:
    err("a title on a dataset without parts loads")
if rejects("  nl:\n    boundaries: declared\n") is None:
    err("a dataset without years, year or parts loads")
with tempfile.TemporaryDirectory() as tmp:
    (Path(tmp) / "datasets.yaml").write_text(HEADER + PARTS)
    ch = Manifest.load(Path(tmp) / "datasets.yaml").datasets["ch"]
if not (ch.is_parts and ch.years == [] and list(ch.parts) == ["ch_ag", "ch_zh"]):
    err(f"parts are not kept in manifest order: {list(ch.parts)}")
if ch.parts["ch_ag"].years or ch.parts["ch_zh"].years != ["2024", "2025"] or ch.parts["ch_zh"].notes != "n":
    err(f"part years/notes not loaded: {ch.parts}")
Manifest.load()  # the real manifest passes the same rules


declared = set(manifest.get("datasets") or {})
built = {p.parent.name for p in CATALOG.glob("*/collection.json")}
for missing in sorted(declared - built):
    print(f"note: {missing} is in datasets.yaml but not built yet (run tools/build.py {missing})")
for extra in sorted(built - declared):
    err(f"catalog/{extra}/ is published but not in datasets.yaml")

root = json.loads((CATALOG / "catalog.json").read_text())
children = {Path(link["href"]).parent.name for link in root["links"] if link["rel"] == "child"}
if children != built:
    err(f"catalog.json children {sorted(children)} != built collections {sorted(built)}")

def expected_items(dataset_id: str, spec: dict) -> set[str]:
    """Item paths relative to the collection: one per edition, or per part edition.

    A part without years has its year from the data, so whatever it has in the
    catalog counts, as long as it has at least one.
    """
    if "parts" not in spec:
        years = [str(y) for y in (spec.get("years") or [spec.get("year")])]
        return {f"year={y}/{dataset_id}-{y}.json" for y in years}
    out = set()
    for part_id, part in spec["parts"].items():
        years = [str(y) for y in (part or {}).get("years") or []]
        if years:
            out |= {f"year={y}/{part_id}-{y}.json" for y in years}
            continue
        found = {
            p.relative_to(CATALOG / dataset_id).as_posix()
            for p in (CATALOG / dataset_id).glob(f"year=*/{part_id}-*.json")
            if re.fullmatch(rf"{re.escape(part_id)}-\d{{4}}\.json", p.name)
        }
        out |= found or {f"year=<Y>/{part_id}-<Y>.json"}
    return out


for dataset_id in sorted(built & declared):
    spec = manifest["datasets"][dataset_id] or {}
    expected = expected_items(dataset_id, spec)
    coll = json.loads((CATALOG / dataset_id / "collection.json").read_text())
    linked = {link["href"].removeprefix("./") for link in coll["links"] if link["rel"] == "item"}
    for path in sorted(expected - linked):
        err(f"{dataset_id}: no item link to {path}")
    for path in sorted(linked - expected):
        err(f"{dataset_id}: item link to {path}, which the manifest does not publish")
    for path in sorted(expected):
        if not (CATALOG / dataset_id / path).is_file():
            err(f"{dataset_id}: missing item catalog/{dataset_id}/{path}")
    glob = coll.get("partition:glob", "")
    if not glob.startswith(config["write_prefix"].rstrip("/") + f"/{dataset_id}/year=*/"):
        err(f"{dataset_id}: partition:glob {glob!r} is not the S3 form of the published prefix")
    providers = coll.get("providers") or []
    if not providers or "host" not in providers[-1].get("roles", []):
        err(f"{dataset_id}: last provider is not the host")
    if providers and providers[-1].get("name") != manifest["host"]["name"]:
        err(f"{dataset_id}: host is {providers[-1].get('name')!r}, manifest says {manifest['host']['name']!r}")
    for required in ("README.md", "AGENTS.md", "llms.txt"):
        if not (CATALOG / dataset_id / required).is_file():
            err(f"{dataset_id}: missing {required}")
    # the manifest's provenance has to reach the published collection, or a reader
    # filtering on how a boundary was made is back to guessing
    boundaries = (manifest["datasets"][dataset_id] or {}).get("boundaries")
    if boundaries not in ("declared", "mapped", "inferred"):
        err(f"{dataset_id}: boundaries is {boundaries!r}, expected declared, mapped or inferred")
    elif coll.get("boundaries") != boundaries:
        err(f"{dataset_id}: collection says boundaries {coll.get('boundaries')!r}, manifest says {boundaries!r}")

    holds = (manifest["datasets"][dataset_id] or {}).get("holds", "fields")
    if holds not in ("fields", "blocks"):
        err(f"{dataset_id}: holds is {holds!r}, expected 'fields' or 'blocks'")
    # a block collection says so where a reader sees it, not only in the manifest
    if holds == "blocks":
        if "field blocks" not in (coll.get("keywords") or []):
            err(f"{dataset_id}: holds blocks but the keyword 'field blocks' is missing")
        if not coll.get("title", "").lower().startswith("field blocks"):
            err(f"{dataset_id}: holds blocks but the title reads {coll.get('title')!r}")
    elif "field blocks" in (coll.get("keywords") or []):
        err(f"{dataset_id}: keyword 'field blocks' on a collection that holds {holds}")

if errors:
    print("\n".join(f"error  {e}" for e in errors))
    raise SystemExit(1)
print(f"OK: manifest and catalog agree on {len(built)} collection(s)")
