# Field boundaries for Czech

The cropfields of Czech (Plodina)

- **Source data provider:** [Czech Ministry of Agriculture (Ministr Zemědělství)](https://mze.gov.cz/public/portal/mze/farmar/LPIS)
- **License:** CC0-1.0
- **Editions:** 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 415,301
- **Coordinate reference system:** EPSG:4258 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/cz.py))
- **Data survey:** [CZ.md](https://github.com/fiboa/data-survey/blob/main/data/CZ.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/cz/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/cz/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2026 | 415,301 | [320.1 MB](https://data.source.coop/ftw/harmonized-field-data/cz/year=2026/cz-2026.parquet) | [144.4 MB](https://data.source.coop/ftw/harmonized-field-data/cz/year=2026/cz-2026.pmtiles) | [cz-2026.json](https://data.source.coop/ftw/harmonized-field-data/cz/year=2026/cz-2026.json) |

The latest edition is also available at a stable path: [cz/latest/cz.parquet](https://data.source.coop/ftw/harmonized-field-data/cz/latest/cz.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/cz/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/cz/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `determination:datetime` | timestamp[ms, tz=UTC] | The last timestamp at which the field did exist and was observed. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `block_id` | string | Carried over from the source column `DPB_ID`; the publisher documents no meaning for it. |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `CZ`
- `crop:code_list`: `https://raw.githubusercontent.com/maja601/EuroCrops/refs/heads/main/csvs/country_mappings/cz_2023.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/cz/latest/cz.parquet');
-- fields | hectares
-- 415301 | 2527960.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Czech Ministry of Agriculture (Ministr Zemědělství)](https://mze.gov.cz/public/portal/mze/farmar/LPIS) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2026: converted 2026-08-22 from <https://agrigis.gov.cz/portal/sharing/rest/content/items/7bcdda9b19724faba447585683c4cfd1/data>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC0-1.0. Attribute the data to Czech Ministry of Agriculture (Ministr Zemědělství).
