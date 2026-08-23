# Denmark Crop Fields (Marker)

The Danish Ministry of Food, Agriculture and Fisheries publishes Crop Fields (Marker) for each year.

- **Source data provider:** [Danish Agricultural Agency](https://lbst.dk/)
- **License:** CC0-1.0
- **Editions:** 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 604,198
- **Coordinate reference system:** EPSG:25832 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/dk.py))
- **Data survey:** [DK.md](https://github.com/fiboa/data-survey/blob/main/data/DK.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/dk/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/dk/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2026 | 604,198 | [313.7 MB](https://data.source.coop/ftw/harmonized-field-data/dk/year=2026/dk-2026.parquet) | [236.1 MB](https://data.source.coop/ftw/harmonized-field-data/dk/year=2026/dk-2026.pmtiles) | [dk-2026.json](https://data.source.coop/ftw/harmonized-field-data/dk/year=2026/dk-2026.json) |

The latest edition is also available at a stable path: [dk/latest/dk.parquet](https://data.source.coop/ftw/harmonized-field-data/dk/latest/dk.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/dk/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/dk/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `DK`
- `determination:datetime`: `2026-01-01T00:00:00Z`
- `crop:code_list`: `https://raw.githubusercontent.com/maja601/EuroCrops/refs/heads/main/csvs/country_mappings/dk_2019.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/dk/latest/dk.parquet');
-- fields | hectares
-- 604198 | 2649306.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Danish Agricultural Agency](https://lbst.dk/) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2026: converted 2026-08-22 from <https://landbrugsgeodata.fvm.dk/Download/Marker/Marker_2026.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC0-1.0. Attribute the data to Danish Agricultural Agency.
