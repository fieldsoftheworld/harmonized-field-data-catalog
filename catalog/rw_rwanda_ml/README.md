# Rwanda Crop Field Boundaries with splits

Field boundaries for smallholder farms in eastern Rwanda from the NASA Harvest
Rwanda Field Boundary Competition dataset. Annotated from Planet imagery for
the 2021 growing season. The competition publishes the labels as rasters; these are the
polygons Kerner Lab (Arizona State University) converted from them for Fields of the World.

- **Source data provider:** [NASA Harvest](https://source.coop/nasa/rwanda-field-boundary-competition)
- **License:** CC-BY-4.0
- **Editions:** 2021 (one GeoParquet per year)
- **Fields in the latest edition (2021):** 1,532
- **Coordinate reference system:** EPSG:4326 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.30.0, vecorel-cli 0.4.2 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/rw_rwanda_ml.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/rw_rwanda_ml/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/rw_rwanda_ml/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2021 | 1,532 | [165.3 KB](https://data.source.coop/ftw/harmonized-field-data/rw_rwanda_ml/year=2021/rw_rwanda_ml-2021.parquet) | [146.7 KB](https://data.source.coop/ftw/harmonized-field-data/rw_rwanda_ml/year=2021/rw_rwanda_ml-2021.pmtiles) | [rw_rwanda_ml-2021.json](https://data.source.coop/ftw/harmonized-field-data/rw_rwanda_ml/year=2021/rw_rwanda_ml-2021.json) |

The latest edition is also available at a stable path: [rw_rwanda_ml/latest/rw_rwanda_ml.parquet](https://data.source.coop/ftw/harmonized-field-data/rw_rwanda_ml/latest/rw_rwanda_ml.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/rw_rwanda_ml/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/rw_rwanda_ml/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `split` | string | Source-specific column; the publisher documents no meaning for it. |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2021-08-31T00:00:00Z`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/rw_rwanda_ml/latest/rw_rwanda_ml.parquet');
-- fields | hectares
-- 1532 | 3404.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [NASA Harvest](https://source.coop/nasa/rwanda-field-boundary-competition) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.30.0, vecorel-cli 0.4.2:

- 2021: converted 2026-11-05 from <https://data.source.coop/kerner-lab/fields-of-the-world-rwanda/boundaries_rwanda_2021.parquet>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: https://doi.org/10.34911/rdnt.g580ww
