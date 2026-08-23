# Spain Castilla-La Mancha Crop fields

SIGPAC is a Geographic Information System dedicated to the control of agricultural aid under
the CAP (Common Agricultural Policy). This tool is mandatory for the management of community aid, and is
the identification basis for any type of aid related to the surface area.

- **Source data provider:** [Unidad de Cartografía. Secretaría General. Consejería de Agricultura, Ganadería y Desarrollo Rural.](https://datosabiertos.castillalamancha.es)
- **License:** CC-BY-SA-4.0
- **Editions:** 2024 (one GeoParquet per year)
- **Fields in the latest edition (2024):** 6,453,236
- **Coordinate reference system:** EPSG:4326 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/es_cm.py))
- **Data survey:** [ES-CM.md](https://github.com/fiboa/data-survey/blob/main/data/ES-CM.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/es_cm/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es_cm/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2024 | 6,453,236 | [2.3 GB](https://data.source.coop/ftw/harmonized-field-data/es_cm/year=2024/es_cm-2024.parquet) | [952.8 MB](https://data.source.coop/ftw/harmonized-field-data/es_cm/year=2024/es_cm-2024.pmtiles) | [es_cm-2024.json](https://data.source.coop/ftw/harmonized-field-data/es_cm/year=2024/es_cm-2024.json) |

The latest edition is also available at a stable path: [es_cm/latest/es_cm.parquet](https://data.source.coop/ftw/harmonized-field-data/es_cm/latest/es_cm.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/es_cm/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es_cm/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name_en` | string | Crop name in English. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `admin_municipality_code` | string | Carried over from the source column `MUNICIPIO`; the publisher documents no meaning for it. |
| `admin_province_code` | string | Carried over from the source column `PROVINCIA`; the publisher documents no meaning for it. |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `ES`
- `crop:code_list`: `https://fiboa.org/code/es/sigpac/land_use.csv`
- `admin:subdivision_code`: `CM`
- `determination:datetime`: `2024-01-01T00:00:00Z`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/es_cm/latest/es_cm.parquet');
-- fields | hectares
-- 6453236 | 6328598.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Unidad de Cartografía. Secretaría General. Consejería de Agricultura, Ganadería y Desarrollo Rural.](https://datosabiertos.castillalamancha.es) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2024: converted 2026-08-23 from <REST>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-SA-4.0. Attribution: Unidad de Cartografía. Secretaría General. Consejería de Agricultura, Ganadería y Desarrollo Rural.
