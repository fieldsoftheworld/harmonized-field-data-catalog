# Spain Cantabria Crop fields

SIGPAC Crop fields of Spain - Cantabria

- **Source data provider:** —
- **License:** CC-BY-NC-4.0
- **Editions:** 2024 (one GeoParquet per year)
- **Fields in the latest edition (2024):** 605,149
- **Coordinate reference system:** EPSG:4326 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/es_cb.py))
- **Data survey:** [ES-CB.md](https://github.com/fiboa/data-survey/blob/main/data/ES-CB.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/es_cb/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es_cb/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2024 | 605,149 | [235.0 MB](https://data.source.coop/ftw/harmonized-field-data/es_cb/year=2024/es_cb-2024.parquet) | [88.3 MB](https://data.source.coop/ftw/harmonized-field-data/es_cb/year=2024/es_cb-2024.pmtiles) | [es_cb-2024.json](https://data.source.coop/ftw/harmonized-field-data/es_cb/year=2024/es_cb-2024.json) |

The latest edition is also available at a stable path: [es_cb/latest/es_cb.parquet](https://data.source.coop/ftw/harmonized-field-data/es_cb/latest/es_cb.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/es_cb/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es_cb/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `admin_municipality_code` | string | Municipality ID (source column `MUNICIPIO`, per the fiboa data survey) |
| `crop:name_en` | string | Crop name in English. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin_province_code`: `39`
- `admin:country_code`: `ES`
- `crop:code_list`: `https://fiboa.org/code/es/sigpac/land_use.csv`
- `admin:subdivision_code`: `CB`
- `determination:datetime`: `2024-01-01T00:00:00Z`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/es_cb/latest/es_cb.parquet');
-- fields
-- 605149
```

## Provenance

This catalog is a mirror: the data is produced and licensed by — and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2024: converted 2026-08-23 from <REST>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-NC-4.0. Attribution: ©Government of Cantabria. Free information available at https://mapas.cantabria.es
