#!/usr/bin/env python3
"""Render a collection's thumbnail from its default style with chiitiler.

Follows the Portolan thumbnails practice: frame a 3:2 window (the browser card
is 350-700 x 250 px), render the collection's *default* MapLibre style
server-side over a light basemap, and gate the result on a blank probe before
it is written to ``catalog/<id>/thumbnail.jpg`` (JPEG keeps the repository small). Field boundary layers are
dense polygon fabrics, so the frame is a zoomed window (strategy B) centred on
the densest cluster, at the PMTiles archive's max zoom so tippecanoe's
thinning does not show as holes.

Needs a running chiitiler (https://github.com/Kanahiro/chiitiler):

    git clone --depth 1 https://github.com/Kanahiro/chiitiler /tmp/chiitiler
    cd /tmp/chiitiler && npm install
    CHIITILER_PROCESSES=0 npx tsx src/main.ts tile-server --port 13579 --cache memory

    python tools/thumbnail.py nl            # writes catalog/nl/thumbnail.jpg
    python tools/thumbnail.py nl --zoom 13  # override the zoom
    python tools/thumbnail.py nl --rank 1   # second-densest cluster, for variety

Look at the image afterwards. The automated gate only proves that some data
landed in the frame, not that the picture is good.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import struct
import sys
from pathlib import Path

import requests

from common import CATALOG_DIR, Manifest, duckdb_connect, quote, read_json

PORT = int(os.environ.get("CHIITILER_PORT", "13579"))
SIZE = 1024
TARGET_ASPECT = 1.5
BASEMAP_URL = "https://basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png"
BASEMAP_OPACITY = 0.6
R = 6378137.0
EARTH_CIRC = 40075016.686


def mx(lon: float) -> float:
    return math.radians(lon) * R


def my(lat: float) -> float:
    lat = max(min(lat, 85.05112878), -85.05112878)
    return R * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


def inv_mx(x: float) -> float:
    return math.degrees(x / R)


def inv_my(y: float) -> float:
    return math.degrees(2 * math.atan(math.exp(y / R)) - math.pi / 2)


def span_for_zoom(z: float, size_px: int) -> float:
    return EARTH_CIRC * size_px / (256 * 2**z)


def window(clon: float, clat: float, z: float, size_px: int = SIZE) -> list[float]:
    """A 3:2 window at zoom z centred on (clon, clat), in degrees."""
    span = span_for_zoom(z, size_px)
    hw, hh = span / 2, span / (2 * TARGET_ASPECT)
    cx, cy = mx(clon), my(clat)
    return [inv_mx(cx - hw), inv_my(cy - hh), inv_mx(cx + hw), inv_my(cy + hh)]


def pmtiles_header(path: Path) -> dict:
    h = path.read_bytes()[:127]
    if h[:7] != b"PMTiles":
        sys.exit(f"{path} is not a PMTiles archive")
    bounds = [v / 1e7 for v in struct.unpack("<iiii", h[102:118])]
    clon, clat = (v / 1e7 for v in struct.unpack("<ii", h[119:127]))
    return {"min_zoom": h[100], "max_zoom": h[101], "center": [clon, clat, h[118]], "bounds": bounds}


def densest_cluster(parquet: Path, crs: str, zoom: float, rank: int) -> tuple[float, float, int]:
    """(lon, lat, count) of the rank-th densest window at this zoom, via the bbox column."""
    con = duckdb_connect()
    cell_m = span_for_zoom(zoom, SIZE) / 2  # half a frame, in metres (source CRS assumed metric or close)
    # work in the source CRS using the per-feature bbox covering column
    rows = con.execute(
        f"""
        WITH c AS (
          SELECT (bbox.xmin + bbox.xmax) / 2 AS x, (bbox.ymin + bbox.ymax) / 2 AS y
          FROM read_parquet({quote(parquet)})
        ), ext AS (
          SELECT max(x) - min(x) AS w, max(y) - min(y) AS h FROM c
        ), g AS (
          SELECT floor(x / {cell_m}) AS gx, floor(y / {cell_m}) AS gy, count(*) AS n FROM c GROUP BY 1, 2
        ), top AS (
          SELECT gx, gy FROM g ORDER BY n DESC LIMIT 1 OFFSET {int(rank)}
        )
        SELECT count(*), avg(x), avg(y) FROM c, top
        WHERE x BETWEEN (gx - 1) * {cell_m} AND (gx + 2) * {cell_m}
          AND y BETWEEN (gy - 1) * {cell_m} AND (gy + 2) * {cell_m}
        """
    ).fetchone()
    n, x, y = rows
    lon, lat = con.execute(
        f"SELECT ST_X(p), ST_Y(p) FROM (SELECT ST_Transform(ST_Point({x}, {y}), '{crs}', 'EPSG:4326', always_xy := true) AS p)"
    ).fetchone()
    return lon, lat, int(n)


def build_styles(style: dict, pmtiles: Path, header: dict) -> tuple[dict, dict, dict]:
    src = {
        "type": "vector",
        "tiles": [f"pmtiles://{pmtiles}/{{z}}/{{x}}/{{y}}"],
        "minzoom": header["min_zoom"],
        "maxzoom": header["max_zoom"],
    }
    layers = [layer for layer in style.get("layers", []) if layer.get("type") != "symbol"]
    sources = {key: dict(src) for key in style.get("sources", {})} or {"data": src}
    white = {"id": "background", "type": "background", "paint": {"background-color": "#ffffff"}}
    render = dict(style)
    render["sources"] = dict(sources)
    render["sources"]["basemap"] = {"type": "raster", "tiles": [BASEMAP_URL], "tileSize": 256}
    render["layers"] = [white, {"id": "basemap", "type": "raster", "source": "basemap", "paint": {"raster-opacity": BASEMAP_OPACITY}}, *layers]
    probe = dict(style)
    probe["sources"] = sources
    probe["layers"] = [white, *layers]
    blank = {"version": 8, "sources": {}, "layers": [white]}
    return render, probe, blank


def clip(style: dict, bbox: list[float], size: int, fmt: str = "png", quality: int = 90) -> bytes:
    url = f"http://localhost:{PORT}/clip.{fmt}?bbox={','.join(f'{v:.6f}' for v in bbox)}&size={size}&quality={quality}"
    r = requests.post(url, json={"style": style}, timeout=600)
    if r.status_code != 200:
        sys.exit(f"chiitiler returned {r.status_code}: {r.text[:200]}")
    return r.content


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("datasets", nargs="+")
    parser.add_argument("--zoom", type=float, help="window zoom (default: the archive's max zoom)")
    parser.add_argument("--rank", type=int, default=0, help="which densest cluster (0 = densest)")
    parser.add_argument("--center", help="lon,lat override for the window centre")
    args = parser.parse_args()

    try:
        requests.get(f"http://localhost:{PORT}/health", timeout=5)
    except requests.RequestException:
        sys.exit(f"chiitiler is not reachable on port {PORT}; see the module docstring")

    manifest = Manifest.load()
    for dataset_id in args.datasets:
        if dataset_id not in manifest.datasets:
            sys.exit(f"{dataset_id} is not in datasets.yaml")
        cdir = CATALOG_DIR / dataset_id
        coll = read_json(cdir / "collection.json")
        style_asset = next((a for a in coll["assets"].values() if "default" in a.get("roles", [])), None)
        visual = coll["assets"].get("visual")
        if not style_asset or not visual:
            print(f"{dataset_id}: no default style or no PMTiles, skipping")
            continue
        style = read_json(cdir / style_asset["href"])
        pmtiles = (cdir / visual["href"]).resolve()
        parquet = (cdir / coll["assets"]["data"]["href"]).resolve()
        crs = coll["assets"]["data"].get("proj:code") or "EPSG:4326"
        header = pmtiles_header(pmtiles)
        zoom = args.zoom if args.zoom is not None else float(header["max_zoom"])
        if args.center:
            clon, clat = (float(v) for v in args.center.split(","))
            n = -1
        else:
            clon, clat, n = densest_cluster(parquet, crs, zoom, args.rank)
        bbox = window(clon, clat, zoom)
        render, probe, blank = build_styles(style, pmtiles, header)
        image = clip(render, bbox, SIZE, "jpeg", 85)
        probe_png = clip(probe, bbox, 256, "png", 100)
        blank_png = clip(blank, bbox, 256, "png", 100)
        if hashlib.sha256(probe_png).digest() == hashlib.sha256(blank_png).digest():
            gate = "FAIL-empty"
        elif len(probe_png) < len(blank_png) * 1.15:
            gate = "WARN-sparse"
        else:
            gate = "PASS"
        out = cdir / "thumbnail.jpg"
        if gate.startswith("FAIL"):
            print(f"{dataset_id}: gate1={gate} — nothing rendered in the frame, not writing {out}")
            continue
        out.write_bytes(image)
        record = {
            "collection": dataset_id,
            "strategy": "B",
            "zoom": zoom,
            "rank": args.rank,
            "center": [round(clon, 5), round(clat, 5)],
            "features_in_window": n,
            "bbox": [round(v, 6) for v in bbox],
            "gate1": gate,
            "bytes": len(image),
        }
        print(json.dumps(record))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
