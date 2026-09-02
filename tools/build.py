#!/usr/bin/env python3
"""Build one or more datasets end to end.

For every dataset (and every year in ``datasets.yaml``):

1. ``fiboa publish <id> --variant <year>`` into ``staging/<id>/year=<year>/``
   — convert, validate, PMTiles, STAC; all conversion logic is fiboa-cli's.
2. a row-count check against the neighbouring editions, which warns when a
   conversion quietly changed what it keeps (``--strict-row-counts`` to fail).
3. ``converter_meta.py`` dumps the converter's declared metadata.
4. ``catalogize.py`` writes ``catalog/<id>/`` and regenerates the root.
5. ``thumbnail.py`` renders the thumbnail when a chiitiler server is running
   (skipped with a warning otherwise), then catalogize registers it.
6. optionally ``upload_data.py`` sends the data files to the bucket.

    python tools/build.py nl                 # steps 1-4
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

from common import (
    ROOT,
    STAGING_DIR,
    Manifest,
    file_stem,
    parquet_row_count,
    staging_year_dir,
)

FIBOA_CMD = shlex.split(os.environ.get("FIBOA_CMD", "fiboa"))
FIBOA_PYTHON = shlex.split(os.environ.get("FIBOA_PYTHON", "python"))
CACHE_DIR = ROOT / "cache"


def run(cmd: list[str], **kwargs) -> None:
    print("$ " + " ".join(shlex.quote(c) for c in cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=ROOT, **kwargs)


def publish(dataset_id: str, year: str, has_variants: bool, latest: bool = True) -> None:
    out = staging_year_dir(dataset_id, year)
    out.mkdir(parents=True, exist_ok=True)
    cmd = [*FIBOA_CMD, "publish", dataset_id, "-c", str(CACHE_DIR), "-o", str(out)]
    if not latest:
        # only the newest edition is rendered in the browser; tiles for older
        # editions would double the storage without ever being seen
        cmd += ["--no-pmtiles"]
    if has_variants:
        cmd += ["--variant", year]
    run(cmd)


# an edition this far from its neighbour is reported; see check_row_counts
DEFAULT_ROW_COUNT_TOLERANCE = 0.25


def check_row_counts(dataset_id: str, years: list[str], tolerance: float) -> list[str]:
    """Report editions whose row count jumps against the preceding one.

    A conversion that quietly changes what it keeps still writes a valid file,
    so no other step notices: es_ga 2022 came out 75% larger than 2023 because
    Galicia had coded scrub as PR before it introduced MT, and that only showed
    up by comparing finished editions. Comparing neighbours catches it in
    seconds instead of after a whole backfill.

    This warns rather than fails, because genuine changes of the same size do
    happen (nl 2023 nearly doubled on a real BRP delineation change). A dataset
    that legitimately jumps sets row_count_tolerance in datasets.yaml.
    """
    counts: list[tuple[str, int]] = []
    for year in years:
        parquet = staging_year_dir(dataset_id, year) / f"{file_stem(dataset_id, year)}.parquet"
        if parquet.exists():
            counts.append((year, parquet_row_count(parquet)))

    warnings = []
    for (prev_year, prev_rows), (year, rows) in zip(counts, counts[1:]):
        if prev_rows == 0:
            continue
        change = (rows - prev_rows) / prev_rows
        if abs(change) > tolerance:
            warnings.append(
                f"{dataset_id} {year}: {rows:,} rows vs {prev_rows:,} in {prev_year} "
                f"({change:+.0%}, tolerance +/-{tolerance:.0%})"
            )
    return warnings


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
    parser.add_argument("--strict-row-counts", action="store_true", help="treat a row-count jump as a failure")
    args = parser.parse_args()

    manifest = Manifest.load()
    ids = list(manifest.datasets) if args.all else args.datasets
    if not ids:
        parser.error("name a dataset or pass --all")

    failures = []
    row_count_warnings = []
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
                    publish(dataset_id, year, has_variants, latest=(year == ds.years[-1]))
            # compare against the whole series, not just the years built now: a
            # single rebuilt edition is only suspicious next to its neighbours
            jumps = check_row_counts(
                dataset_id,
                ds.years,
                ds.row_count_tolerance
                if ds.row_count_tolerance is not None
                else DEFAULT_ROW_COUNT_TOLERANCE,
            )
            for msg in jumps:
                print(f"row-count jump: {msg}", file=sys.stderr)
            row_count_warnings += jumps
            if jumps and args.strict_row_counts:
                raise SystemExit(f"{dataset_id}: row-count jump with --strict-row-counts")
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

    if row_count_warnings:
        print("\nrow-count jumps to check (set row_count_tolerance in datasets.yaml if real):", file=sys.stderr)
        for msg in row_count_warnings:
            print(f"  {msg}", file=sys.stderr)
    if failures:
        print("\nfailed: " + ", ".join(failures), file=sys.stderr)
        return 1
    print("\nall done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
