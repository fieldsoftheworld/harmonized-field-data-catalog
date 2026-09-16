# Spain Extremadura Crop fields

SIGPAC recintos of Extremadura, from the national release by the Spanish
paying agency. The region's own download portal (sitex.gobex.es) has not answered since at
least 2026-09-10.

- **Source data provider:** [Fondo Español de Garantía Agraria (FEGA)](https://www.fega.gob.es)
- **License:** CC-BY-4.0
- **Editions:** 2025, 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 1,549,765
- **Coordinate reference system:** EPSG:4258 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.18 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/es_ex.py))
- **Data survey:** [ES-EX.md](https://github.com/fiboa/data-survey/blob/main/data/ES-EX.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/es_ex/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es_ex/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2025 | 1,550,714 | [838.8 MB](https://data.source.coop/ftw/harmonized-field-data/es_ex/year=2025/es_ex-2025.parquet) | — | [es_ex-2025.json](https://data.source.coop/ftw/harmonized-field-data/es_ex/year=2025/es_ex-2025.json) |
| 2026 | 1,549,765 | [839.8 MB](https://data.source.coop/ftw/harmonized-field-data/es_ex/year=2026/es_ex-2026.parquet) | [339.2 MB](https://data.source.coop/ftw/harmonized-field-data/es_ex/year=2026/es_ex-2026.pmtiles) | [es_ex-2026.json](https://data.source.coop/ftw/harmonized-field-data/es_ex/year=2026/es_ex-2026.json) |

The latest edition is also available at a stable path: [es_ex/latest/es_ex.parquet](https://data.source.coop/ftw/harmonized-field-data/es_ex/latest/es_ex.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/es_ex/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es_ex/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

Extremadura's own portal (sitex.gobex.es) has not answered since 2026-09-10, so these editions come from FEGA's national release of the same register, provinces 06 (Badajoz) and 10 (Cáceres).

## Columns

| Column | Type | Description |
|---|---|---|
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `admin_municipality_code` | string | Adminstrative subdivision municipality ID (source column `municipio`, per the fiboa data survey) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `admin_province_code` | string | Adminstrative subdivision Province ID (source column `provincia`, per the fiboa data survey) |
| `crop:name_en` | string | Crop name in English. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `ES`
- `crop:code_list`: `https://fiboa.org/code/es/sigpac/land_use.csv`
- `admin:subdivision_code`: `EX`
- `determination:datetime`: `2026-01-01T00:00:00Z`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/es_ex/latest/es_ex.parquet');
-- fields | hectares
-- 1549765 | 3230661.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Fondo Español de Garantía Agraria (FEGA)](https://www.fega.gob.es) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.18:

- 2025: converted 2026-09-16 from <https://sigpac-hubcloud.es/geopackages/2025/recintos/06_BADAJOZ_rec_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/recintos/10_CACERES_rec_2025_20250110_gpkg.zip>
- 2026: converted 2026-09-16 from <https://sigpac-hubcloud.es/geopackages/2026/recintos/06_BADAJOZ_rec_2026_20251215_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2026/recintos/10_CACERES_rec_2026_20251215_gpkg.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: ©FEGA / Ministerio de Agricultura, Pesca y Alimentación
