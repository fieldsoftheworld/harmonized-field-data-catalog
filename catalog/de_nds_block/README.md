# Field boundaries for Lower Saxony / Bremen / Hamburg, Germany

A field block (German: "Feldblock") is a contiguous agricultural area surrounded by permanent boundaries, which is cultivated by one or more farmers with one or more crops, is fully or partially set aside or is fully or partially taken out of production.

- **Source data provider:** [ML/SLA Niedersachsen](https://sla.niedersachsen.de/landentwicklung/LEA/)
- **License:** DL-DE-BY-2.0
- **Editions:** 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 539,834
- **Coordinate reference system:** EPSG:25832 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.16 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/de_nds_block.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/de_nds_block/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_nds_block/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2026 | 539,834 | [168.4 MB](https://data.source.coop/ftw/harmonized-field-data/de_nds_block/year=2026/de_nds_block.parquet) | [64.8 MB](https://data.source.coop/ftw/harmonized-field-data/de_nds_block/year=2026/de_nds_block.pmtiles) | [de_nds_block-2026.json](https://data.source.coop/ftw/harmonized-field-data/de_nds_block/year=2026/de_nds_block-2026.json) |

The latest edition is also available at a stable path: [de_nds_block/latest/de_nds_block.parquet](https://data.source.coop/ftw/harmonized-field-data/de_nds_block/latest/de_nds_block.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/de_nds_block/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_nds_block/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bnk` | string | Carried over from the source column `BNK`; the publisher documents no meaning for it. |
| `flik` | string | The area identifier (FLIK code) is a 16-character string. ([spec](https://github.com/fiboa/flik-extension/blob/main/README.md)) |
| `bnk_txt` | string | Carried over from the source column `BNK_TXT`; the publisher documents no meaning for it. |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `metrics:perimeter` | float | Perimeter of the field, in meters (m). Must be > 0 and <= 125,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `ant_jahr`: `2026`
- `admin:country_code`: `DE`
- `admin:subdivision_code`: `NI`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/de_nds_block/latest/de_nds_block.parquet');
-- fields | hectares
-- 539834 | 2615085.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [ML/SLA Niedersachsen](https://sla.niedersachsen.de/landentwicklung/LEA/) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.16:

- 2026: converted 2026-09-03 from <https://sla.niedersachsen.de/mapbender_sla/download/FB_NDS.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

DL-DE-BY-2.0. Attribution: © ML/SLA Niedersachsen (2024), DL-DE-BY-2.0 (www.govdata.de/DL-DE-BY-2.0), Daten bearbeitet
