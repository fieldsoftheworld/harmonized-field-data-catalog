# Field blocks for The Netherlands

A field block (Dutch: "Referentieperceel"), formerly known as "AAN" (Agrarisch Areaal Nederland),
is a contiguous agricultural area surrounded by permanent boundaries, which is cultivated by one or
more farmers with one or more crops, is fully or partially set aside or is fully or partially
taken out of production.

The following field block types exist:

- Woods (Hout)
- Agricultural area (Landbouwgrond)
- Other (Overig)
- Water (Water)

We filter on "Agricultural area" in this converter.
For crop data, look at BasisRegistratie gewasPercelen (BRP)

- **Source data provider:** [RVO / PDOK](https://www.pdok.nl/introductie/-/article/referentiepercelen)
- **License:** CC0-1.0
- **Editions:** 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 534,786
- **Coordinate reference system:** EPSG:28992 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/nl_block.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/nl_block/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/nl_block/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2026 | 534,786 | [342.8 MB](https://data.source.coop/ftw/harmonized-field-data/nl_block/year=2026/nl_block.parquet) | [120.8 MB](https://data.source.coop/ftw/harmonized-field-data/nl_block/year=2026/nl_block.pmtiles) | [nl_block-2026.json](https://data.source.coop/ftw/harmonized-field-data/nl_block/year=2026/nl_block-2026.json) |

The latest edition is also available at a stable path: [nl_block/latest/nl_block.parquet](https://data.source.coop/ftw/harmonized-field-data/nl_block/latest/nl_block.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/nl_block/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/nl_block/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `source`: `luchtfoto`
- `determination:datetime`: `2023-06-15T00:00:00Z`
- `admin:country_code`: `NL`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/nl_block/latest/nl_block.parquet');
-- fields | hectares
-- 534786 | 1834697.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [RVO / PDOK](https://www.pdok.nl/introductie/-/article/referentiepercelen) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2026: converted 2026-08-23 from <https://service.pdok.nl/rvo/referentiepercelen/atom/downloads/referentiepercelen.gpkg>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC0-1.0. Attribute the data to RVO / PDOK.
