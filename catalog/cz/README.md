# Field boundaries for Czech

The cropfields of Czech (Plodina)

- **Source data provider:** [Czech Ministry of Agriculture (Ministr Zemědělství)](https://mze.gov.cz/public/portal/mze/farmar/LPIS)
- **License:** CC0-1.0
- **Editions:** 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 415,300
- **Coordinate reference system:** EPSG:4258 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.16 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/cz.py))
- **Data survey:** [CZ.md](https://github.com/fiboa/data-survey/blob/main/data/CZ.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/cz/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/cz/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2019 | 292,798 | [211.5 MB](https://data.source.coop/ftw/harmonized-field-data/cz/year=2019/cz-2019.parquet) | — | [cz-2019.json](https://data.source.coop/ftw/harmonized-field-data/cz/year=2019/cz-2019.json) |
| 2020 | 312,512 | [241.7 MB](https://data.source.coop/ftw/harmonized-field-data/cz/year=2020/cz-2020.parquet) | — | [cz-2020.json](https://data.source.coop/ftw/harmonized-field-data/cz/year=2020/cz-2020.json) |
| 2021 | 331,329 | [255.5 MB](https://data.source.coop/ftw/harmonized-field-data/cz/year=2021/cz-2021.parquet) | — | [cz-2021.json](https://data.source.coop/ftw/harmonized-field-data/cz/year=2021/cz-2021.json) |
| 2022 | 327,692 | [267.5 MB](https://data.source.coop/ftw/harmonized-field-data/cz/year=2022/cz-2022.parquet) | — | [cz-2022.json](https://data.source.coop/ftw/harmonized-field-data/cz/year=2022/cz-2022.json) |
| 2023 | 397,798 | [334.2 MB](https://data.source.coop/ftw/harmonized-field-data/cz/year=2023/cz-2023.parquet) | — | [cz-2023.json](https://data.source.coop/ftw/harmonized-field-data/cz/year=2023/cz-2023.json) |
| 2024 | 426,583 | [351.7 MB](https://data.source.coop/ftw/harmonized-field-data/cz/year=2024/cz-2024.parquet) | — | [cz-2024.json](https://data.source.coop/ftw/harmonized-field-data/cz/year=2024/cz-2024.json) |
| 2025 | 411,105 | [317.4 MB](https://data.source.coop/ftw/harmonized-field-data/cz/year=2025/cz-2025.parquet) | — | [cz-2025.json](https://data.source.coop/ftw/harmonized-field-data/cz/year=2025/cz-2025.json) |
| 2026 | 415,300 | [321.8 MB](https://data.source.coop/ftw/harmonized-field-data/cz/year=2026/cz-2026.parquet) | [143.4 MB](https://data.source.coop/ftw/harmonized-field-data/cz/year=2026/cz-2026.pmtiles) | [cz-2026.json](https://data.source.coop/ftw/harmonized-field-data/cz/year=2026/cz-2026.json) |

The latest edition is also available at a stable path: [cz/latest/cz.parquet](https://data.source.coop/ftw/harmonized-field-data/cz/latest/cz.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/cz/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/cz/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `block_id` | string | Carried over from the source column `DPB_ID`; the publisher documents no meaning for it. |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `determination:datetime` | timestamp[ms, tz=UTC] | The last timestamp at which the field did exist and was observed. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
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
-- 415300 | 2527959.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Czech Ministry of Agriculture (Ministr Zemědělství)](https://mze.gov.cz/public/portal/mze/farmar/LPIS) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.16:

- 2019: converted 2026-09-12 from <https://agrigis.gov.cz/portal/sharing/rest/content/items/9cbc2b4429704b73863596fa5f488d27/data>
- 2020: converted 2026-09-12 from <https://agrigis.gov.cz/portal/sharing/rest/content/items/c843561778b44b308485aafdbb813d76/data>
- 2021: converted 2026-09-12 from <https://agrigis.gov.cz/portal/sharing/rest/content/items/c662c15b70794a06937096be54c095ab/data>
- 2022: converted 2026-09-12 from <https://agrigis.gov.cz/portal/sharing/rest/content/items/791cd91c4f354c9085173fc267b2be4d/data>
- 2023: converted 2026-09-12 from <https://agrigis.gov.cz/portal/sharing/rest/content/items/d9a6e306fe534a059519fdf788da1df6/data>
- 2024: converted 2026-09-12 from <https://agrigis.gov.cz/portal/sharing/rest/content/items/1b315e81ce474b3b808b4940808bb106/data>
- 2025: converted 2026-09-12 from <https://agrigis.gov.cz/portal/sharing/rest/content/items/2cac84bb1f5245598f0334c6011ef5a6/data>
- 2026: converted 2026-09-12 from <https://agrigis.gov.cz/portal/sharing/rest/content/items/7bcdda9b19724faba447585683c4cfd1/data>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC0-1.0. Attribute the data to Czech Ministry of Agriculture (Ministr Zemědělství).
