# Field boundaries for Switzerland

The cropfields of Switzerland (Nutzungsflächen) are published per administrative subdivision called Canton.

- **Source data provider:** [Konferenz der kantonalen Geoinformations- und Katasterstellen](https://www.kgk-cgc.ch)
- **License:** other — [opendata.swiss terms of use](https://opendata.swiss/en/terms-of-use) (converter: `opendata.swiss terms of use <https://opendata.swiss/en/terms-of-use>`)
- **Editions:** 2025 (one GeoParquet per year)
- **Fields in the latest edition (2025):** 1,350,979
- **Coordinate reference system:** EPSG:2056 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch.py))
- **Data survey:** [CH.md](https://github.com/fiboa/data-survey/blob/main/data/CH.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/ch/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ch/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2025 | 1,350,979 | [268.6 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch.parquet) | [155.4 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch.pmtiles) | [ch-2025.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch-2025.json) |

The latest edition is also available at a stable path: [ch/latest/ch.parquet](https://data.source.coop/ftw/harmonized-field-data/ch/latest/ch.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/ch/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ch/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `admin:subdivision_code` | string | ISO 3166-2 code for the principal subdivision (e.g., province or state, aka admin1) of a country that contains the field. Only the second part of the ISO 3166-2 code is stored. ([spec](https://github.com/vecorel/administrative-division-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `determination:datetime` | timestamp[ms, tz=UTC] | The last timestamp at which the field did exist and was observed. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `CH`
- `crop:code_list`: `https://fiboa.org/code/ch/ch.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/ch/latest/ch.parquet');
-- fields | hectares
-- 1350979 | 1390475.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Konferenz der kantonalen Geoinformations- und Katasterstellen](https://www.kgk-cgc.ch) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2025: converted 2026-08-25 from a manually obtained file

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

other — [opendata.swiss terms of use](https://opendata.swiss/en/terms-of-use) (converter: `opendata.swiss terms of use <https://opendata.swiss/en/terms-of-use>`). Attribute the data to Konferenz der kantonalen Geoinformations- und Katasterstellen.
