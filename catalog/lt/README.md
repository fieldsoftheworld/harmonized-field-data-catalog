# Lithuania crop fields

Collection of data on agricultural land and crop areas, cultivated crops in the territory of the Republic of Lithuania

- **Source data provider:** [Nacionalinė mokėjimo agentūra prie Žemės ūkio ministerijos <https://www.nma.lt>, Europe-LAND HE Project](https://doi.org/10.5281/zenodo.14230620)
- **License:** CC-BY-4.0
- **Editions:** 2024, 2025 (one GeoParquet per year)
- **Fields in the latest edition (2025):** 1,156,767
- **Coordinate reference system:** EPSG:3035 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.16 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/lt.py))
- **Data survey:** [LT.md](https://github.com/fiboa/data-survey/blob/main/data/LT.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/lt/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/lt/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2024 | 1,213,522 | [606.1 MB](https://data.source.coop/ftw/harmonized-field-data/lt/year=2024/lt-2024.parquet) | — | [lt-2024.json](https://data.source.coop/ftw/harmonized-field-data/lt/year=2024/lt-2024.json) |
| 2025 | 1,156,767 | [600.0 MB](https://data.source.coop/ftw/harmonized-field-data/lt/year=2025/lt-2025.parquet) | [238.3 MB](https://data.source.coop/ftw/harmonized-field-data/lt/year=2025/lt-2025.pmtiles) | [lt-2025.json](https://data.source.coop/ftw/harmonized-field-data/lt/year=2025/lt-2025.json) |

The latest edition is also available at a stable path: [lt/latest/lt.parquet](https://data.source.coop/ftw/harmonized-field-data/lt/latest/lt.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/lt/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/lt/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2025-01-01T00:00:00Z`
- `crop:code_list`: `https://raw.githubusercontent.com/maja601/EuroCrops/refs/heads/main/csvs/country_mappings/lt_2021.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/lt/latest/lt.parquet');
-- fields | hectares
-- 1156767 | 2915116.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Nacionalinė mokėjimo agentūra prie Žemės ūkio ministerijos <https://www.nma.lt>, Europe-LAND HE Project](https://doi.org/10.5281/zenodo.14230620) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.16:

- 2024: converted 2026-09-10 from <https://zenodo.org/records/18670815/files/LT_years_2024-2025.zip>
- 2025: converted 2026-09-10 from <https://zenodo.org/records/18670815/files/LT_years_2024-2025.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: Nacionalinė mokėjimo agentūra prie Žemės ūkio ministerijos
