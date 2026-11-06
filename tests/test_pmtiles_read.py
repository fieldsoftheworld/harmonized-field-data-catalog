#!/usr/bin/env python3
"""The tiles read every feature of a GeoParquet intact, whatever its column order.

GDAL 3.13's Parquet reader garbles the strings of a few features (empty or
invalid UTF-8) for some column orders and values, and fiboa-cli writes
columns in set order, so build.py reads through ogr_geojsonseq(). This writes
100,002 rows in an order that triggers it and checks every feature that argv
streams has its id.

Needs ogr2ogr and pyarrow, so it SKIPs where either is missing.

Run: python tests/test_pmtiles_read.py
"""
import json
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
except ImportError:
    print("SKIP: pyarrow is not installed")
    raise SystemExit(0)
if shutil.which("ogr2ogr") is None:
    print("SKIP: ogr2ogr is not installed")
    raise SystemExit(0)

from build import ogr_geojsonseq  # noqa: E402

ROWS = 100_002


def point_wkb(x: float, y: float) -> bytes:
    import struct

    return struct.pack("<BIdd", 1, 1, x, y)


# Ids like GloCAB's, in the shuffled order a spatial sort leaves them in; short ids in
# sequence do not trigger the corruption.
IDS = [f"Ukraine_H-{i}" for i in random.Random(0).sample(range(ROWS), ROWS)]

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "layer-2020.parquet"
    geo = {"version": "1.1.0", "primary_column": "geometry",
           "columns": {"geometry": {"encoding": "WKB", "geometry_types": ["Point"]}}}
    # The trigger, as fiboa-cli wrote GloCAB: a timestamp first, a string after it, and a
    # non-nullable id (fiboa requires it); without any one of these GDAL reads it intact.
    schema = pa.schema([
        pa.field("determination:datetime", pa.timestamp("ms", tz="UTC")),
        pa.field("crop", pa.string()),
        pa.field("id", pa.string(), nullable=False),
        pa.field("geometry", pa.binary(), nullable=False),
    ], metadata={b"geo": json.dumps(geo).encode()})
    table = pa.table({
        "determination:datetime": [0] * ROWS,
        "crop": ["Maize", "Wheat"] * (ROWS // 2),
        "id": IDS,
        "geometry": [point_wkb(i % 360 - 180, 0.0) for i in range(ROWS)],
    }, schema=schema)
    pq.write_table(table, path, row_group_size=18_432)

    out = subprocess.run(ogr_geojsonseq(path), capture_output=True, check=True).stdout
    ids = []
    for line in out.splitlines():
        try:
            ids.append(json.loads(line.decode("utf-8"))["properties"]["id"])
        except (UnicodeDecodeError, json.JSONDecodeError):
            ids.append(None)
    bad = [i for i, (v, want) in enumerate(zip(ids, IDS), 1) if v != want]
    if len(ids) != ROWS or bad:
        print(f"error  {len(ids)} features of {ROWS}; garbled at {bad[:5]}")
        raise SystemExit(1)
    print(f"ok     ogr_geojsonseq streams all {ROWS:,} features intact in a column order GDAL mis-reads")
