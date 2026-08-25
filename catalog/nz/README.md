# Irrigated land area

This dataset covers Irrigated Land. Adapted by Ministry for the Environment and Statistics
New Zealand to provide for environmental reporting transparency

The spatial data covers all mainland regions of New Zealand, with the exception of Nelson, which is not believed to
contain significant irrigated areas. The spatial dataset is an update of the national dataset that was first
created in 2017. The current update has incorporated data from the 2019 – 2020 irrigation season.

- **Source data provider:** [Aqualinc Research Limited](https://environment.govt.nz/publications/national-irrigated-land-spatial-dataset-2020-update)
- **License:** CC-BY-4.0
- **Editions:** 2017, 2020 (one GeoParquet per year)
- **Fields in the latest edition (2020):** 42,133
- **Coordinate reference system:** EPSG:2193 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/nz.py))
- **Data survey:** [NZ.md](https://github.com/fiboa/data-survey/blob/main/data/NZ.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/nz/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/nz/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2017 | 32,762 | [8.6 MB](https://data.source.coop/ftw/harmonized-field-data/nz/year=2017/nz-2017.parquet) | — | [nz-2017.json](https://data.source.coop/ftw/harmonized-field-data/nz/year=2017/nz-2017.json) |
| 2020 | 42,133 | [13.8 MB](https://data.source.coop/ftw/harmonized-field-data/nz/year=2020/nz-2020.parquet) | [9.3 MB](https://data.source.coop/ftw/harmonized-field-data/nz/year=2020/nz-2020.pmtiles) | [nz-2020.json](https://data.source.coop/ftw/harmonized-field-data/nz/year=2020/nz-2020.json) |

The latest edition is also available at a stable path: [nz/latest/nz.parquet](https://data.source.coop/ftw/harmonized-field-data/nz/latest/nz.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/nz/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/nz/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `admin:subdivision_code` | string | ISO 3166-2 code for the principal subdivision (e.g., province or state, aka admin1) of a country that contains the field. Only the second part of the ISO 3166-2 code is stored. ([spec](https://github.com/vecorel/administrative-division-extension/blob/main/README.md)) |
| `determination:datetime` | timestamp[ms, tz=UTC] | The last timestamp at which the field did exist and was observed. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `type` | string | Irrigation type. Drip/micro, Rotorainer, Pivot, K-line/Long lateral, Unknown (per the fiboa data survey) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `NZ`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/nz/latest/nz.parquet');
-- fields | hectares
-- 42133 | 1006551.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Aqualinc Research Limited](https://environment.govt.nz/publications/national-irrigated-land-spatial-dataset-2020-update) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2017: converted 2026-08-25 from <mfe-irrigated-land-area-2017-SHP.zip>
- 2020: converted 2026-08-25 from <mfe-irrigated-land-area-raw-2020-update-SHP.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribute the data to Aqualinc Research Limited.
