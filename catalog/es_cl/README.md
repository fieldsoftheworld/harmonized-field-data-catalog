# Spain Castile and León Crop fields

Official SIGPAC land plan for the year 2024. (reference date 02-01-2024)

Source: SIGPAC (FEGA) database. The Land Consolidation Replacement Farms are included,
not updated in the SIGPAC published in the Viewer.
Data manager: Ministry of Agriculture, Fisheries and Food.
Data provided by: Department of Agriculture, Livestock and Rural Development. Regional Government of Castile and Leon.
Free use of the data is permitted, but commercial exploitation is prohibited.

- **Source data provider:** [Junta de Castilla y León](https://datos.jcyl.es/web/jcyl/set/es/sector-publico/sigpac/1284212629849)
- **License:** other — [CC-NC: Free use of the data is permitted, but commercial exploitation is prohibited](http://ftp.itacyl.es/cartografia/LICENCIA-IGCYL-NC-2012.pdf) (converter: `CC-NC: Free use of the data is permitted, but commercial exploitation is prohibited <http://ftp.itacyl.es/cartografia/LICENCIA-IGCYL-NC-2012.pdf>`)
- **Editions:** 2025 (one GeoParquet per year)
- **Fields in the latest edition (2025):** 9,109,136
- **Coordinate reference system:** EPSG:4258 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/es_cl.py))
- **Data survey:** [ES-CL.md](https://github.com/fiboa/data-survey/blob/main/data/ES-CL.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/es_cl/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es_cl/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2025 | 9,109,136 | [2.4 GB](https://data.source.coop/ftw/harmonized-field-data/es_cl/year=2025/es_cl.parquet) | [880.6 MB](https://data.source.coop/ftw/harmonized-field-data/es_cl/year=2025/es_cl.pmtiles) | [es_cl-2025.json](https://data.source.coop/ftw/harmonized-field-data/es_cl/year=2025/es_cl-2025.json) |

The latest edition is also available at a stable path: [es_cl/latest/es_cl.parquet](https://data.source.coop/ftw/harmonized-field-data/es_cl/latest/es_cl.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/es_cl/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es_cl/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `crop:name_en` | string | Crop name in English. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `ES`
- `crop:code_list`: `https://fiboa.org/code/es/sigpac/land_use.csv`
- `admin:subdivision_code`: `CL`
- `determination:datetime`: `2025-01-01T00:00:00Z`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/es_cl/latest/es_cl.parquet');
-- fields
-- 9109136
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Junta de Castilla y León](https://datos.jcyl.es/web/jcyl/set/es/sector-publico/sigpac/1284212629849) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2025: converted 2026-08-24 from <https://ftp.itacyl.es/cartografia/05_SIGPAC/2025_ETRS89/Parcelario_SIGPAC_CyL_Provincias/AVILA.zip>, <https://ftp.itacyl.es/cartografia/05_SIGPAC/2025_ETRS89/Parcelario_SIGPAC_CyL_Provincias/BURGOS.zip>, <https://ftp.itacyl.es/cartografia/05_SIGPAC/2025_ETRS89/Parcelario_SIGPAC_CyL_Provincias/LEON.zip>, <https://ftp.itacyl.es/cartografia/05_SIGPAC/2025_ETRS89/Parcelario_SIGPAC_CyL_Provincias/PALENCIA.zip>, <https://ftp.itacyl.es/cartografia/05_SIGPAC/2025_ETRS89/Parcelario_SIGPAC_CyL_Provincias/SALAMANCA.zip>, <https://ftp.itacyl.es/cartografia/05_SIGPAC/2025_ETRS89/Parcelario_SIGPAC_CyL_Provincias/SEGOVIA.zip>, <https://ftp.itacyl.es/cartografia/05_SIGPAC/2025_ETRS89/Parcelario_SIGPAC_CyL_Provincias/SORIA.zip>, <https://ftp.itacyl.es/cartografia/05_SIGPAC/2025_ETRS89/Parcelario_SIGPAC_CyL_Provincias/VALLADOLID.zip>, <https://ftp.itacyl.es/cartografia/05_SIGPAC/2025_ETRS89/Parcelario_SIGPAC_CyL_Provincias/ZAMORA.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

other — [CC-NC: Free use of the data is permitted, but commercial exploitation is prohibited](http://ftp.itacyl.es/cartografia/LICENCIA-IGCYL-NC-2012.pdf) (converter: `CC-NC: Free use of the data is permitted, but commercial exploitation is prohibited <http://ftp.itacyl.es/cartografia/LICENCIA-IGCYL-NC-2012.pdf>`). Attribute the data to Junta de Castilla y León.
