"""MapLibre GL styles for a field boundary collection.

Every style is chosen from what the data actually holds (``common.hcat_groups``,
``common.column_stats``), not from column names alone. The browser derives a
legend only from a ``fill`` layer whose ``fill-color`` is a top-level ``match``
or ``step`` expression (portolan-browser ``extractLegend``), so the styles
below are written in exactly that shape:

* HCAT crops — an outer ``match`` on human-readable crop names carries the
  legend; an inner ``match`` maps ``hcat:code`` values to those names. Colours
  come from the palette fiboa.org uses on its crop map (``hcat_palette.json``,
  from fiboa/fiboa.github.io ``map/crop/codes2.js``), made distinct where that
  palette falls back to its group default.
* Field size — a ``step`` on ``metrics:area`` expressed in hectares, with stops
  picked from the measured quantiles.
* Outline — a plain fill + outline in a per-collection colour, for reading the
  boundaries themselves.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from common import TOOLS_DIR, humanize

HCAT_PALETTE = json.loads((TOOLS_DIR / "hcat_palette.json").read_text())
HCAT_BY_CODE = {entry["code"]: entry for entry in HCAT_PALETTE}
HCAT_MAX_LEGEND = 12
OTHER_COLOR = "#c8c8c8"

# Outline colours, one per collection, so sibling datasets do not all read as
# the same pale blue in a card grid.
OUTLINE_PALETTE = [
    "#1b7837", "#2166ac", "#b2182b", "#762a83", "#e08214", "#35978f",
    "#8c510a", "#4d4d4d", "#c51b7d", "#01665e", "#5e3c99", "#d6604d",
]

HA_STOP_CANDIDATES = [0.1, 0.25, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500]
SIZE_RAMP = ["#f7fcf5", "#c7e9c0", "#74c476", "#238b45", "#00441b"]


def _source(pmtiles_rel: str) -> dict:
    return {"data": {"type": "vector", "url": f"pmtiles://{pmtiles_rel}"}}


def _base(name: str, pmtiles_rel: str, description: str) -> dict:
    return {
        "version": 8,
        "name": name,
        "metadata": {"description": description},
        "sources": _source(pmtiles_rel),
        "layers": [],
    }


def outline_style(collection_id: str, layer: str, pmtiles_rel: str, title: str) -> dict:
    idx = int(hashlib.md5(collection_id.encode()).hexdigest(), 16) % len(OUTLINE_PALETTE)
    color = OUTLINE_PALETTE[idx]
    style = _base(
        f"{title} — field boundaries",
        pmtiles_rel,
        "Every field in one colour with a thin outline; for reading the boundaries themselves.",
    )
    style["layers"] = [
        {
            "id": "fields-fill",
            "type": "fill",
            "source": "data",
            "source-layer": layer,
            "paint": {"fill-color": color, "fill-opacity": 0.25},
        },
        {
            "id": "fields-outline",
            "type": "line",
            "source": "data",
            "source-layer": layer,
            "paint": {"line-color": color, "line-width": 0.8},
        },
    ]
    return style


FALLBACK_PALETTE = [
    "#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f",
    "#ff7f00", "#cab2d6", "#6a3d9a", "#ffff99", "#b15928", "#8dd3c7", "#bebada",
]
GENERIC_HCAT_COLORS = {"#cc8c32"}  # the palette's "arable crops" default, reused by 41 groups


MIN_COLOR_DISTANCE = 48  # euclidean RGB distance below which two legend colours read as one


def _rgb(color: str) -> tuple[int, int, int]:
    c = color.lstrip("#")
    return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)


def _too_close(color: str, used: set[str]) -> bool:
    r, g, b = _rgb(color)
    return any(
        ((r - r2) ** 2 + (g - g2) ** 2 + (b - b2) ** 2) ** 0.5 < MIN_COLOR_DISTANCE
        for r2, g2, b2 in (_rgb(u) for u in used)
    )


def distinct_color(preferred: str | None, used: set[str]) -> str:
    """The palette colour when it is specific and distinct from the ones already
    in the legend, else the next fallback colour that is."""
    if preferred and preferred.lower() not in GENERIC_HCAT_COLORS and not _too_close(preferred, used):
        return preferred
    for color in FALLBACK_PALETTE:
        if not _too_close(color, used):
            return color
    return OTHER_COLOR


def hcat_style(
    crops: list[tuple[str, str | None, int, float]], layer: str, pmtiles_rel: str, title: str
) -> tuple[dict, list[dict]] | None:
    """Style + legend rows for the largest HCAT crops present in the data.

    ``crops`` is ``common.hcat_crops(parquet)``: (10-digit code, hcat:name, count,
    area in m²), largest area first. The top ``HCAT_MAX_LEGEND`` crops are named
    and coloured from the fiboa.org palette (made distinct where the palette
    repeats its group default); everything else is grey "Other". Returns None
    when the data carries no HCAT codes.
    """
    crops = [c for c in crops if c[0] and c[0].isdigit()]
    if not crops:
        return None
    total_area = sum(c[3] for c in crops) or 1
    total_count = sum(c[2] for c in crops) or 1

    legend = []
    used: set[str] = set()
    # hcat:code is a number in the tiles (uint32 in the parquet); match it as an
    # integer literal — MapLibre's to-string of the number does not equal the
    # code spelled out as a string, so a string match silently selects nothing.
    inner: list = ["match", ["get", "hcat:code"]]
    outer: list = ["match", inner]
    for code, name, count, area in crops[:HCAT_MAX_LEGEND]:
        entry = HCAT_BY_CODE.get(code)
        label = humanize(name or (entry["name"] if entry else f"HCAT {code}"))
        color = distinct_color(entry["color"] if entry else None, used)
        used.add(color.lower())
        inner.extend([int(code), label])
        outer.extend([label, color])
        legend.append(
            {
                "label": label,
                "code": code,
                "color": color,
                "count": count,
                "share": area / total_area if total_area else count / total_count,
            }
        )
    inner.append("Other")
    outer.append(OTHER_COLOR)
    rest = crops[HCAT_MAX_LEGEND:]
    if rest:
        legend.append(
            {
                "label": "Other",
                "code": "",
                "color": OTHER_COLOR,
                "count": sum(c[2] for c in rest),
                "share": sum(c[3] for c in rest) / total_area,
            }
        )

    style = _base(
        f"{title} — crops (HCAT)",
        pmtiles_rel,
        "Fields coloured by harmonized crop (EuroCrops HCAT code, `hcat:code`). The "
        f"{min(len(crops), HCAT_MAX_LEGEND)} crops covering the most area are named, everything else "
        "is grey. Colours follow the fiboa.org crop map palette.",
    )
    style["layers"] = [
        {
            "id": "fields-by-crop",
            "type": "fill",
            "source": "data",
            "source-layer": layer,
            "paint": {"fill-color": outer, "fill-opacity": 0.75},
        },
        {
            "id": "fields-outline",
            "type": "line",
            "source": "data",
            "source-layer": layer,
            "minzoom": 11,
            "paint": {"line-color": "rgba(60,60,60,0.5)", "line-width": 0.5},
        },
    ]
    return style, legend


def size_stops(stats: dict) -> list[float]:
    """Up to four ascending stops in hectares: nice values nearest the 20th, 40th,
    60th and 80th percentiles, so every class holds a similar share of fields."""
    stops = []
    for key in ("p20", "p40", "p60", "p80"):
        value = stats.get(key)
        if value is None:
            continue
        ha = float(value) / 10_000
        nearest = min(HA_STOP_CANDIDATES, key=lambda c: abs(c - ha))
        if nearest not in stops and (not stops or nearest > stops[-1]):
            stops.append(nearest)
    return stops or [1, 5, 20]


def field_size_style(stats: dict, layer: str, pmtiles_rel: str, title: str) -> dict:
    stops = size_stops(stats)
    ramp = SIZE_RAMP[: len(stops) + 1]
    expr: list = ["step", ["/", ["get", "metrics:area"], 10000], ramp[0]]
    for stop, color in zip(stops, ramp[1:]):
        expr.extend([stop, color])
    style = _base(
        f"{title} — field size (ha)",
        pmtiles_rel,
        "Fields shaded light to dark by area in hectares (metrics:area / 10 000). Stops at "
        + ", ".join(f"{s:g}" for s in stops)
        + " ha, the nice values nearest this dataset's 20th/40th/60th/80th percentiles so each class holds a similar share of fields.",
    )
    style["layers"] = [
        {
            "id": "fields-by-size",
            "type": "fill",
            "source": "data",
            "source-layer": layer,
            "paint": {"fill-color": expr, "fill-opacity": 0.8},
        },
        {
            "id": "fields-outline",
            "type": "line",
            "source": "data",
            "source-layer": layer,
            "minzoom": 11,
            "paint": {"line-color": "rgba(60,60,60,0.4)", "line-width": 0.5},
        },
    ]
    return style


def write_style(path: Path, style: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(style, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
