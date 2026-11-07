# 10,000 Crop Field Boundaries across India with splits

Release of dataset and neural network weights accompanying the paper
"Unlocking large-scale crop field delineation in smallholder farming systems with transfer learning and weak supervision"
(forthcoming in Remote Sensing). Ten thousand crop fields in India were delineated manually through inspection
of high-resolution satellite imagery (Airbus SPOT). We also provide the weights of the highest performing
neural network (FracTAL ResUNet architecture) pre-trained in France and fine-tuned on Airbus SPOT images in India.
The model was trained in MXNet 1.6.0 and can be loaded with the "model.load_parameters()" function.

- **Source data provider:** [Zenodo](https://zenodo.org)
- **License:** CC-BY-4.0
- **Editions:** 2020 (one GeoParquet per year)
- **Fields in the latest edition (2020):** 10,013
- **Coordinate reference system:** EPSG:4326 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.30.0, vecorel-cli 0.4.3 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/india_10k_ml.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/in_10k_ml/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/in_10k_ml/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2020 | 10,013 | [7.6 MB](https://data.source.coop/ftw/harmonized-field-data/in_10k_ml/year=2020/in_10k_ml-2020.parquet) | [5.7 MB](https://data.source.coop/ftw/harmonized-field-data/in_10k_ml/year=2020/in_10k_ml-2020.pmtiles) | [in_10k_ml-2020.json](https://data.source.coop/ftw/harmonized-field-data/in_10k_ml/year=2020/in_10k_ml-2020.json) |

The latest edition is also available at a stable path: [in_10k_ml/latest/in_10k_ml.parquet](https://data.source.coop/ftw/harmonized-field-data/in_10k_ml/latest/in_10k_ml.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/in_10k_ml/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/in_10k_ml/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `split` | string | Source-specific column; the publisher documents no meaning for it. |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2020-10-01T00:00:00Z`
- `admin:country_code`: `IN`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/in_10k_ml/latest/in_10k_ml.parquet');
-- fields | hectares
-- 10013 | 4303.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Zenodo](https://zenodo.org) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.30.0, vecorel-cli 0.4.3:

- 2020: converted 2026-11-07 from <https://zenodo.org/api/records/7315090/files/india_10k_fields.shp/content>, <https://zenodo.org/api/records/7315090/files/india_10k_fields.shx/content>, <https://zenodo.org/api/records/7315090/files/india_10k_fields.dbf/content>, <https://zenodo.org/api/records/7315090/files/india_10k_fields.prj/content>, <https://zenodo.org/api/records/7315090/files/india_10k_fields.cpg/content>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: https://doi.org/10.5281/zenodo.7315090
