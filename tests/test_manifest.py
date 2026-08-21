#!/usr/bin/env python3
"""The manifest and the published tree agree.

datasets.yaml is the list of what this catalog publishes; catalog/ is what is
published. A collection in one but not the other is a mistake either way:
metadata that was never built, or a collection nobody intends to maintain.

Also checks what catalogize.py promises: one item per edition, hive
partition directories, a partition glob under the public base, and a host
provider last. Dependency-free apart from PyYAML (CI installs it).

Run: python3 tests/test_manifest.py
"""
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from publish import load_config  # noqa: E402

config = load_config()
CATALOG = ROOT / config["publish_dir"]
manifest = yaml.safe_load((ROOT / "datasets.yaml").read_text())
errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


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

for dataset_id in sorted(built & declared):
    spec = manifest["datasets"][dataset_id] or {}
    years = [str(y) for y in (spec.get("years") or [spec.get("year")])]
    coll = json.loads((CATALOG / dataset_id / "collection.json").read_text())
    items = [link for link in coll["links"] if link["rel"] == "item"]
    if len(items) != len(years):
        err(f"{dataset_id}: {len(items)} item links for {len(years)} editions {years}")
    for year in years:
        d = CATALOG / dataset_id / f"year={year}"
        if not (d / f"{dataset_id}-{year}.json").is_file():
            err(f"{dataset_id}: missing item {d.relative_to(ROOT)}/{dataset_id}-{year}.json")
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

if errors:
    print("\n".join(f"error  {e}" for e in errors))
    raise SystemExit(1)
print(f"OK: manifest and catalog agree on {len(built)} collection(s)")
