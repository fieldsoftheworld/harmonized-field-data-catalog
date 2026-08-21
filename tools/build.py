#!/usr/bin/env python3
"""Build one or more datasets end to end.

For every dataset (and every year in ``datasets.yaml``):

1. ``fiboa publish <id> --variant <year>`` into ``staging/<id>/year=<year>/``
   — convert, validate, PMTiles, STAC; all conversion logic is fiboa-cli's.
2. ``converter_meta.py`` dumps the converter's declared metadata.
3. ``catalogize.py`` writes ``catalog/<id>/`` and regenerates the root.
4. ``thumbnail.py`` renders the thumbnail when a chiitiler server is running
   (skipped with a warning otherwise), then catalogize registers it.
5. optionally ``upload_data.py`` sends the data files to the bucket.

    python tools/build.py nl                 # steps 1-3
    python tools/build.py nl --upload        # and upload the data
    python tools/build.py --all              # every dataset in the manifest
    python tools/build.py nl --year 2024     # one edition only

fiboa-cli is found through $FIBOA_CMD (default ``fiboa``) and the interpreter
that has it installed through $FIBOA_PYTHON (default ``python``). Set both to
e.g. ``pixi run -e dev --manifest-path ../cli/pyproject.toml fiboa`` to use a
checkout of fiboa-cli. Steps are idempotent: existing staging files are reused,
delete them to reconvert.
"""
from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys

from common import ROOT, STAGING_DIR, Manifest, staging_year_dir

FIBOA_CMD = shlex.split(os.environ.get("FIBOA_CMD", "fiboa"))
FIBOA_PYTHON = shlex.split(os.environ.get("FIBOA_PYTHON", "python"))
CACHE_DIR = ROOT / "cache"


def run(cmd: list[str], **kwargs) -> None:
    print("$ " + " ".join(shlex.quote(c) for c in cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=ROOT, **kwargs)


def publish(dataset_id: str, year: str, has_variants: bool) -> None:
    out = staging_year_dir(dataset_id, year)
    out.mkdir(parents=True, exist_ok=True)
    cmd = [*FIBOA_CMD, "publish", dataset_id, "-c", str(CACHE_DIR), "-o", str(out)]
    if has_variants:
        cmd += ["--variant", year]
    run(cmd)


def converter_meta(dataset_id: str) -> None:
    out = STAGING_DIR / dataset_id / "converter.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        run([*FIBOA_PYTHON, str(ROOT / "tools" / "converter_meta.py"), dataset_id], stdout=f)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("datasets", nargs="*", help="dataset ids from datasets.yaml")
    parser.add_argument("--all", action="store_true", help="build every dataset in the manifest")
    parser.add_argument("--year", help="build only this edition")
    parser.add_argument("--skip-convert", action="store_true", help="skip fiboa publish (staging must exist)")
    parser.add_argument("--skip-thumbnail", action="store_true", help="do not render a thumbnail")
    parser.add_argument("--upload", action="store_true", help="upload the data files afterwards (dry run without --confirm)")
    parser.add_argument("--confirm", action="store_true", help="with --upload: actually upload")
    args = parser.parse_args()

    manifest = Manifest.load()
    ids = list(manifest.datasets) if args.all else args.datasets
    if not ids:
        parser.error("name a dataset or pass --all")

    failures = []
    for dataset_id in ids:
        ds = manifest.datasets.get(dataset_id)
        if ds is None:
            sys.exit(f"{dataset_id} is not in datasets.yaml")
        years = [args.year] if args.year else ds.years
        # the manifest knows whether the year is a converter variant or only a label
        has_variants = "years" in (__import__("yaml").safe_load(open(ROOT / "datasets.yaml"))["datasets"][dataset_id] or {})
        try:
            if not args.skip_convert:
                for year in years:
                    publish(dataset_id, year, has_variants)
            converter_meta(dataset_id)
            run([sys.executable, str(ROOT / "tools" / "catalogize.py"), dataset_id])
            if not args.skip_thumbnail:
                try:
                    cmd = [sys.executable, str(ROOT / "tools" / "thumbnail.py"), dataset_id]
                    if "zoom" in ds.thumbnail:
                        cmd += ["--zoom", str(ds.thumbnail["zoom"])]
                    if "center" in ds.thumbnail:
                        cmd += ["--center", ",".join(str(v) for v in ds.thumbnail["center"])]
                    if "rank" in ds.thumbnail:
                        cmd += ["--rank", str(ds.thumbnail["rank"])]
                    run(cmd)
                    run([sys.executable, str(ROOT / "tools" / "catalogize.py"), dataset_id])
                except subprocess.CalledProcessError:
                    print(f"warning: thumbnail for {dataset_id} not rendered (is chiitiler running?)", file=sys.stderr)
            if args.upload:
                cmd = [sys.executable, str(ROOT / "tools" / "upload_data.py"), dataset_id]
                if args.confirm:
                    cmd.append("--confirm")
                run(cmd)
        except subprocess.CalledProcessError as exc:
            print(f"FAILED {dataset_id}: {exc}", file=sys.stderr)
            failures.append(dataset_id)
            continue

    if failures:
        print("\nfailed: " + ", ".join(failures), file=sys.stderr)
        return 1
    print("\nall done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
