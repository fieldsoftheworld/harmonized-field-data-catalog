#!/usr/bin/env python3
"""Build one or more datasets end to end.

For every dataset (and every year in ``datasets.yaml``):

1. ``stage()`` fills ``staging/<id>/year=<year>/``: ``fiboa convert`` and
   ``fiboa validate`` (all conversion logic is fiboa-cli's), PMTiles with
   ogr2ogr and tippecanoe, and the ``collection.json`` catalogize reads.
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

A collection with ``parts`` (``ch``) stages each part with its own converter as
``year=<Y>/<part>-<Y>.parquet`` beside ``<part>-<Y>.collection.json``, keeps
each part's converter metadata in ``converters/<part>.json``, and tiles the
newest edition of every part into one ``latest/<id>.pmtiles``. A part without
years is converted once into ``tmp/`` and filed under the most frequent year of
its ``determination:datetime``. The row-count check runs per part.

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
from pathlib import Path

from common import (
    FILE_EXTENSION,
    PMTILES_TYPE,
    ROOT,
    STAGING_DIR,
    WEB_MAP_LINKS_EXTENSION,
    Dataset,
    Manifest,
    determination_years,
    file_facts,
    file_stem,
    parquet_row_count,
    read_json,
    staged_part_years,
    staging_converter_meta,
    staging_part_stac,
    staging_year_dir,
    write_json,
)

FIBOA_CMD = shlex.split(os.environ.get("FIBOA_CMD", "fiboa"))
FIBOA_PYTHON = shlex.split(os.environ.get("FIBOA_PYTHON", "python"))
CACHE_DIR = ROOT / "cache"


def run(cmd: list[str], **kwargs) -> None:
    print("$ " + " ".join(shlex.quote(c) for c in cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=ROOT, **kwargs)


TIPPECANOE_OPTS = ["-zg", "--drop-densest-as-needed", "--extend-zooms-if-still-dropping"]


def convert(converter_id: str, parquet: Path, variant: str | None = None) -> None:
    parquet.parent.mkdir(parents=True, exist_ok=True)
    cmd = [*FIBOA_CMD, "convert", converter_id, "-c", str(CACHE_DIR), "-o", str(parquet)]
    if variant:
        cmd += ["--variant", variant]
    run(cmd)


def stage(dataset_id: str, year: str, has_variants: bool, latest: bool = True) -> None:
    out = staging_year_dir(dataset_id, year)
    out.mkdir(parents=True, exist_ok=True)
    # an edition that is only a label, not a converter variant, is published as <id>
    stem = file_stem(dataset_id, year) if has_variants else dataset_id
    parquet, pmtiles = out / f"{stem}.parquet", out / f"{stem}.pmtiles"

    if not parquet.exists():
        convert(dataset_id, parquet, year if has_variants else None)
    run([*FIBOA_CMD, "validate", "-n", "-1", str(parquet)])

    # only the newest edition is rendered in the browser; tiles for older
    # editions would double the storage without ever being seen
    if latest and not pmtiles.exists():
        make_pmtiles(parquet, pmtiles, dataset_id)
    describe(dataset_id, parquet, pmtiles if pmtiles.exists() else None, out / "collection.json")


def stage_part(dataset_id: str, part_id: str, year: str) -> None:
    """One edition of a part: a converter variant, staged as <part>-<year>."""
    parquet = staging_year_dir(dataset_id, year) / f"{file_stem(part_id, year)}.parquet"
    if not parquet.exists():
        convert(part_id, parquet, year)
    run([*FIBOA_CMD, "validate", "-n", "-1", str(parquet)])
    describe(part_id, parquet, None, staging_part_stac(dataset_id, part_id, year))


def stage_part_snapshot(dataset_id: str, part_id: str) -> None:
    """A part without variants: convert once, and file it under the year the data holds.

    The source is the part's current state, so its year is read from the file:
    the most frequent year of ``determination:datetime``. catalogize notes a
    file that holds other years too. A staged edition is reused; delete it to
    take a new snapshot.
    """
    years = staged_part_years(dataset_id, part_id)
    if not years:
        parquet = STAGING_DIR / dataset_id / "tmp" / f"{part_id}.parquet"
        if not parquet.exists():
            convert(part_id, parquet)
        counts = determination_years(parquet)
        if not counts:
            raise SystemExit(f"{part_id}: no determination:datetime in {parquet}, so no year to file it under")
        year = counts[0][0]
        target = staging_year_dir(dataset_id, year) / f"{file_stem(part_id, year)}.parquet"
        target.parent.mkdir(parents=True, exist_ok=True)
        print(f"{part_id}: {', '.join(f'{y}: {n:,}' for y, n in counts)} rows by year; filed under {year}", flush=True)
        os.replace(parquet, target)
        years = [year]
    for year in years:
        stage_part(dataset_id, part_id, year)


def stage_parts(ds: Dataset, only_year: str | None) -> None:
    for part in ds.parts.values():
        if part.years:
            for year in part.years:
                if only_year in (None, year):
                    stage_part(ds.id, part.id, year)
        elif only_year is None:
            stage_part_snapshot(ds.id, part.id)
        else:
            print(f"{part.id}: no years in the manifest, skipped with --year", flush=True)


def stage_parts_pmtiles(ds: Dataset) -> None:
    """One PMTiles for the collection, from the newest edition of every part.

    The editions are tiled as one layer named after the collection; the tiles'
    attribution names every part, since the map shows them together. Older
    editions get no tiles, as for any other collection.
    """
    latest = ds.latest_per_part()
    sources = [staging_year_dir(ds.id, y) / f"{file_stem(p, y)}.parquet" for p, y in latest.items()]
    pmtiles = STAGING_DIR / ds.id / "latest" / f"{ds.id}.pmtiles"
    if pmtiles.exists() and pmtiles.stat().st_mtime >= max(s.stat().st_mtime for s in sources):
        return
    attributions = []
    for part_id in latest:
        meta = read_json(staging_converter_meta(ds.id, part_id))
        attributions.append(meta.get("attribution") or meta.get("provider") or part_id)
    make_pmtiles(sources, pmtiles, ds.id, attribution="; ".join(attributions))


def make_pmtiles(sources: Path | list[Path], pmtiles: Path, layer: str, attribution: str | None = None) -> None:
    """Tile one or more GeoParquet files into one layer (ogr2ogr, one after another, into tippecanoe)."""
    sources = [sources] if isinstance(sources, Path) else sources
    pmtiles.parent.mkdir(parents=True, exist_ok=True)
    # tippecanoe ignores $TMPDIR and spills into /tmp, which is often a small partition
    tmp = ["-t", os.environ["TMPDIR"]] if os.environ.get("TMPDIR") else []
    extra = ["--attribution", attribution] if attribution else []
    tippecanoe = ["tippecanoe", *tmp, *TIPPECANOE_OPTS, "--projection=EPSG:4326", *extra, "-o", str(pmtiles), "-l", layer]
    print(f"$ {shlex.join(tippecanoe)}", flush=True)
    tiles = subprocess.Popen(tippecanoe, stdin=subprocess.PIPE)
    failed = 0
    for parquet in sources:
        ogr = ["ogr2ogr", "-t_srs", "EPSG:4326", "-f", "GeoJSONSeq", "/vsistdout/", str(parquet)]
        print(f"  <- {shlex.join(ogr)}", flush=True)
        failed = failed or subprocess.run(ogr, stdout=tiles.stdin).returncode
    tiles.stdin.close()
    if tiles.wait() != 0 or failed:
        pmtiles.unlink(missing_ok=True)
        raise subprocess.CalledProcessError(tiles.returncode or failed, tippecanoe)


def describe(dataset_id: str, parquet: Path, pmtiles: Path | None, stac_file: Path) -> None:
    """The collection.json catalogize reads: fiboa's STAC with relative hrefs, sizes and checksums."""
    newest = max(p.stat().st_mtime for p in (parquet, pmtiles) if p is not None)
    if stac_file.exists() and stac_file.stat().st_mtime >= newest:
        return
    run([*FIBOA_CMD, "create-stac-collection", str(parquet), "-o", str(stac_file)])
    data = read_json(stac_file)
    if data["id"] != dataset_id:
        stac_file.unlink()
        raise SystemExit(f"{parquet}: collection id {data['id']!r}, expected {dataset_id!r}")

    extensions = data.setdefault("stac_extensions", [])
    extensions += [e for e in (FILE_EXTENSION, WEB_MAP_LINKS_EXTENSION if pmtiles else None) if e and e not in extensions]
    title = data.get("title") or dataset_id
    asset = data["assets"]["data"]
    asset.update({"href": f"./{parquet.name}", "title": f"{title} (GeoParquet)", **file_facts(parquet)})
    data["links"] = [link for link in data.get("links", []) if link.get("rel") != "pmtiles"]
    if pmtiles:
        href = f"./{pmtiles.name}"
        data["links"].append({"rel": "pmtiles", "href": href, "type": PMTILES_TYPE, "title": "Web map tiles", "pmtiles:layers": [dataset_id]})
        data["assets"]["visual"] = {"href": href, "type": PMTILES_TYPE, "title": f"{title} (PMTiles)", "roles": ["visual"], **file_facts(pmtiles)}
    write_json(stac_file, data)


