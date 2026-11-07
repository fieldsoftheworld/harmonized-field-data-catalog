# South Africa Crop Field Boundaries (Fusion Competition) with splits

Field boundaries for South Africa from the ESA Fusion Competition dataset.
Contains crop field polygons labeled with crop type information,
covering three tiles in the Western Cape region of South Africa.

- **Source data provider:** [ESA Fusion Competition via Source Cooperative](https://source.coop/esa/fusion-competition)
- **License:** CC-BY-4.0
- **Editions:** 2017 (one GeoParquet per year)
- **Fields in the latest edition (2017):** 6,568
- **Coordinate reference system:** EPSG:4326 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.30.0, vecorel-cli 0.4.2 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/za_fusion_ml.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/za_fusion_ml/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/za_fusion_ml/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2017 | 6,568 | [2.0 MB](https://data.source.coop/ftw/harmonized-field-data/za_fusion_ml/year=2017/za_fusion_ml-2017.parquet) | [1.1 MB](https://data.source.coop/ftw/harmonized-field-data/za_fusion_ml/year=2017/za_fusion_ml-2017.pmtiles) | [za_fusion_ml-2017.json](https://data.source.coop/ftw/harmonized-field-data/za_fusion_ml/year=2017/za_fusion_ml-2017.json) |

The latest edition is also available at a stable path: [za_fusion_ml/latest/za_fusion_ml.parquet](https://data.source.coop/ftw/harmonized-field-data/za_fusion_ml/latest/za_fusion_ml.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/za_fusion_ml/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/za_fusion_ml/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `split` | string | Source-specific column; the publisher documents no meaning for it. |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2017-01-01T00:00:00Z`
- `crop:code_list`: `https://fiboa.org/code/za/fusion/crop.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/za_fusion_ml/latest/za_fusion_ml.parquet');
-- fields | hectares
-- 6568 | 90442.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [ESA Fusion Competition via Source Cooperative](https://source.coop/esa/fusion-competition) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.30.0, vecorel-cli 0.4.2:

- 2017: converted 2026-11-05 from <https://data.source.coop/esa/fusion-competition/sa-19E-258N-crop-labels-train-2017.geojson>, <https://data.source.coop/esa/fusion-competition/sa-19E-259N-crop-labels-train-2017.geojson>, <https://data.source.coop/esa/fusion-competition/sa-20E-259N-crop-labels-test-2017.geojson>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: https://data.source.coop/esa/fusion-competition
