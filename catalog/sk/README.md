# Slovakia Agricultural Land Identification System

Systém identifikácie poľnohospodárskych pozemkov (LPIS)

LPIS is an agricultural land identification system. It represents the vector boundaries of agricultural land
and carries information about the unique code, acreage, culture/land use, etc., which is used as a reference
for farmers' applications, for administrative and cross-checks, on-site checks and also checks using remote
sensing methods.

Dataset Hranice užívania contains the use declared by applicants for direct support.

- **Source data provider:** [Pôdohospodárska platobná agentúra](https://www.apa.sk)
- **License:** CC0-1.0
- **Editions:** 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 271,807
- **Coordinate reference system:** EPSG:5514 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.16 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/sk.py))
- **Data survey:** [SK.md](https://github.com/fiboa/data-survey/blob/main/data/SK.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/sk/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/sk/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2018 | 240,600 | [217.2 MB](https://data.source.coop/ftw/harmonized-field-data/sk/year=2018/sk-2018.parquet) | — | [sk-2018.json](https://data.source.coop/ftw/harmonized-field-data/sk/year=2018/sk-2018.json) |
| 2019 | 247,544 | [242.4 MB](https://data.source.coop/ftw/harmonized-field-data/sk/year=2019/sk-2019.parquet) | — | [sk-2019.json](https://data.source.coop/ftw/harmonized-field-data/sk/year=2019/sk-2019.json) |
| 2020 | 249,393 | [255.8 MB](https://data.source.coop/ftw/harmonized-field-data/sk/year=2020/sk-2020.parquet) | — | [sk-2020.json](https://data.source.coop/ftw/harmonized-field-data/sk/year=2020/sk-2020.json) |
| 2021 | 255,712 | [274.1 MB](https://data.source.coop/ftw/harmonized-field-data/sk/year=2021/sk-2021.parquet) | — | [sk-2021.json](https://data.source.coop/ftw/harmonized-field-data/sk/year=2021/sk-2021.json) |
| 2022 | 264,084 | [314.3 MB](https://data.source.coop/ftw/harmonized-field-data/sk/year=2022/sk-2022.parquet) | — | [sk-2022.json](https://data.source.coop/ftw/harmonized-field-data/sk/year=2022/sk-2022.json) |
| 2023 | 275,830 | [314.3 MB](https://data.source.coop/ftw/harmonized-field-data/sk/year=2023/sk-2023.parquet) | — | [sk-2023.json](https://data.source.coop/ftw/harmonized-field-data/sk/year=2023/sk-2023.json) |
| 2024 | 275,049 | [327.3 MB](https://data.source.coop/ftw/harmonized-field-data/sk/year=2024/sk-2024.parquet) | — | [sk-2024.json](https://data.source.coop/ftw/harmonized-field-data/sk/year=2024/sk-2024.json) |
| 2025 | 273,387 | [334.6 MB](https://data.source.coop/ftw/harmonized-field-data/sk/year=2025/sk-2025.parquet) | — | [sk-2025.json](https://data.source.coop/ftw/harmonized-field-data/sk/year=2025/sk-2025.json) |
| 2026 | 271,807 | [341.7 MB](https://data.source.coop/ftw/harmonized-field-data/sk/year=2026/sk-2026.parquet) | [113.3 MB](https://data.source.coop/ftw/harmonized-field-data/sk/year=2026/sk-2026.pmtiles) | [sk-2026.json](https://data.source.coop/ftw/harmonized-field-data/sk/year=2026/sk-2026.json) |

The latest edition is also available at a stable path: [sk/latest/sk.parquet](https://data.source.coop/ftw/harmonized-field-data/sk/latest/sk.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/sk/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/sk/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `municipality` | string | Municipality (source column `LOKALITA_N`, per the fiboa data survey) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `block_id` | string | code KD (source column `KODKD`, per the fiboa data survey) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `crop_group` | string | Crop Group (source column `KULTURA_NA`, per the fiboa data survey) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `SK`
- `determination:datetime`: `2026-01-01T00:00:00Z`
- `crop:code_list`: `https://fiboa.org/code/sk/sk.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/sk/latest/sk.parquet');
-- fields | hectares
-- 271807 | 1779089.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Pôdohospodárska platobná agentúra](https://www.apa.sk) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.16:

- 2018: converted 2026-09-12 from <https://data.slovensko.sk/download?id=a6773bee-ec27-4626-b5fb-8bbfc7765cee&blocksize=0>
- 2019: converted 2026-09-12 from <https://data.slovensko.sk/download?id=b0b42cfc-7605-4fb9-82db-fee913d09230&blocksize=0>
- 2020: converted 2026-09-12 from <https://data.slovensko.sk/download?id=adc9765b-6ce4-43b2-9d31-263a740dd779&blocksize=0>
- 2021: converted 2026-09-12 from <https://data.slovensko.sk/download?id=97d82440-b904-4671-8a24-2dc5b13a61f5&blocksize=0>
- 2022: converted 2026-09-12 from <https://data.slovensko.sk/download?id=68f005a1-49d3-47ac-9717-a533c3a0508e&blocksize=0>
- 2023: converted 2026-09-12 from <https://data.slovensko.sk/download?id=f90f29e6-e222-432e-a4ef-c97cc1c5fb61&blocksize=0>
- 2024: converted 2026-09-12 from <https://data.slovensko.sk/download?id=16daebac-f974-4002-81ee-053e10d1e2a3&blocksize=0>
- 2025: converted 2026-09-12 from <https://data.slovensko.sk/download?id=56f934e9-3c6b-48c6-9115-cac418b4bb41&blocksize=0>
- 2026: converted 2026-09-12 from <https://data.slovensko.sk/download?id=5a88fa63-04d7-4496-93ce-796f553a6478&blocksize=0>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC0-1.0. Attribute the data to Pôdohospodárska platobná agentúra.
