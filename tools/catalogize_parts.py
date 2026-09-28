"""catalogize for a collection with ``parts``: one collection fed by several converters.

Switzerland's cantons publish their usage areas under their own terms, so ``ch``
is one collection with one item per canton and year. Input, per part edition
(see common.py for the staging layout):

    staging/<id>/year=<Y>/<part>-<Y>.parquet
    staging/<id>/year=<Y>/<part>-<Y>.collection.json
    staging/<id>/converters/<part>.json
    staging/<id>/latest/<id>.pmtiles          the newest edition of every part

Output under ``catalog/<id>/``:

    collection.json                   license `other`, a license link per distinct license
    year=<Y>/<part>-<Y>.json          one item per part edition, with the part's own
                                      license, attribution, providers and via
    latest/<part>.parquet             the newest edition of every part (symlink)
    latest/<id>.pmtiles               the tiles of all of them (symlink)
    styles/*.json, README.md, AGENTS.md, llms.txt

The same rule holds as for any collection: every sentence is attested (the data
survey's overview, the converters' metadata) or derived from the files, with
the query printed.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import catalogize as cz
import common
from common import (
    FILE_EXTENSION,
    PARQUET_TYPE,
    PARTITION_EXTENSION,
    PARTITION_KEY,
    PMTILES_TYPE,
    PORTOLAN_EXTENSION,
    PROCESSING_EXTENSION,
    PROJECTION_EXTENSION,
    TABLE_EXTENSION,
    WEB_MAP_LINKS_EXTENSION,
    Dataset,
    Manifest,
    catalog_year_dir,
    determination_years,
    duckdb_s3_setup,
    file_facts,
    file_stem,
    fmt_bytes,
    fmt_int,
    glob_base,
    hcat_unmapped,
    parse_link_str,
    partition_dir,
    publish_config,
    write_json,
    write_text,
)

YearInput = cz.YearInput


def catalogize_parts(ds: Dataset, manifest: Manifest) -> None:
    config = publish_config()
    public_base = config["public_base"].rstrip("/")
    human_base = manifest.catalog["human_base"].rstrip("/")
    editions = ds.editions()
    staged = {part_id for part_id, _ in editions}
    missing = [part_id for part_id in ds.parts if part_id not in staged]
    if missing:
        sys.exit(f"{ds.id}: nothing staged for {', '.join(missing)}; run tools/build.py {ds.id}")
    metas = {part_id: cz.load_converter_meta(ds.id, part_id) for part_id in ds.parts}
    inputs = [YearInput(ds.id, year, part_id) for part_id, year in editions]
    newest = {y.part_id: y for y in inputs}  # inputs ascend by year
    latest = {part_id: newest[part_id] for part_id in ds.parts}
    pmtiles = common.STAGING_DIR / ds.id / "latest" / f"{ds.id}.pmtiles"
    if not pmtiles.exists():
        sys.exit(f"missing {pmtiles}: run tools/build.py {ds.id} (it tiles the newest edition of every part)")

    link_files(ds, inputs, latest, pmtiles)

    survey_url, text = cz.survey_text(ds.id)
    overview = cz.survey_overview(text, survey_url) if text else None
    if not overview:
        sys.exit(f"{ds.id}: the collection is described by the Overview of its data survey entry, and there is none")
    survey_props = cz.survey_properties(text)

    latest_glob = common.STAGING_DIR / ds.id / "latest" / "*.parquet"
    style_assets, _ = cz.write_styles(ds, ds.title, str(latest_glob), f"../latest/{pmtiles.name}")
    items = [part_item(ds, metas[y.part_id], y, survey_props) for y in inputs]
    table_columns = cz.union_columns(items)
    collection = parts_collection(ds, metas, inputs, latest, items, manifest, human_base, table_columns, style_assets, survey_url, overview, pmtiles)

    for y, item in zip(inputs, items):
        write_json(catalog_year_dir(ds.id, y.year) / f"{item['id']}.json", item)
    write_json(common.CATALOG_DIR / ds.id / "collection.json", collection)
    parts_docs(ds, metas, inputs, latest, collection, manifest, public_base, human_base, survey_url, overview)
    print(f"catalogized {ds.id}: {len(ds.parts)} part(s), {len(inputs)} edition(s), {len(style_assets)} style(s), {len(table_columns)} columns")


def link_files(ds: Dataset, inputs: list[YearInput], latest: dict[str, YearInput], pmtiles: Path) -> None:
    """Symlink the data into catalog/ and keep staging's latest/ to the newest edition per part.

    The editions and latest/ under catalog/<id>/ are rewritten whole, so an
    edition or a part that left the manifest does not linger there.
    """
    cdir = common.CATALOG_DIR / ds.id
    for stale in [*cdir.glob(f"{PARTITION_KEY}=*"), cdir / "latest"]:
        if stale.is_dir():
            shutil.rmtree(stale)
    staged_latest = pmtiles.parent
    for stale in staged_latest.glob("*.parquet"):
        if stale.stem not in latest:
            stale.unlink()
    for y in inputs:
        cz.link_data_file(y.parquet, catalog_year_dir(ds.id, y.year) / y.parquet.name)
    for part_id, y in latest.items():
        copy = staged_latest / f"{part_id}.parquet"
        cz.copy_latest(y.parquet, copy)
        cz.link_data_file(copy, cdir / "latest" / copy.name)
    cz.link_data_file(pmtiles, cdir / "latest" / pmtiles.name)


def part_providers(stac: dict, meta: dict) -> list[dict]:
    providers = list(stac.get("providers") or [])
    name, url = parse_link_str(meta.get("provider"))
    if not providers and name:
        providers = [{"name": name, "roles": ["producer", "licensor"], **({"url": url} if url else {})}]
    return providers


def spdx_link(lic: str) -> dict:
    return {"rel": "license", "href": f"https://spdx.org/licenses/{lic}.html", "type": "text/html", "title": lic}


def part_license(y: YearInput) -> tuple[str, list[dict]]:
    """(license, links) of one part edition; an SPDX id gets a link to its SPDX page."""
    lic, links = cz.license_fields(y.stac)
    if not links and lic != "other":
        links = [spdx_link(lic)]
    return lic, links


def year_mix(y: YearInput) -> str:
    """A sentence on a file that holds other years than its edition, or ''."""
    counts = determination_years(y.parquet)
    others = [f"{fmt_int(n)} from {year}" for year, n in counts if year != y.year]
    if not others:
        return ""
    own = sum(n for year, n in counts if year == y.year)
    return (
        f" The file is the source's state when it was converted, and not all of it is from {y.year}: "
        f"by `determination:datetime`, {fmt_int(own)} fields are from {y.year}, {', '.join(others)}."
    )


def part_item(ds: Dataset, meta: dict, y: YearInput, survey_props: dict[str, str]) -> dict:
    lic, license_links = part_license(y)
    description = (
        f"{meta['short_name']}, {y.year} edition: one GeoParquet file (`{y.parquet.name}`, "
        f"{fmt_int(y.row_count)} fields) converted with the fiboa-cli converter `{y.part_id}`. "
        f"Partition `{PARTITION_KEY}={y.year}` of the collection's hive layout. The terms are this "
        "source's own: see `license`, `attribution` and `providers` on this item."
    ) + year_mix(y)
    notes = ds.parts[y.part_id].notes
    if notes:
        description += f" {notes}"
    item = cz.build_item(ds.id, file_stem(y.part_id, y.year), meta, y, survey_props, description)
    props = item["properties"]
    props["license"] = lic
    if meta.get("attribution"):
        props["attribution"] = meta["attribution"]
    props["providers"] = part_providers(y.stac, meta)
    item["links"] += [dict(link) for link in license_links]
    _, via = parse_link_str(meta.get("provider"))
    if via:
        item["links"].append({"rel": "via", "href": via, "type": "text/html", "title": "Original source (publisher page)"})
    item["links"].append({"rel": "related", "href": converter_url(y.part_id), "type": "text/html", "title": "Converter source code (fiboa-cli)"})
    return item


def converter_url(part_id: str) -> str:
    return f"{cz.FIBOA_CLI_REPO}/blob/main/fiboa_cli/datasets/{part_id}.py"


def lic_md(y: YearInput) -> str:
    lic, links = cz.license_fields(y.stac)
    if lic != "other":
        return lic
    return f"other — [{links[0].get('title') or 'license terms'}]({links[0]['href']})" if links else "other"


def parts_collection(
    ds: Dataset,
    metas: dict[str, dict],
    inputs: list[YearInput],
    latest: dict[str, YearInput],
    items: list[dict],
    manifest: Manifest,
    human_base: str,
    table_columns: list[dict],
    style_assets: dict,
    survey_url: str | None,
    overview: str,
    pmtiles: Path,
) -> dict:
    config = publish_config()
    glob = f"{glob_base(config)}/{ds.id}/{PARTITION_KEY}=*/*.parquet"
    latest_glob = f"{glob_base(config)}/{ds.id}/latest/*.parquet"
    years = sorted({y.year for y in inputs})
    crs_values = sorted({y.crs for y in inputs if y.crs})
    names = ", ".join(f"{metas[p]['short_name']} (`{p}`)" for p in latest)

    parts_text = (
        f"\n\nThis collection is fed by {len(latest)} fiboa-cli converters, one per source: {names}. "
        f"It holds {len(inputs)} editions ({years[0]}–{years[-1]}), one GeoParquet file and one STAC item per source "
        f"and year: `{PARTITION_KEY}=<year>/<converter>-<year>.parquet`. The sources publish under different terms, "
        "so the collection's license is `other` with a link to each, and every item carries its own source's "
        "`license`, `attribution` and `providers`."
    )
    access = (
        f"\n\nRead every edition at once with the partition glob `{glob}`, or the newest edition of every source "
        f"with `{latest_glob}` (S3 through the Source Cooperative proxy, endpoint `{config.get('endpoint_url')}`; "
        "plain https cannot expand `*`; the files differ in columns, so read them with `union_by_name = true`). "
        f"Geometries are kept in the source CRS ({', '.join(crs_values)}). Converted with [fiboa-cli]({cz.FIBOA_CLI_REPO}) "
        f"into the [fiboa]({cz.FIBOA_SPEC}) schema; tested queries are in the collection's "
        f"[AGENTS.md]({human_base}/{ds.id}/AGENTS.md)."
    )

    license_links: list[dict] = []
    for y in inputs:
        for link in part_license(y)[1]:
            if link["href"] not in {known["href"] for known in license_links}:
                license_links.append(link)

    providers: list[dict] = []
    for y in latest.values():
        for provider in part_providers(y.stac, metas[y.part_id]):
            if provider.get("name") not in {known.get("name") for known in providers}:
                providers.append(provider)
    providers.append(dict(manifest.host))

    base = next(iter(latest.values())).stac
    collection = {
        "type": "Collection",
        "stac_version": "1.1.0",
        "stac_extensions": [
            PORTOLAN_EXTENSION,
            FILE_EXTENSION,
            TABLE_EXTENSION,
            PROJECTION_EXTENSION,
            PROCESSING_EXTENSION,
            WEB_MAP_LINKS_EXTENSION,
            PARTITION_EXTENSION,
        ],
        "id": ds.id,
        "title": ds.title,
        "description": overview + parts_text + access + cz.PROVENANCE[ds.boundaries],
        "boundaries": ds.boundaries,
        "keywords": sorted(set(["field boundaries", "agriculture", "fiboa", *ds.keywords])),
        "license": "other",
        "providers": providers,
        "extent": {
            "spatial": {"bbox": [cz.bbox_union([y.bbox for y in inputs])]},
            "temporal": {
                "interval": [
                    [
                        min(cz.year_interval(y.year, y.interval)[0] for y in inputs),
                        max(cz.year_interval(y.year, y.interval)[1] for y in inputs),
                    ]
                ]
            },
        },
        **({"summaries": {"proj:code": crs_values}} if crs_values else {}),
        "table:columns": table_columns,
        "table:primary_geometry": "geometry",
        # Switzerland as it is now: the newest edition of every part
        "table:row_count": sum(y.row_count or 0 for y in latest.values()),
        "partition:scheme": "hive",
        "partition:strategy": "temporal",
        "partition:keys": [
            {
                "name": PARTITION_KEY,
                "type": "int32",
                "description": "Edition year of the source dataset: the converter variant, or for a source without variants the most frequent year of `determination:datetime` in the file. Not a column in the files; DuckDB adds it with hive_partitioning=true. Expand the glob through S3 (endpoint data.source.coop, path style); plain https has no listing.",
            }
        ],
        "partition:file_count": len(inputs),
        "partition:glob": glob,
        "assets": {
            **{
                f"data-{part_id}": {
                    "href": f"./latest/{part_id}.parquet",
                    "type": PARQUET_TYPE,
                    "title": f"{metas[part_id]['short_name']} — latest edition ({y.year}) (GeoParquet)",
                    "description": f"Byte-identical copy of `{partition_dir(y.year)}/{y.parquet.name}`, kept at a stable path so `{ds.id}/latest/*.parquet` selects the newest edition of every source.",
                    "roles": ["data"],
                    "file:size": y.data_asset["file:size"],
                    "file:checksum": y.data_asset["file:checksum"],
                    "proj:code": y.crs,
                }
                for part_id, y in latest.items()
            },
            "visual": {
                "href": f"./latest/{pmtiles.name}",
                "type": PMTILES_TYPE,
                "title": f"{ds.title} — latest edition of every source (PMTiles)",
                "roles": ["visual"],
                **file_facts(pmtiles),
            },
            **style_assets,
        },
        "links": [
            {"rel": "root", "href": "../catalog.json", "type": "application/json"},
            {"rel": "parent", "href": "../catalog.json", "type": "application/json"},
            *license_links,
            {"rel": "agents", "href": "./AGENTS.md", "type": "text/markdown", "title": "Guidance for AI agents"},
            {"rel": "describedby", "href": "./README.md", "type": "text/markdown", "title": "Human-readable documentation"},
            {"rel": "llms", "href": "./llms.txt", "type": "text/markdown", "title": "Agent/LLM usage guide"},
            {"rel": "pmtiles", "href": f"./latest/{pmtiles.name}", "type": PMTILES_TYPE, "title": "Web map tiles", "pmtiles:layers": [ds.id]},
        ],
        "updated": max(cz.iso_mtime(y.parquet) for y in latest.values()),
    }
    for key in ("fiboa_version", "vecorel_version"):
        if key in base:
            collection[key] = base[key]
    attributions = [metas[p].get("attribution") for p in latest if metas[p].get("attribution")]
    if attributions:
        collection["attribution"] = "; ".join(dict.fromkeys(attributions))

    thumbnail = cz.thumbnail_asset(ds)
    if thumbnail:
        collection["assets"]["thumbnail"] = thumbnail
    if ds.via:
        collection["links"].append({"rel": "via", "href": ds.via, "type": "text/html", "title": "Original source (publisher page)"})
    if survey_url:
        collection["links"].append({"rel": "related", "href": survey_url, "type": "text/html", "title": "fiboa data survey entry for this source"})
    for item in items:
        year = item["properties"][PARTITION_KEY]
        collection["links"].append(
            {"rel": "item", "href": f"./{partition_dir(year)}/{item['id']}.json", "type": "application/geo+json", "title": item["properties"]["title"]}
        )
    return collection


def parts_docs(
    ds: Dataset,
    metas: dict[str, dict],
    inputs: list[YearInput],
    latest: dict[str, YearInput],
    collection: dict,
    manifest: Manifest,
    public_base: str,
    human_base: str,
    survey_url: str | None,
    overview: str,
) -> None:
    cdir = common.CATALOG_DIR / ds.id
    config = publish_config()
    s3 = glob_base(config)
    glob = collection["partition:glob"]
    latest_glob = f"{s3}/{ds.id}/latest/*.parquet"
    first = next(iter(latest))
    example = f"{public_base}/{ds.id}/latest/{first}.parquet"
    years = sorted({y.year for y in inputs})
    columns = collection["table:columns"]
    latest_columns = [{c["name"] for c in y.data_asset.get("table:columns", [])} for y in latest.values()]
    everywhere = set.intersection(*latest_columns)
    somewhere = set.union(*latest_columns)
    has_area = "metrics:area" in everywhere
    hcat_cols = "hcat:code" in somewhere
    software = sorted({f"{k} {v}" for y in latest.values() for k, v in y.data_asset.get("processing:software", {}).items()})
    software_md = ", ".join(software) or "fiboa-cli"
    crs = ", ".join(collection.get("summaries", {}).get("proj:code", []))
    total = collection["table:row_count"]
    part_lines = []
    for part_id, y in latest.items():
        prov_name, prov_url = parse_link_str(metas[part_id].get("provider"))
        prov = f"[{prov_name}]({prov_url})" if prov_url else (prov_name or "—")
        part_years = ", ".join(i.year for i in inputs if i.part_id == part_id)
        part_lines.append(
            f"| {metas[part_id]['short_name']} | [`{part_id}`]({converter_url(part_id)}) | {part_years} | {fmt_int(y.row_count)} | {lic_md(y)} | {prov} |"
        )
    notes = [f"- **{metas[p]['short_name']}:** {part.notes}" for p, part in ds.parts.items() if part.notes]

    # -- README.md
    lines = [f"# {ds.title}", "", overview, ""]
    lines += [
        f"- **Sources:** {len(latest)}, each converted by its own fiboa-cli converter and published under its own terms (see [Sources](#sources))",
        "- **License:** other — per source, carried by each item (see [License](#license))",
        f"- **Editions:** {', '.join(years)} ({len(inputs)} files, one per source and year)",
        f"- **Fields in the newest edition of every source:** {fmt_int(total)}",
        f"- **Coordinate reference system:** {crs} (as published by the sources; not reprojected)",
        f"- **Converted with:** {software_md}",
    ]
    if survey_url:
        lines.append(f"- **Data survey:** [{Path(survey_url).name}]({survey_url})")
    lines += ["", f"Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/{public_base.removeprefix('https://')}/{ds.id}/collection.json), or start from the [AGENTS.md]({human_base}/{ds.id}/AGENTS.md) for tested queries.", ""]
    lines += ["## Sources", "", "| Source | Converter | Editions | Fields (newest) | License | Source data provider |", "|---|---|---|---:|---|---|", *part_lines, ""]
    if notes:
        lines += notes + [""]
    if ds.notes:
        lines += [ds.notes, ""]
    lines += ["## Files", "", "| Year | Source | Fields | GeoParquet | STAC item |", "|---|---|---:|---|---|"]
    for y in inputs:
        base = f"{public_base}/{ds.id}/{partition_dir(y.year)}"
        stem = file_stem(y.part_id, y.year)
        lines.append(f"| {y.year} | {metas[y.part_id]['short_name']} | {fmt_int(y.row_count)} | [{fmt_bytes(y.data_asset['file:size'])}]({base}/{y.parquet.name}) | [{stem}.json]({base}/{stem}.json) |")
    lines += ["", f"The newest edition of every source is also at a stable path, `{ds.id}/latest/<converter>.parquet` (e.g. [{first}.parquet]({example})), and tiled together in [{ds.id}/latest/{ds.id}.pmtiles]({public_base}/{ds.id}/latest/{ds.id}.pmtiles). `{latest_glob}` reads the newest editions together, `{glob}` every edition (S3 globs; see the [AGENTS.md]({human_base}/{ds.id}/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).", ""]
    lines += ["## Columns", "", "| Column | Type | Description |", "|---|---|---|"]
    for c in columns:
        note = "" if c["name"] in everywhere else " *(not a column in every source's newest edition)*"
        lines.append(f"| `{c['name']}` | {c['type']} | {c.get('description', '')}{note} |")
    lines += ["", "A value that is the same for every field of a file is stored once, in the file's GeoParquet `collection` metadata, rather than as a column; that is why the sources' files do not all have the same columns.", ""]
    lines += ["## Access", "", "Query the published files in place with DuckDB; nothing needs downloading first. Fields per source in their newest editions:", ""]
    area = ', round(sum("metrics:area") / 1e4) AS hectares' if has_area else ""
    q1 = f"INSTALL spatial; LOAD spatial;\n{duckdb_s3_setup(config)}\nSELECT regexp_extract(filename, '([^/]+)\\.parquet$', 1) AS source, count(*) AS fields{area}\nFROM read_parquet('{latest_glob}', union_by_name = true, filename = true)\nGROUP BY 1 ORDER BY 1;"
    lines += [cz.md_query(q1, public_base), ""]
    lines += ["## Provenance", ""]
    lines.append(f"This catalog is a mirror: the data is produced and licensed by the sources listed above and republished here as cloud-native GeoParquet and PMTiles by {manifest.host['name']}. Each edition was downloaded from its source and converted with {software_md}:")
    lines.append("")
    for y in inputs:
        sources = metas[y.part_id].get("sources", {})
        urls = sources.get(y.year) or sources.get("") or []
        lines.append(f"- {y.year}, {metas[y.part_id]['short_name']}: converted {cz.iso_mtime(y.parquet)[:10]} from " + (", ".join(f"<{u}>" for u in urls) if urls else "a manually obtained file"))
    lines += ["", f"The conversion is deterministic and lives in [fiboa-cli]({cz.FIBOA_CLI_REPO}); changes to how a column is mapped are made there, not in this catalog.", "", "## License", ""]
    lines.append("Each source publishes under its own terms, and the STAC item of every edition carries them (`license`, `attribution`, `providers`). The collection's license is `other`. The map tiles show all sources together and name each of them in their attribution.")
    lines.append("")
    for part_id, y in latest.items():
        attribution = metas[part_id].get("attribution")
        lines.append(f"- {metas[part_id]['short_name']} (`{part_id}`): {lic_md(y)}." + (f" Attribution: {attribution}" if attribution else ""))
    write_text(cdir / "README.md", "\n".join(lines))

    # -- AGENTS.md
    a = [f"# Agent guidance — {ds.title}", ""]
    a.append(f"Field boundaries in the [fiboa]({cz.FIBOA_SPEC}) schema from {len(latest)} sources, each with its own fiboa-cli converter and terms, {len(inputs)} editions ({', '.join(years)}). Every claim below is quoted from the source, the converters, or measured from the published files; each query was run before it was written down, and its output follows it as comments.")
    a += ["", "## Access", ""]
    a.append(f"- Newest edition of one source, stable path: `{public_base}/{ds.id}/latest/<converter>.parquet`, e.g. `{example}`. Converters: " + ", ".join(f"`{p}`" for p in latest) + ".")
    a.append(f"- Newest edition of every source: `{latest_glob}`, and every edition: `{glob}` — the S3 form of the same prefix through the Source Cooperative proxy, because `*` needs a listing that plain https does not provide. In DuckDB: `CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT '{config.get('endpoint_url', '').replace('https://', '')}', URL_STYLE 'path', REGION '{config.get('region', 'us-west-2')}');` then `read_parquet(glob, union_by_name = true, filename = true)`; `hive_partitioning = true` adds the `{PARTITION_KEY}` column. No credentials are needed.")
    a.append(f"- One edition: `{public_base}/{ds.id}/{PARTITION_KEY}=<year>/<converter>-<year>.parquet`, e.g. `{public_base}/{ds.id}/{partition_dir(latest[first].year)}/{latest[first].parquet.name}`")
    a.append(f"- PMTiles for maps: `{public_base}/{ds.id}/latest/{ds.id}.pmtiles`, layer `{ds.id}`, the newest edition of every source; MapLibre styles in `styles/`.")
    a += ["", "## Quirks that produce silently wrong answers", ""]
    a.append("- **The terms differ per source.** The collection's `license` is `other`; the terms of a row are those of its file's STAC item (`license`, `attribution`, `providers`): " + "; ".join(f"`{p}` {lic_md(y)}" for p, y in latest.items()) + ".")
    a.append("- **The files do not have the same columns.** A value that is the same for every field of a file is stored once in its GeoParquet `collection` metadata instead of as a column (read it with `parquet_kv_metadata()`), so read the files with `union_by_name = true` and take the source from the file name (`filename = true`)." + (" Not a column in every newest edition: " + ", ".join(f"`{c}`" for c in sorted(somewhere - everywhere)) + "." if somewhere - everywhere else ""))
    a.append(f"- **CRS is {crs}, not WGS84.** `ST_Area`/`ST_Distance` return units of that CRS; transform with `ST_Transform` if you need lon/lat, or use `metrics:area`.")
    if has_area:
        a.append("- **`metrics:area` is in square metres.** Divide by 10 000 for hectares.")
    a.append(f"- **`{PARTITION_KEY}` is the edition, not the observation date.** For a converter with variants it is the variant; a source without variants is converted once and filed under the most frequent year of its `determination:datetime`, and its item says when the file holds other years too.")
    a.append("- **`id` is only guaranteed unique within one file** (fiboa requires uniqueness per file). Whether an id persists across editions is not verified here; do not join editions on it without checking.")
    if hcat_cols:
        unmapped = hcat_unmapped(str(common.STAGING_DIR / ds.id / "latest" / "*.parquet")) or 0
        share = (
            f"All {fmt_int(total)} rows of the newest editions carry one."
            if not unmapped
            else f"{fmt_int(unmapped)} of the {fmt_int(total)} rows of the newest editions ({unmapped / total * 100:.2f}%) have none, so a query that filters or groups on crop silently leaves them out."
        )
        a.append(f"- **`hcat:code` is hierarchical.** The first 4/6/8 digits are increasingly specific crop groups; compare prefixes, not equality, to aggregate (see the crop query below). {share}")
    a += [f"- {line[2:]}" for line in notes]
    if ds.notes:
        a.append(f"- {ds.notes}")
    a += ["", "## Tested queries", ""]
    a.append("Fields and hectares per edition and source, through the partition glob:")
    a.append("")
    area_expr = ', round(sum("metrics:area") / 1e4) AS hectares' if has_area else ""
    q = f"{duckdb_s3_setup(config)}\nSELECT {PARTITION_KEY}, regexp_extract(filename, '([^/]+)-[0-9]{{4}}\\.parquet$', 1) AS source, count(*) AS fields{area_expr}\nFROM read_parquet('{glob}', hive_partitioning = true, union_by_name = true, filename = true)\nGROUP BY 1, 2 ORDER BY 1, 2;"
    a += [cz.md_query(q, public_base), ""]
    if hcat_cols:
        a.append("Largest crop groups in the newest edition of every source (HCAT level 3 = first 6 digits):")
        a.append("")
        measure = ', round(sum("metrics:area") / 1e4) AS hectares' if has_area else ""
        order = "hectares" if has_area else "fields"
        q = f"{duckdb_s3_setup(config)}\nSELECT substr(CAST(\"hcat:code\" AS VARCHAR), 1, 6) AS hcat_group, mode(\"hcat:name\") AS most_common_name,\n       count(*) AS fields{measure}\nFROM read_parquet('{latest_glob}', union_by_name = true)\nWHERE \"hcat:code\" IS NOT NULL\nGROUP BY 1 ORDER BY {order} DESC LIMIT 5;"
        a += [cz.md_query(q, public_base), ""]
    largest = max(latest.values(), key=lambda y: y.row_count or 0)
    if largest.crs:
        a.append(f"Fields around a point in the largest source ({metas[largest.part_id]['short_name']}), transforming the point into the data's CRS instead of the data into WGS84:")
        a.append("")
        cx = (largest.bbox[0] + largest.bbox[2]) / 2
        cy = (largest.bbox[1] + largest.bbox[3]) / 2
        sel = 'id, round("metrics:area") AS m2' if has_area else "id"
        url = f"{public_base}/{ds.id}/latest/{largest.part_id}.parquet"
        q = f"INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;\nSELECT {sel}\nFROM read_parquet('{url}')\nWHERE ST_Intersects(geometry, ST_Buffer(ST_Transform(ST_Point({cy:.4f}, {cx:.4f}), 'EPSG:4326', '{largest.crs}'), 500))\nLIMIT 5;"
        try:
            a += [cz.md_query(q, public_base), ""]
        except Exception as exc:  # noqa: BLE001 — a failed recipe is not shipped
            print(f"note: spatial query skipped for {ds.id}: {exc}")
    a += ["## Related collections", "", f"Every collection in this catalog shares the fiboa core columns, so the same queries work across countries; `{s3}/*/latest/*.parquet` with `union_by_name = true` reads the newest edition of all of them (see the catalog [AGENTS.md]({human_base}/AGENTS.md)).", "", "## Structure", "", "Assets and structural links resolve relative to the object that carries them; there is no `self` link. Source: this collection is generated by [tools/catalogize_parts.py]({0}/blob/main/tools/catalogize_parts.py) in the catalog repository — fix documentation there.".format(manifest.catalog["repository"])]
    write_text(cdir / "AGENTS.md", "\n".join(a))

    # -- llms.txt
    host = manifest.host["name"]
    l = [f"# {ds.title}", "", f"Field boundaries from {len(latest)} sources ({', '.join(years)}) as fiboa GeoParquet + PMTiles, mirrored by {host}. License: other — each source's own, on its STAC items.", ""]
    l.append(f"- Newest per source: {public_base}/{ds.id}/latest/<converter>.parquet, converters " + ", ".join(latest))
    l.append(f"- All newest: {latest_glob}; all editions: {glob} (S3 via endpoint {config.get('endpoint_url')}, path style, anonymous; union_by_name=true, filename=true; hive_partitioning=true adds `{PARTITION_KEY}`)")
    l.append(f"- CRS {crs}; `metrics:area` in m²; `{PARTITION_KEY}` = edition, `id` unique per file only.")
    l.append(f"- Columns: {', '.join(c['name'] for c in columns)}")
    l.append(f"- Docs: {human_base}/{ds.id}/README.md, agent guide {human_base}/{ds.id}/AGENTS.md, STAC {public_base}/{ds.id}/collection.json")
    write_text(cdir / "llms.txt", "\n".join(l))
