# Field boundaries for Berlin / Brandenburg, Germany

A Crop Field (German: "Schlaege") is a contiguous agricultural area surrounded by permanent boundaries, which is cultivated with a single crop.

- **Source data provider:** [Land Brandenburg](https://geobroker.geobasis-bb.de/gbss.php?MODE=GetProductInformation&PRODUCTID=9e95f21f-4ecf-4682-9a44-e5f7609f6fa0)
- **License:** DL-DE-BY-2.0
- **Editions:** 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 290,688
- **Coordinate reference system:** EPSG:25833 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/de_bb.py))
- **Data survey:** [DE-BB.md](https://github.com/fiboa/data-survey/blob/main/data/DE-BB.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/de_bb/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_bb/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2026 | 290,688 | [101.7 MB](https://data.source.coop/ftw/harmonized-field-data/de_bb/year=2026/de_bb.parquet) | [48.8 MB](https://data.source.coop/ftw/harmonized-field-data/de_bb/year=2026/de_bb.pmtiles) | [de_bb-2026.json](https://data.source.coop/ftw/harmonized-field-data/de_bb/year=2026/de_bb-2026.json) |

The latest edition is also available at a stable path: [de_bb/latest/de_bb.parquet](https://data.source.coop/ftw/harmonized-field-data/de_bb/latest/de_bb.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/de_bb/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_bb/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `farmer_id` | string | Carried over from the source column `ref_ident`; the publisher documents no meaning for it. |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `determination:datetime` | timestamp[ms, tz=UTC] | The last timestamp at which the field did exist and was observed. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `DE`
- `admin:subdivision_code`: `BB`
- `crop:code_list`: `https://raw.githubusercontent.com/maja601/EuroCrops/refs/heads/main/csvs/country_mappings/de.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/de_bb/latest/de_bb.parquet');
-- fields | hectares
-- 290688 | 1355920.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Land Brandenburg](https://geobroker.geobasis-bb.de/gbss.php?MODE=GetProductInformation&PRODUCTID=9e95f21f-4ecf-4682-9a44-e5f7609f6fa0) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2026: converted 2026-08-22 from <https://data.geobasis-bb.de/geofachdaten/Landwirtschaft/antrag.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

DL-DE-BY-2.0. Attribute the data to Land Brandenburg.
