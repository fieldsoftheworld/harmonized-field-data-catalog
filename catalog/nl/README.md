# BRP Crop Field Boundaries for The Netherlands (CAP-based)

BasisRegistratie Percelen (BRP) combines the location of
agricultural plots with the crop grown. The data set
is published by RVO (Netherlands Enterprise Agency). The boundaries of the agricultural plots
are based within the reference parcels (formerly known as AAN). A user an agricultural plot
annually has to register his crop fields with crops (for the Common Agricultural Policy scheme).
A dataset is generated for each year with reference date May 15.
A view service and a download service are available for the most recent BRP crop plots.

<https://service.pdok.nl/rvo/brpgewaspercelen/atom/v1_0/index.xml>

Data is currently available for the years 2009 to 2024.

- **Source data provider:** [RVO / PDOK](https://www.pdok.nl/introductie/-/article/basisregistratie-gewaspercelen-brp-)
- **License:** CC0-1.0
- **Editions:** 2025 (one GeoParquet per year)
- **Fields in the latest edition (2025):** 1,293,962
- **Coordinate reference system:** EPSG:28992 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/nl.py))
- **Data survey:** [NL.md](https://github.com/fiboa/data-survey/blob/main/data/NL.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/nl/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/nl/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2025 | 1,293,962 | [721.4 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2025/nl-2025.parquet) | [507.4 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2025/nl-2025.pmtiles) | [nl-2025.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2025/nl-2025.json) |

The latest edition is also available at a stable path: [nl/latest/nl.parquet](https://data.source.coop/ftw/harmonized-field-data/nl/latest/nl.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/nl/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/nl/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `coverage` | string | Land-cover category (Grass land, Arable field, Ditch, Landscape element) (source column `category`, per the fiboa data survey) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2025-05-15T00:00:00Z`
- `admin:country_code`: `NL`
- `crop:code_list`: `https://fiboa.org/code/nl/nl.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/nl/latest/nl.parquet');
-- fields | hectares
-- 1293962 | 1787357.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [RVO / PDOK](https://www.pdok.nl/introductie/-/article/basisregistratie-gewaspercelen-brp-) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2025: converted 2026-08-21 from <https://service.pdok.nl/rvo/brpgewaspercelen/atom/downloads/brpgewaspercelen_definitief_2025.gpkg>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC0-1.0. Attribute the data to RVO / PDOK.
