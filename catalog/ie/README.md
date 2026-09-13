# Ireland INSPIRE Geospatial aid application (GSAA) dataset

This data represents the outline shape of LPIS parcels as claimed under area based schemes. The dataset includes the crops claimed as part of the annual GSAA. Yearly information provided through the beneficiary declaration.

- **Source data provider:** [Department of Agriculture, Food and the Marine](https://www.gov.ie/en/organisation/department-of-agriculture-food-and-the-marine/)
- **License:** CC-BY-4.0
- **Editions:** 2022, 2023, 2024 (one GeoParquet per year)
- **Fields in the latest edition (2024):** 1,119,949
- **Coordinate reference system:** EPSG:4258 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.16 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ie.py))
- **Data survey:** [IE.md](https://github.com/fiboa/data-survey/blob/main/data/IE.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/ie/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ie/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2022 | 1,026,499 | [659.7 MB](https://data.source.coop/ftw/harmonized-field-data/ie/year=2022/ie-2022.parquet) | — | [ie-2022.json](https://data.source.coop/ftw/harmonized-field-data/ie/year=2022/ie-2022.json) |
| 2023 | 1,117,023 | [801.8 MB](https://data.source.coop/ftw/harmonized-field-data/ie/year=2023/ie-2023.parquet) | — | [ie-2023.json](https://data.source.coop/ftw/harmonized-field-data/ie/year=2023/ie-2023.json) |
| 2024 | 1,119,949 | [860.3 MB](https://data.source.coop/ftw/harmonized-field-data/ie/year=2024/ie-2024.parquet) | [337.5 MB](https://data.source.coop/ftw/harmonized-field-data/ie/year=2024/ie-2024.pmtiles) | [ie-2024.json](https://data.source.coop/ftw/harmonized-field-data/ie/year=2024/ie-2024.json) |

The latest edition is also available at a stable path: [ie/latest/ie.parquet](https://data.source.coop/ftw/harmonized-field-data/ie/latest/ie.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/ie/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ie/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

The department's INSPIRE bucket serves GSAA_2022, GSAA_2023 and GSAA_2024; GSAA_2017 through GSAA_2021 answer 403, so the earlier campaigns EuroCrops lists are no longer downloadable there.

## Columns

| Column | Type | Description |
|---|---|---|
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `parcel_id` | string | Identifier (source column `localId`, per the fiboa data survey) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2024-12-31T00:00:00Z`
- `admin:country_code`: `IE`
- `crop:code_list`: `https://fiboa.org/code/ie/ie.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/ie/latest/ie.parquet');
-- fields | hectares
-- 1119949 | 4946224.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Department of Agriculture, Food and the Marine](https://www.gov.ie/en/organisation/department-of-agriculture-food-and-the-marine/) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.16:

- 2022: converted 2026-09-13 from <https://dafm-inspire-atom.s3.eu-west-1.amazonaws.com/files/LU/GSAA_2022.zip>
- 2023: converted 2026-09-13 from <https://dafm-inspire-atom.s3.eu-west-1.amazonaws.com/files/LU/GSAA_2023.zip>
- 2024: converted 2026-09-13 from <https://dafm-inspire-atom.s3.eu-west-1.amazonaws.com/files/LU/GSAA_2024.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: Ireland Department of Agriculture, Food and the Marine
