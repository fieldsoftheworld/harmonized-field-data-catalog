#!/usr/bin/env python3
"""A ``split_by_year`` dataset is converted once and filed by the year its fields represent.

Checks build.write_year_split() on a tiny file (no fiboa-cli):

- each edition holds exactly the rows whose determination:datetime is in its year;
- the fiboa collection metadata, compression and row groups are kept, and the geo
  bbox is the year's own extent;
- data whose years differ from datasets.yaml's list fails instead of losing rows;

and that the manifest accepts split_by_year only with `years`, as no converter variants.

Needs duckdb with the spatial extension, so it SKIPs where that is missing.

Run: python tests/test_split_years.py
"""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

if not all(importlib.util.find_spec(m) for m in ("duckdb", "pyarrow", "yaml")):
    print("SKIP: duckdb/pyarrow/yaml not installed; run in the pixi environment")
    raise SystemExit(0)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fixtures import write_parquet  # noqa: E402

import pyarrow as pa  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

import build  # noqa: E402
from common import Manifest  # noqa: E402

errors: list[str] = []


def check(ok: bool, what: str) -> None:
    if not ok:
        errors.append(what)


def years_in(path: Path) -> list[int]:
    return sorted(d.year for d in pq.read_table(path)["determination:datetime"].to_pylist())


with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    full = write_parquet(tmp / "full.parquet", 10.0, [2017, 2019, 2017, 2018, 2019, 2019])
    # as the converter writes it: UTC timestamps, fiboa collection metadata, zstd, small row groups
    table = pq.read_table(full)
    i = table.schema.get_field_index("determination:datetime")
    table = table.set_column(i, "determination:datetime", table.column(i).cast(pa.timestamp("ms", tz="UTC")))
    geo = json.loads(table.schema.metadata[b"geo"]) if b"geo" in (table.schema.metadata or {}) else {
        "version": "1.1.0", "primary_column": "geometry", "columns": {"geometry": {"encoding": "WKB"}}}
    geo["columns"][geo["primary_column"]]["bbox"] = [-180.0, -90.0, 180.0, 90.0]
    meta = {**(table.schema.metadata or {}), b"collection": json.dumps({"collection": "x"}).encode(),
            b"geo": json.dumps(geo).encode()}
    pq.write_table(table.replace_schema_metadata(meta), full, compression="zstd", row_group_size=2)

    years = ["2017", "2018", "2019"]
    for year in years:
        out = tmp / f"year={year}" / f"x-{year}.parquet"
        build.write_year_split(full, year, years, out)
        got = years_in(out)
        check(set(got) == {int(year)}, f"{year}: only that year's rows, got {got}")
        got_meta, src_meta = pq.read_schema(out).metadata, pq.read_schema(full).metadata
        check(got_meta[b"collection"] == src_meta[b"collection"], f"{year}: fiboa collection metadata kept")
        part = pq.read_table(out)
        want = [min(b["xmin"] for b in part["bbox"].to_pylist()), min(b["ymin"] for b in part["bbox"].to_pylist()),
                max(b["xmax"] for b in part["bbox"].to_pylist()), max(b["ymax"] for b in part["bbox"].to_pylist())]
        bbox = json.loads(got_meta[b"geo"])["columns"]["geometry"]["bbox"]
        check(bbox == want, f"{year}: geo bbox is this year's extent {want}, got {bbox}")
        md = pq.ParquetFile(out).metadata
        check(md.row_group(0).column(0).compression == "ZSTD", f"{year}: compression kept")
        check(md.row_group(0).num_rows <= 2, f"{year}: row group size kept")
    counts = [pq.read_metadata(tmp / f"year={y}" / f"x-{y}.parquet").num_rows for y in years]
    check(counts == [2, 1, 3], f"rows per year 2, 1, 3, got {counts}")

    for listed in (["2017", "2018"], ["2016", "2017", "2018", "2019"]):
        try:
            build.write_year_split(full, "2017", listed, tmp / "bad.parquet")
            errors.append(f"years {listed} that differ from the data must fail")
        except SystemExit:
            pass

    base = "catalog: {id: c}\nhost: {name: h}\ndatasets:\n  x:\n    boundaries: mapped\n"
    manifest = tmp / "datasets.yaml"
    manifest.write_text(base + "    years: [2017, 2018]\n    split_by_year: true\n")
    ds = Manifest.load(manifest).datasets["x"]
    check(ds.split_by_year and not ds.has_variants, "split_by_year years are not converter variants")
    for bad in ("    year: 2017\n    split_by_year: true\n", "    split_by_year: true\n"):
        manifest.write_text(base + bad)
        try:
            Manifest.load(manifest)
            errors.append(f"split_by_year without 'years' must fail: {bad.strip()!r}")
        except SystemExit:
            pass

for e in errors:
    print(f"error  {e}")
if errors:
    raise SystemExit(1)
print("OK: a split_by_year dataset is filed by the year its fields represent")
