# Field blocks for Bulgaria

The agricultural part of the Bulgarian physical block register (физически блокове): a physical block is a
contiguous area of land bounded by permanent features, identified as <EKATTE settlement code>-<block number>
and classified by its use. The register has been produced from field checks and orthophoto mapping.

These layers hold the blocks used agriculturally — arable land, greenhouses, rice fields and courtyards —
where the Physical_Blocks layers of the same service also carry forest, urban and transport land.

- **Source data provider:** [Ministry of Agriculture and Food](https://www.mzh.government.bg)
- **License:** CC-BY-4.0
- **Editions:** 2021, 2022, 2023, 2024, 2025 (one GeoParquet per year)
- **Fields in the latest edition (2025):** 226,592
- **Coordinate reference system:** EPSG:32635 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.16 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/bg.py))
- **Data survey:** [BG.md](https://github.com/fiboa/data-survey/blob/main/data/BG.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/bg/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/bg/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2021 | 202,384 | [145.7 MB](https://data.source.coop/ftw/harmonized-field-data/bg/year=2021/bg-2021.parquet) | — | [bg-2021.json](https://data.source.coop/ftw/harmonized-field-data/bg/year=2021/bg-2021.json) |
| 2022 | 199,819 | [151.9 MB](https://data.source.coop/ftw/harmonized-field-data/bg/year=2022/bg-2022.parquet) | — | [bg-2022.json](https://data.source.coop/ftw/harmonized-field-data/bg/year=2022/bg-2022.json) |
| 2023 | 163,944 | [133.1 MB](https://data.source.coop/ftw/harmonized-field-data/bg/year=2023/bg-2023.parquet) | — | [bg-2023.json](https://data.source.coop/ftw/harmonized-field-data/bg/year=2023/bg-2023.json) |
| 2024 | 172,872 | [143.1 MB](https://data.source.coop/ftw/harmonized-field-data/bg/year=2024/bg-2024.parquet) | — | [bg-2024.json](https://data.source.coop/ftw/harmonized-field-data/bg/year=2024/bg-2024.json) |
| 2025 | 226,592 | [174.8 MB](https://data.source.coop/ftw/harmonized-field-data/bg/year=2025/bg-2025.parquet) | [66.1 MB](https://data.source.coop/ftw/harmonized-field-data/bg/year=2025/bg-2025.pmtiles) | [bg-2025.json](https://data.source.coop/ftw/harmonized-field-data/bg/year=2025/bg-2025.json) |

The latest edition is also available at a stable path: [bg/latest/bg.parquet](https://data.source.coop/ftw/harmonized-field-data/bg/latest/bg.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/bg/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/bg/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name_en` | string | Crop name in English. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `block_id` | string | Field identifier (source column `PHBIDENT`, per the fiboa data survey) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `BG`
- `determination:datetime`: `2025-01-01T00:00:00Z`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/bg/latest/bg.parquet');
-- fields | hectares
-- 226592 | 3559220.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Ministry of Agriculture and Food](https://www.mzh.government.bg) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.16:

- 2021: converted 2026-09-13 from <http://inspire.mzh.government.bg:8080/geoserver/ows?request=GetFeature&service=WFS&version=2.0.0&outputFormat=SHAPE-ZIP&typeNames=VectorData:Agricultural_Land_2021&format_options=CHARSET:UTF-8>
- 2022: converted 2026-09-13 from <http://inspire.mzh.government.bg:8080/geoserver/ows?request=GetFeature&service=WFS&version=2.0.0&outputFormat=SHAPE-ZIP&typeNames=VectorData:Agricultural_Land_2022&format_options=CHARSET:UTF-8>
- 2023: converted 2026-09-13 from <http://inspire.mzh.government.bg:8080/geoserver/ows?request=GetFeature&service=WFS&version=2.0.0&outputFormat=SHAPE-ZIP&typeNames=VectorData:Agricultural_Land_2023&format_options=CHARSET:UTF-8>
- 2024: converted 2026-09-13 from <http://inspire.mzh.government.bg:8080/geoserver/ows?request=GetFeature&service=WFS&version=2.0.0&outputFormat=SHAPE-ZIP&typeNames=VectorData:Agricultural_Land_2024&format_options=CHARSET:UTF-8>
- 2025: converted 2026-09-13 from <http://inspire.mzh.government.bg:8080/geoserver/ows?request=GetFeature&service=WFS&version=2.0.0&outputFormat=SHAPE-ZIP&typeNames=VectorData:Agricultural_Land_2025&format_options=CHARSET:UTF-8>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribute the data to Ministry of Agriculture and Food.
