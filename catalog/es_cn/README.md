# Spain Crop fields of Canary Islands

The Canary Islands Crop Map is a cartographic dataset developed by the Department of Agriculture, Livestock,
Fisheries and Water of the Government of the Canary Islands, to understand the reality of the available
agricultural surface of the Canary Islands. This tool has been developed from 1998 to the present.

There are several crop maps for each of the islands, which allow us to see the temporal and spatial evolution
of the cultivated areas of the islands in recent years. All this means that the Canary Islands Crop Map is a
basic tool for decision-making in present and future regional agricultural policy, as well as being a basic
source for the preservation of agricultural land in the field of territorial planning.

The data of the Canary Islands Crop Map have been published on the open data portal of
the Government of the Canary Islands (https://datos.canarias.es/catalogos/general/dataset/mapa-de-cultivos-de-canarias)
and in datos gob (https://datos.gob.es/es/catalogo/a05003638-mapa-de-cultivos-de-canarias1),
this work having been addressed within the Strategic Plan for Innovation and Continuous Improvement
of the Ministry of Agriculture, Livestock and Fisheries.

- **Source data provider:** [Gobierno de Canarias - Consejería de Agricultura, Ganadería, Pesca y Soberanía Alimentaria](https://www.gobiernodecanarias.org/agpsa/)
- **License:** CC-BY-4.0
- **Editions:** 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 461,729
- **Coordinate reference system:** EPSG:32628 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/es_cn.py))
- **Data survey:** [ES-CN.md](https://github.com/fiboa/data-survey/blob/main/data/ES-CN.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/es_cn/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es_cn/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2026 | 461,729 | [111.8 MB](https://data.source.coop/ftw/harmonized-field-data/es_cn/year=2026/es_cn.parquet) | [45.0 MB](https://data.source.coop/ftw/harmonized-field-data/es_cn/year=2026/es_cn.pmtiles) | [es_cn-2026.json](https://data.source.coop/ftw/harmonized-field-data/es_cn/year=2026/es_cn-2026.json) |

The latest edition is also available at a stable path: [es_cn/latest/es_cn.parquet](https://data.source.coop/ftw/harmonized-field-data/es_cn/latest/es_cn.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/es_cn/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es_cn/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `admin_island` | string | Island name (source column `ISLA_NA`, per the fiboa data survey) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `determination:datetime` | timestamp[ms, tz=UTC] | The last timestamp at which the field did exist and was observed. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `ES`
- `admin:subdivision_code`: `CB`
- `crop:code_list`: `https://fiboa.org/code/es/cn/crop.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/es_cn/latest/es_cn.parquet');
-- fields | hectares
-- 461729 | 123162.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Gobierno de Canarias - Consejería de Agricultura, Ganadería, Pesca y Soberanía Alimentaria](https://www.gobiernodecanarias.org/agpsa/) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2026: converted 2026-08-22 from <https://opendata.sitcan.es/upload/medio-rural/gobcan_mapa-cultivos_lz_shp.zip>, <https://opendata.sitcan.es/upload/medio-rural/gobcan_mapa-cultivos_eh_shp.zip>, <https://opendata.sitcan.es/upload/medio-rural/gobcan_mapa-cultivos_lp_shp.zip>, <https://opendata.sitcan.es/upload/medio-rural/gobcan_mapa-cultivos_lg_shp.zip>, <https://opendata.sitcan.es/upload/medio-rural/gobcan_mapa-cultivos_tf_shp.zip>, <https://opendata.sitcan.es/upload/medio-rural/gobcan_mapa-cultivos_gc_shp.zip>, <https://opendata.sitcan.es/upload/medio-rural/gobcan_mapa-cultivos_fv_shp.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: Gobierno de Canarias
