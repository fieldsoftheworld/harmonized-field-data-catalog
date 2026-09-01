# Field boundaries for Schleswig-Holstein (SH), Germany

A field block (German: "Feldblock") is a contiguous agricultural area surrounded by permanent boundaries, which is cultivated by one or more farmers with one or more crops, is fully or partially set aside or is fully or partially taken out of production.

- **Source data provider:** [Land Schleswig-Holstein](https://sh-mis.gdi-sh.de/catalog/#/datasets/iso/21f67269-780f-4f3c-8f66-03dde27acfe7)
- **License:** DL-DE-ZERO-2.0
- **Editions:** 2023, 2024, 2025, 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 194,503
- **Coordinate reference system:** EPSG:4647 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.16 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/de_sh.py))
- **Data survey:** [DE-SH.md](https://github.com/fiboa/data-survey/blob/main/data/DE-SH.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/de_sh/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_sh/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2023 | 198,614 | [62.1 MB](https://data.source.coop/ftw/harmonized-field-data/de_sh/year=2023/de_sh-2023.parquet) | — | [de_sh-2023.json](https://data.source.coop/ftw/harmonized-field-data/de_sh/year=2023/de_sh-2023.json) |
| 2024 | 197,673 | [61.9 MB](https://data.source.coop/ftw/harmonized-field-data/de_sh/year=2024/de_sh-2024.parquet) | — | [de_sh-2024.json](https://data.source.coop/ftw/harmonized-field-data/de_sh/year=2024/de_sh-2024.json) |
| 2025 | 195,747 | [61.7 MB](https://data.source.coop/ftw/harmonized-field-data/de_sh/year=2025/de_sh-2025.parquet) | — | [de_sh-2025.json](https://data.source.coop/ftw/harmonized-field-data/de_sh/year=2025/de_sh-2025.json) |
| 2026 | 194,503 | [61.5 MB](https://data.source.coop/ftw/harmonized-field-data/de_sh/year=2026/de_sh-2026.parquet) | [24.7 MB](https://data.source.coop/ftw/harmonized-field-data/de_sh/year=2026/de_sh-2026.pmtiles) | [de_sh-2026.json](https://data.source.coop/ftw/harmonized-field-data/de_sh/year=2026/de_sh-2026.json) |

The latest edition is also available at a stable path: [de_sh/latest/de_sh.parquet](https://data.source.coop/ftw/harmonized-field-data/de_sh/latest/de_sh.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/de_sh/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_sh/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `flik` | string | The area identifier (FLIK code) is a 16-character string. ([spec](https://github.com/fiboa/flik-extension/blob/main/README.md)) |
| `hbn` | string | Category of main land use (see below) (source column `HBN`, per the fiboa data survey) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2026-01-01T00:00:00Z`
- `admin:country_code`: `DE`
- `admin:subdivision_code`: `SH`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/de_sh/latest/de_sh.parquet');
-- fields | hectares
-- 194503 | 984410.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Land Schleswig-Holstein](https://sh-mis.gdi-sh.de/catalog/#/datasets/iso/21f67269-780f-4f3c-8f66-03dde27acfe7) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.16:

- 2023: converted 2026-09-01 from <https://service.gdi-sh.de/SH_OpenGBD/feeds/Atom_SH_Feldblockfinder_OpenGBD/data/Feldbloecke_2023_GPKG.zip>
- 2024: converted 2026-09-01 from <https://service.gdi-sh.de/SH_OpenGBD/feeds/Atom_SH_Feldblockfinder_OpenGBD/data/Feldbloecke_2024_GPKG.zip>
- 2025: converted 2026-09-01 from <https://service.gdi-sh.de/SH_OpenGBD/feeds/Atom_SH_Feldblockfinder_OpenGBD/data/Feldbloecke_2025_GPKG.zip>
- 2026: converted 2026-09-01 from <https://service.gdi-sh.de/SH_OpenGBD/feeds/Atom_SH_Feldblockfinder_OpenGBD/data/Feldbloecke_2026_GPKG.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

DL-DE-ZERO-2.0. Attribute the data to Land Schleswig-Holstein.
