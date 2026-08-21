# Harmonized Field Boundary Data

Official, non-AI field boundary datasets — typically published by governments from their agricultural subsidy registers (IACS/LPIS), cadastres and statistics — harmonized into the [fiboa](https://github.com/fiboa/specification) schema with [fiboa-cli](https://github.com/fiboa/cli) and republished as cloud-native GeoParquet and PMTiles. 3 collections (BE, DE, NL), 2,630,704 fields in their latest editions. Each collection is one source dataset, partitioned by edition year; `*/latest/*.parquet` reads the newest edition of every collection. Hosted by [Fields of the World](https://fieldsofthe.world) on [Source Cooperative](https://source.coop/ftw/harmonized-field-data); the metadata is maintained in the [harmonized-field-data-catalog repository](https://github.com/fieldsoftheworld/harmonized-field-data-catalog), where corrections are welcome as pull requests. Start at the catalog [AGENTS.md](https://source.coop/ftw/harmonized-field-data/AGENTS.md) for cross-dataset queries.

## Collections

| Collection | Source data provider | Editions | Fields (latest) | License | Docs |
|---|---|---|---:|---|---|
| [Field boundaries for Flanders, Belgium](https://source.coop/ftw/harmonized-field-data/be_vlg) | [Agentschap Landbouw & Zeevisserij (Government)](https://landbouwcijfers.vlaanderen.be/open-geodata-landbouwgebruikspercelen) | 2023, 2024, 2025 | 594,732 | other | [README](https://source.coop/ftw/harmonized-field-data/be_vlg/README.md) · [agents](https://source.coop/ftw/harmonized-field-data/be_vlg/AGENTS.md) |
| [Field boundaries for North Rhine-Westphalia (NRW), Germany](https://source.coop/ftw/harmonized-field-data/de_nrw) | [Land Nordrhein-Westfalen / Open.NRW](https://www.opengeodata.nrw.de/produkte/umwelt_klima/bodennutzung/landwirtschaft/) | 2026 | 742,010 | DL-DE-BY-2.0 | [README](https://source.coop/ftw/harmonized-field-data/de_nrw/README.md) · [agents](https://source.coop/ftw/harmonized-field-data/de_nrw/AGENTS.md) |
| [BRP Crop Field Boundaries for The Netherlands (CAP-based)](https://source.coop/ftw/harmonized-field-data/nl) | [RVO / PDOK](https://www.pdok.nl/introductie/-/article/basisregistratie-gewaspercelen-brp-) | 2025 | 1,293,962 | CC0-1.0 | [README](https://source.coop/ftw/harmonized-field-data/nl/README.md) · [agents](https://source.coop/ftw/harmonized-field-data/nl/AGENTS.md) |

## Access

Everything is static files on object storage: query them in place with DuckDB, GeoPandas or any GeoParquet reader, and render the PMTiles with MapLibre. Newest edition of every collection:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT regexp_extract(filename, '/([^/]+)/latest/', 1) AS collection, count(*) AS fields
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/*/latest/*.parquet', union_by_name = true, filename = true)
GROUP BY 1 ORDER BY 1;
-- collection | fields
-- be_vlg | 594732
-- de_nrw | 742010
-- nl | 1293962
```

## License

Each collection carries the license of its source data provider (see the table and each `collection.json`). The catalog metadata, styles and tooling are Apache-2.0, in the [repository](https://github.com/fieldsoftheworld/harmonized-field-data-catalog).

## Provenance

A mirror: every collection links its original source (`rel: via`) and the fiboa data survey entry describing it, and records the fiboa-cli version that converted it. Conversion logic lives in [fiboa-cli](https://github.com/fiboa/cli); this repository only orchestrates publication. Previously published at [source.coop/fiboa/data](https://source.coop/fiboa/data).
