# Italy Tuscany (ITI1) Crop Fields — EuroCropsV2

EuroCropsV2 harmonised Geo-Spatial Application (GSA) declarations for Tuscany (NUTS-2: ITI1), Italy. Produced by
the JRC, EUROSTAT and Technical University of Munich from the Italian paying agency's parcel-level crop
declarations.

The source is distributed as one GeoParquet per year (2016-2023) in EPSG:3035 (LAEA Europe). HCAT3 names and
codes are joined in from the EuroCropsV2 NUTS mapping table at conversion time.

- **Source data provider:** [Joint Research Centre, European Commission](https://data.jrc.ec.europa.eu/dataset/b9fb9e67-78a9-4327-9d59-39a928d812d3)
- **License:** CC-BY-4.0
- **Editions:** 2023 (one GeoParquet per year)
- **Fields in the latest edition (2023):** 623,666
- **Coordinate reference system:** EPSG:3035 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/it_1.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/it_1/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/it_1/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2023 | 623,666 | [182.7 MB](https://data.source.coop/ftw/harmonized-field-data/it_1/year=2023/it_1-2023.parquet) | [64.4 MB](https://data.source.coop/ftw/harmonized-field-data/it_1/year=2023/it_1-2023.pmtiles) | [it_1-2023.json](https://data.source.coop/ftw/harmonized-field-data/it_1/year=2023/it_1-2023.json) |

The latest edition is also available at a stable path: [it_1/latest/it_1.parquet](https://data.source.coop/ftw/harmonized-field-data/it_1/latest/it_1.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/it_1/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/it_1/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `IT`
- `admin:subdivision_code`: `1`
- `crop:code_list`: `https://fiboa.org/code/it/iti1.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/it_1/latest/it_1.parquet');
-- fields | hectares
-- 623666 | 725013.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Joint Research Centre, European Commission](https://data.jrc.ec.europa.eu/dataset/b9fb9e67-78a9-4327-9d59-39a928d812d3) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2023: converted 2026-08-22 from <https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/DRLL/EuroCropsV2/gpqtv201/iti1_2023.parquet>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: European Commission, Joint Research Centre — EuroCropsV2
