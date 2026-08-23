# Field boundaries for Berlin / Brandenburg, Germany

A field block (German: "Feldblock") is a contiguous agricultural area surrounded by permanent boundaries, which is cultivated by one or more farmers with one or more crops, is fully or partially set aside or is fully or partially taken out of production.

- **Source data provider:** [Land Brandenburg](https://geobroker.geobasis-bb.de/gbss.php?MODE=GetProductInformation&PRODUCTID=9e95f21f-4ecf-4682-9a44-e5f7609f6fa0)
- **License:** DL-DE-BY-2.0
- **Editions:** 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 90,764
- **Coordinate reference system:** EPSG:25833 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/de_bb_block.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/de_bb_block/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_bb_block/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2026 | 90,764 | [70.6 MB](https://data.source.coop/ftw/harmonized-field-data/de_bb_block/year=2026/de_bb_block.parquet) | [34.9 MB](https://data.source.coop/ftw/harmonized-field-data/de_bb_block/year=2026/de_bb_block.pmtiles) | [de_bb_block-2026.json](https://data.source.coop/ftw/harmonized-field-data/de_bb_block/year=2026/de_bb_block-2026.json) |

The latest edition is also available at a stable path: [de_bb_block/latest/de_bb_block.parquet](https://data.source.coop/ftw/harmonized-field-data/de_bb_block/latest/de_bb_block.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/de_bb_block/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_bb_block/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `tk10` | string | Carried over from the source column `TK10_BLATT`; the publisher documents no meaning for it. |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hbn` | string | Carried over from the source column `HBN_KAT`; the publisher documents no meaning for it. |
| `net_area` | float | Carried over from the source column `FL_NETTO`; the publisher documents no meaning for it. |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `flik` | string | The area identifier (FLIK code) is a 16-character string. ([spec](https://github.com/fiboa/flik-extension/blob/main/README.md)) |
| `kreis_nr` | uint16 | Carried over from the source column `KREIS_NR`; the publisher documents no meaning for it. |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `fgue_jahr`: `2026`
- `determination:datetime`: `2026-01-01T00:00:00Z`
- `expiry_datetime`: `2026-12-31T00:00:00Z`
- `admin:country_code`: `DE`
- `admin:subdivision_code`: `BB`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/de_bb_block/latest/de_bb_block.parquet');
-- fields | hectares
-- 90764 | 1335621.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Land Brandenburg](https://geobroker.geobasis-bb.de/gbss.php?MODE=GetProductInformation&PRODUCTID=9e95f21f-4ecf-4682-9a44-e5f7609f6fa0) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2026: converted 2026-08-22 from <https://data.geobasis-bb.de/geofachdaten/Landwirtschaft/dfbk.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

DL-DE-BY-2.0. Attribute the data to Land Brandenburg.
