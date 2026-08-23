# Field boundaries for Romania - Eurocrops

The dataset includes the land cover layer from the Romanian side of the Romania-Bulgaria cross-border area (Mehedinți, Dolj, Olt, Teleorman, Giurgiu, Călărași, Constanța counties), developed within the project "Common strategy for territorial development of the cross-border area Romania-Bulgaria", code MIS-ETC 171, funded by the Romania-Bulgaria Cross-Border Cooperation Programme 2007-2013.

The dataset is published in the WGS 84 / UTM zone 35N coordinate system (to be compatible with the similar dataset on the Bulgarian side).

The dataset is in line with the conceptual framework described in the Land Cover Data Specifications for the Implementation of the INSPIRE Directive (version 3.0). The information layer was developed based on a methodology developed within the project, which was carried out as follows: - analysis and harmonisation of the land cover classification system; - acquisition and processing of the reference data, listed below; - verification and validation of the quality of the spatial data produced;

- **Source data provider:** [Ministry of Regional Development and Public Administration <http://spatial.mdrap.ro>, EuroCrops](https://github.com/maja601/EuroCrops)
- **License:** CC-BY-SA-4.0
- **Editions:** 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 259,862
- **Coordinate reference system:** EPSG:32635 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ec_ro.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/ec_ro/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ec_ro/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2026 | 259,862 | [90.5 MB](https://data.source.coop/ftw/harmonized-field-data/ec_ro/year=2026/ec_ro.parquet) | [41.3 MB](https://data.source.coop/ftw/harmonized-field-data/ec_ro/year=2026/ec_ro.pmtiles) | [ec_ro-2026.json](https://data.source.coop/ftw/harmonized-field-data/ec_ro/year=2026/ec_ro-2026.json) |

The latest edition is also available at a stable path: [ec_ro/latest/ec_ro.parquet](https://data.source.coop/ftw/harmonized-field-data/ec_ro/latest/ec_ro.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/ec_ro/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ec_ro/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `source` | string | Carried over from the source column `SOURCE`; the publisher documents no meaning for it. |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2017-01-01T00:00:00Z`
- `crop:code_list`: `https://raw.githubusercontent.com/maja601/EuroCrops/refs/heads/main/csvs/country_mappings/ro_no_year.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/ec_ro/latest/ec_ro.parquet');
-- fields | hectares
-- 259862 | 5722521.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Ministry of Regional Development and Public Administration <http://spatial.mdrap.ro>, EuroCrops](https://github.com/maja601/EuroCrops) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2026: converted 2026-08-22 from <https://zenodo.org/records/14094196/files/RO_ny.zip?download=1>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-SA-4.0. Attribute the data to Ministry of Regional Development and Public Administration <http://spatial.mdrap.ro>, EuroCrops.
