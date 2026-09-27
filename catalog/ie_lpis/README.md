# LPIS parcels for Ireland

Every parcel of Ireland's LPIS with the crop declared on it, from the "Anonymous LPIS" datasets the
Department of Agriculture, Food and the Marine publishes per campaign year (none for 2023 and 2024).
The source has one row per claim; here a parcel is one row with the crop of its largest claim, its
digitised and eligible area and the area claimed by all applicants together. Unclaimed parcels
(buildings, farmyards, bog) are kept and parcel identifiers are hashed by the department.

- **Source data provider:** [Department of Agriculture, Food and the Marine](https://data.gov.ie/organization/department-of-agriculture-food-and-the-marine)
- **License:** CC-BY-4.0
- **Editions:** 2017, 2018, 2019, 2020, 2021, 2022, 2025 (one GeoParquet per year)
- **Fields in the latest edition (2025):** 1,454,480
- **Coordinate reference system:** EPSG:2157 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.3.1 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ie_lpis.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/ie_lpis/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ie_lpis/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2017 | 1,310,933 | [538.6 MB](https://data.source.coop/ftw/harmonized-field-data/ie_lpis/year=2017/ie_lpis-2017.parquet) | — | [ie_lpis-2017.json](https://data.source.coop/ftw/harmonized-field-data/ie_lpis/year=2017/ie_lpis-2017.json) |
| 2018 | 1,308,587 | [540.9 MB](https://data.source.coop/ftw/harmonized-field-data/ie_lpis/year=2018/ie_lpis-2018.parquet) | — | [ie_lpis-2018.json](https://data.source.coop/ftw/harmonized-field-data/ie_lpis/year=2018/ie_lpis-2018.json) |
| 2019 | 1,306,462 | [551.6 MB](https://data.source.coop/ftw/harmonized-field-data/ie_lpis/year=2019/ie_lpis-2019.parquet) | — | [ie_lpis-2019.json](https://data.source.coop/ftw/harmonized-field-data/ie_lpis/year=2019/ie_lpis-2019.json) |
| 2020 | 1,311,162 | [596.6 MB](https://data.source.coop/ftw/harmonized-field-data/ie_lpis/year=2020/ie_lpis-2020.parquet) | — | [ie_lpis-2020.json](https://data.source.coop/ftw/harmonized-field-data/ie_lpis/year=2020/ie_lpis-2020.json) |
| 2021 | 1,309,443 | [653.9 MB](https://data.source.coop/ftw/harmonized-field-data/ie_lpis/year=2021/ie_lpis-2021.parquet) | — | [ie_lpis-2021.json](https://data.source.coop/ftw/harmonized-field-data/ie_lpis/year=2021/ie_lpis-2021.json) |
| 2022 | 1,421,266 | [759.3 MB](https://data.source.coop/ftw/harmonized-field-data/ie_lpis/year=2022/ie_lpis-2022.parquet) | — | [ie_lpis-2022.json](https://data.source.coop/ftw/harmonized-field-data/ie_lpis/year=2022/ie_lpis-2022.json) |
| 2025 | 1,454,480 | [920.5 MB](https://data.source.coop/ftw/harmonized-field-data/ie_lpis/year=2025/ie_lpis-2025.parquet) | [336.1 MB](https://data.source.coop/ftw/harmonized-field-data/ie_lpis/year=2025/ie_lpis-2025.pmtiles) | [ie_lpis-2025.json](https://data.source.coop/ftw/harmonized-field-data/ie_lpis/year=2025/ie_lpis-2025.json) |

The latest edition is also available at a stable path: [ie_lpis/latest/ie_lpis.parquet](https://data.source.coop/ftw/harmonized-field-data/ie_lpis/latest/ie_lpis.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/ie_lpis/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ie_lpis/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `eligible_area` | double | Carried over from the source column `MEA`; the publisher documents no meaning for it. |
| `claimed_area` | double | Carried over from the source column `CLAIM_AREA`; the publisher documents no meaning for it. |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `commonage` | bool | Carried over from the source column `COM_IND`; the publisher documents no meaning for it. |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `IE`
- `determination:datetime`: `2025-01-01T00:00:00Z`
- `crop:code_list`: `https://fiboa.org/code/ie/ie.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/ie_lpis/latest/ie_lpis.parquet');
-- fields | hectares
-- 1454480 | 5206763.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Department of Agriculture, Food and the Marine](https://data.gov.ie/organization/department-of-agriculture-food-and-the-marine) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.3.1:

- 2017: converted 2026-09-27 from <https://opendata.agriculture.gov.ie/dataset/a2e8ac1d-0776-4f6d-93f4-ffbf111117f0/resource/63eb5ec0-e643-4d42-84d6-fe27e362cfac/download/geoserviceshelp-54_parcels_2017_enc.zip>
- 2018: converted 2026-09-27 from <https://opendata.agriculture.gov.ie/dataset/dc7a6e57-673f-45ea-96fd-d30d1c8160ae/resource/c19b3135-2dd6-493d-816d-eed6584e3cc3/download/geoserviceshelp-54_parcels_2018_enc.zip>
- 2019: converted 2026-09-27 from <https://opendata.agriculture.gov.ie/dataset/e70b1882-8b87-4e29-940c-bd7d84110a09/resource/843134db-cc82-4d7a-ac4f-d3a7a1b96146/download/geoserviceshelp-54_parcels_2019_enc.zip>
- 2020: converted 2026-09-27 from <https://opendata.agriculture.gov.ie/dataset/ccac60d7-bc9b-40ec-83ba-198904d759f6/resource/11b02a59-6885-47f9-9b5c-6af33f0feed5/download/geoserviceshelp-54_parcels_2020_enc.zip>
- 2021: converted 2026-09-27 from <https://opendata.agriculture.gov.ie/dataset/1a87e9f7-a6a0-4f0f-845d-1b1ce6babd6d/resource/3f358eba-17ab-4ea9-a8e8-c9e4ce56cf50/download/geoserviceshelp-54_parcels_2021_enc.zip>
- 2022: converted 2026-09-27 from <https://opendata.agriculture.gov.ie/dataset/ecd6db57-820f-48c0-8142-5aaae7378689/resource/8797641f-2f58-4f3b-a5e3-8427de8c9bea/download/geoserviceshelp-100_parcels_rnd_2022.zip>
- 2025: converted 2026-09-27 from <https://opendata.agriculture.gov.ie/dataset/40d859ac-58a8-4082-98d2-4ebf1c7cdd29/resource/bd5a8a3b-cc9f-498d-9f40-dc7006d4efee/download/geo_860-parcels_gpk_2025.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: Ireland Department of Agriculture, Food and the Marine