# an edition this far from its neighbour is reported; see check_row_counts
DEFAULT_ROW_COUNT_TOLERANCE = 0.25


def check_row_counts(dataset_id: str, years: list[str], tolerance: float, part_id: str | None = None) -> list[str]:
    """Report editions whose row count jumps against the preceding one.

    A conversion that quietly changes what it keeps still writes a valid file,
    so no other step notices: es_ga 2022 came out 75% larger than 2023 because
    Galicia had coded scrub as PR before it introduced MT, and that only showed
    up by comparing finished editions. Comparing neighbours catches it in
    seconds instead of after a whole backfill.

    This warns rather than fails, because genuine changes of the same size do
    happen (nl 2023 nearly doubled on a real BRP delineation change). A dataset
    that legitimately jumps sets row_count_tolerance in datasets.yaml.
    In a parts collection each part is its own series.
    """
    label = f"{dataset_id}/{part_id}" if part_id else dataset_id
    counts: list[tuple[str, int]] = []
    for year in years:
        parquet = staging_year_dir(dataset_id, year) / f"{file_stem(part_id or dataset_id, year)}.parquet"
        if parquet.exists():
            counts.append((year, parquet_row_count(parquet)))

    warnings = []
    for (prev_year, prev_rows), (year, rows) in zip(counts, counts[1:]):
        if prev_rows == 0:
            continue
        change = (rows - prev_rows) / prev_rows
        if abs(change) > tolerance:
            warnings.append(
                f"{label} {year}: {rows:,} rows vs {prev_rows:,} in {prev_year} "
                f"({change:+.0%}, tolerance +/-{tolerance:.0%})"
            )
    return warnings


