# Spain Madrid Crop fields

SIGPAC is the Agricultural Parcel Identification System implemented throughout the European Union for the application of CAP (Common Agricultural Policy) aid to farmers and ranchers.

- **Source data provider:** [Comunidad de Madrid](https://www.comunidad.madrid)
- **License:** CC0-1.0
- **Editions:** 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 636,756
- **Coordinate reference system:** EPSG:4258 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/es_md.py))
- **Data survey:** [ES-MD.md](https://github.com/fiboa/data-survey/blob/main/data/ES-MD.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/es_md/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es_md/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2026 | 636,756 | [265.1 MB](https://data.source.coop/ftw/harmonized-field-data/es_md/year=2026/es_md.parquet) | [96.6 MB](https://data.source.coop/ftw/harmonized-field-data/es_md/year=2026/es_md.pmtiles) | [es_md-2026.json](https://data.source.coop/ftw/harmonized-field-data/es_md/year=2026/es_md-2026.json) |

The latest edition is also available at a stable path: [es_md/latest/es_md.parquet](https://data.source.coop/ftw/harmonized-field-data/es_md/latest/es_md.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/es_md/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es_md/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name_en` | string | Crop name in English. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `ES`
- `crop:code_list`: `https://fiboa.org/code/es/sigpac/land_use.csv`
- `determination:datetime`: `2024-01-01T00:00:00Z`
- `admin:subdivision_code`: `MD`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/es_md/latest/es_md.parquet');
-- fields
-- 636756
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Comunidad de Madrid](https://www.comunidad.madrid) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2026: converted 2026-08-22 from <https://idem.comunidad.madrid/recursos_cat_geo/Catalogo/recursos/UsoDelSuelo/spacm_sigpac.cm.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC0-1.0. Attribute the data to Comunidad de Madrid.
