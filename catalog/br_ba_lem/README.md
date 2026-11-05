# Field boundaries for the west of Bahia state, Brazil

This dataset is the supplementary data of a paper published in the Data in Brief Journal.

The dataset, in ESRI shapefile format (spatial reference system: WGS 84, EPSG: 4326), provides monthly land use
information about 1854 fields from October 2019 to September 2020 from Luís Eduardo Magalhães (LEM) and other
municipalities in the west of Bahia state, Brazil. The majority of the 16 land uses classes are related to crops.

- **Source data provider:** [Mendeley Data](https://data.mendeley.com/datasets/vz6d7tw87f/1#file-5ac1542b-12ef-4dce-8258-113b5c5d87c9)
- **License:** CC-BY-4.0
- **Editions:** 2020 (one GeoParquet per year)
- **Fields in the latest edition (2020):** 1,854
- **Coordinate reference system:** EPSG:4326 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.30.0, vecorel-cli 0.4.2 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/br_ba_lem.py))
- **Data survey:** [BR-BA-LEM.md](https://github.com/fiboa/data-survey/blob/main/data/BR-BA-LEM.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/br_ba_lem/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/br_ba_lem/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2020 | 1,854 | [1.4 MB](https://data.source.coop/ftw/harmonized-field-data/br_ba_lem/year=2020/br_ba_lem-2020.parquet) | [712.8 KB](https://data.source.coop/ftw/harmonized-field-data/br_ba_lem/year=2020/br_ba_lem-2020.pmtiles) | [br_ba_lem-2020.json](https://data.source.coop/ftw/harmonized-field-data/br_ba_lem/year=2020/br_ba_lem-2020.json) |

The latest edition is also available at a stable path: [br_ba_lem/latest/br_ba_lem.parquet](https://data.source.coop/ftw/harmonized-field-data/br_ba_lem/latest/br_ba_lem.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/br_ba_lem/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/br_ba_lem/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `2020-04` | string | Carried over from the source column `Apr_2020`; the publisher documents no meaning for it. |
| `2020-03` | string | Carried over from the source column `Mar_2020`; the publisher documents no meaning for it. |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `2020-06` | string | Carried over from the source column `Jun_2020`; the publisher documents no meaning for it. |
| `2019-10` | string | Carried over from the source column `Oct_2019`; the publisher documents no meaning for it. |
| `2020-01` | string | Carried over from the source column `Jan_2020`; the publisher documents no meaning for it. |
| `2020-02` | string | Carried over from the source column `Feb_2020`; the publisher documents no meaning for it. |
| `2019-12` | string | Carried over from the source column `Dec_2019`; the publisher documents no meaning for it. |
| `2020-05` | string | Carried over from the source column `May_2020`; the publisher documents no meaning for it. |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `2020-09` | string | Carried over from the source column `Sep_2020`; the publisher documents no meaning for it. |
| `2020-08` | string | Carried over from the source column `Aug_2020`; the publisher documents no meaning for it. |
| `2019-11` | string | Carried over from the source column `Nov_2019`; the publisher documents no meaning for it. |
| `2020-07` | string | Carried over from the source column `Jul_2020`; the publisher documents no meaning for it. |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `BR`
- `admin:subdivision_code`: `BA`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/br_ba_lem/latest/br_ba_lem.parquet');
-- fields | hectares
-- 1854 | 251041.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Mendeley Data](https://data.mendeley.com/datasets/vz6d7tw87f/1#file-5ac1542b-12ef-4dce-8258-113b5c5d87c9) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.30.0, vecorel-cli 0.4.2:

- 2020: converted 2026-11-05 from <https://data.mendeley.com/public-files/datasets/vz6d7tw87f/files/57c83c3f-b5a9-45f5-94f8-ac1df8fab923/file_downloaded>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: Copyright © 2024 Elsevier inc, its licensors, and contributors.
