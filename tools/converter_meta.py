#!/usr/bin/env python3
"""Dump the metadata a fiboa-cli converter declares, as JSON.

Run with the Python interpreter that has fiboa-cli installed (build.py does
this through $FIBOA_PYTHON), so the catalog tooling itself never imports
fiboa-cli:

    python tools/converter_meta.py nl > staging/nl/converter.json

Everything printed here is what the converter author wrote in
fiboa_cli/datasets/<id>.py — attested metadata, not research.
"""
from __future__ import annotations

import json
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    dataset_id = sys.argv[1]

    from fiboa_cli import Registry  # noqa: F401  (sets up the fiboa registry)
    from fiboa_cli.converters import Converters

    converter = Converters().load(dataset_id)
    variants = getattr(converter, "variants", None) or {}
    sources = {}
    for variant in variants or [None]:
        if variant is not None:
            converter.variant = variant
        urls = converter.get_urls()
        if isinstance(urls, dict):
            urls = list(urls.keys())
        elif isinstance(urls, str):
            urls = [urls]
        sources[variant or ""] = urls or []

    meta = {
        "id": getattr(converter, "id", dataset_id),
        "cli_id": dataset_id,
        "short_name": getattr(converter, "short_name", ""),
        "title": getattr(converter, "title", ""),
        "description": (getattr(converter, "description", "") or "").strip(),
        "provider": getattr(converter, "provider", None),
        "attribution": getattr(converter, "attribution", None),
        "license": getattr(converter, "license", None),
        "variants": list(variants.keys()) if isinstance(variants, dict) else list(variants),
        "sources": sources,
        "columns": getattr(converter, "columns", {}),
        "extensions": sorted(getattr(converter, "extensions", set()) or []),
        "ec_mapping_csv": getattr(converter, "ec_mapping_csv", None),
        "area_is_in_ha": getattr(converter, "area_is_in_ha", None),
        "area_calculate_missing": getattr(converter, "area_calculate_missing", None),
        "use_variant_as_determination": getattr(converter, "use_variant_as_determination", None),
        "fiboa_cli_version": Registry.get_version(),
    }
    json.dump(meta, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
