# Field boundaries for Bavaria, Germany

A field block (German: "Feldblock") is a contiguous agricultural area surrounded by permanent boundaries, which is cultivated by one or more farmers with one or more crops, is fully or partially set aside or is fully or partially taken out of production.

- **Source data provider:** [Bayerische Vermessungsverwaltung](https://www.ldbv.bayern.de)
- **License:** CC-BY-4.0
- **Editions:** 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 1,296,105
- **Coordinate reference system:** EPSG:25832 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/de_by.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/de_by/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_by/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2026 | 1,296,105 | [286.5 MB](https://data.source.coop/ftw/harmonized-field-data/de_by/year=2026/de_by.parquet) | [164.3 MB](https://data.source.coop/ftw/harmonized-field-data/de_by/year=2026/de_by.pmtiles) | [de_by-2026.json](https://data.source.coop/ftw/harmonized-field-data/de_by/year=2026/de_by-2026.json) |

The latest edition is also available at a stable path: [de_by/latest/de_by.parquet](https://data.source.coop/ftw/harmonized-field-data/de_by/latest/de_by.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/de_by/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_by/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `determination:datetime` | timestamp[ms, tz=UTC] | The last timestamp at which the field did exist and was observed. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `DE`
- `admin:subdivision_code`: `BY`
- `crop:code_list`: `https://fiboa.org/code/de/de_by.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/de_by/latest/de_by.parquet');
-- fields
-- 1296105
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Bayerische Vermessungsverwaltung](https://www.ldbv.bayern.de) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2026: converted 2026-08-22 from <https://geodaten.bayern.de/odd/m/3/daten/ln/landnutzung.gpkg>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: Datenquelle: Bayerische Vermessungsverwaltung – www.geodaten.bayern.de