def converter_meta(converter_id: str, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        run([*FIBOA_PYTHON, str(ROOT / "tools" / "converter_meta.py"), converter_id], stdout=f)


def row_count_tolerance(ds: Dataset) -> float:
    return ds.row_count_tolerance if ds.row_count_tolerance is not None else DEFAULT_ROW_COUNT_TOLERANCE


def prepare(ds: Dataset, only_year: str | None, skip_convert: bool) -> list[str]:
    """Staging, row-count check and converter metadata; returns the row-count warnings."""
    if ds.is_parts:
        if not skip_convert:
            stage_parts(ds, only_year)
        for part_id in ds.parts:
            converter_meta(part_id, staging_converter_meta(ds.id, part_id))
        if not skip_convert:
            stage_parts_pmtiles(ds)
        editions = ds.editions()
        return [
            jump
            for part_id in ds.parts
            for jump in check_row_counts(
                ds.id, [y for p, y in editions if p == part_id], row_count_tolerance(ds), part_id
            )
        ]
    if not skip_convert:
        for year in [only_year] if only_year else ds.years:
            stage(ds.id, year, ds.has_variants, latest=(year == ds.years[-1]))
    # compare against the whole series, not just the years built now: a
    # single rebuilt edition is only suspicious next to its neighbours
    jumps = check_row_counts(ds.id, ds.years, row_count_tolerance(ds))
    converter_meta(ds.id, staging_converter_meta(ds.id))
    return jumps


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("datasets", nargs="*", help="dataset ids from datasets.yaml")
    parser.add_argument("--all", action="store_true", help="build every dataset in the manifest")
    parser.add_argument("--year", help="build only this edition")
    parser.add_argument("--skip-convert", action="store_true", help="skip the staging step (staging must exist)")
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
        try:
            jumps = prepare(ds, args.year, args.skip_convert)
            for msg in jumps:
                print(f"row-count jump: {msg}", file=sys.stderr)
            row_count_warnings += jumps
            if jumps and args.strict_row_counts:
                raise SystemExit(f"{dataset_id}: row-count jump with --strict-row-counts")
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
