# Belgium Wallonia: Parcellaire Agricole Anonyme

The Crop Fields (PAA) covers land use in agricultural and forestry areas managed as part of the implementation of the
Common Agricultural Policy by the Paying Agency of Wallonia.

The PAA represents the public version of the agricultural plot. It therefore does not include personal information
allowing the operator to be identified. It is provided on an annual basis. Data from a year of cultivation are made
available to the public during the following year.

The data is distributed in two ways: either at the source of the paying agency (more attributes
but no public distribution) or at the European Commission data portal (no limitations). We use the
free-licensed version for this converter.

- **Source data provider:** [Inspire Geoportal of the European Commission](https://inspire-geoportal.ec.europa.eu/srv/eng/catalog.search#/metadata/2a0d9be0-ac3d-443e-9db0-a7cfb0f128e2)
- **License:** other — [No conditions apply to access and use. Distributed through Inspire guidelines](https://inspire-geoportal.ec.europa.eu/srv/eng/catalog.search#/metadata/2a0d9be0-ac3d-443e-9db0-a7cfb0f128e2) (converter: `No conditions apply to access and use. Distributed through Inspire guidelines <https://inspire-geoportal.ec.europa.eu/srv/eng/catalog.search#/metadata/2a0d9be0-ac3d-443e-9db0-a7cfb0f128e2>`)
- **Editions:** 2022 (one GeoParquet per year)
- **Fields in the latest edition (2022):** 341,968
- **Coordinate reference system:** EPSG:3035 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/be_wal.py))
- **Data survey:** [BE-WAL.md](https://github.com/fiboa/data-survey/blob/main/data/BE-WAL.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/be_wal/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/be_wal/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2022 | 341,968 | [102.6 MB](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2022/be_wal.parquet) | [24.2 MB](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2022/be_wal.pmtiles) | [be_wal-2022.json](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2022/be_wal-2022.json) |

The latest edition is also available at a stable path: [be_wal/latest/be_wal.parquet](https://data.source.coop/ftw/harmonized-field-data/be_wal/latest/be_wal.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/be_wal/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/be_wal/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2022-01-01T00:00:00Z`
- `admin:country_code`: `BE`
- `crop:code_list`: `https://raw.githubusercontent.com/maja601/EuroCrops/refs/heads/main/csvs/country_mappings/be_wal_all_years.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/be_wal/latest/be_wal.parquet');
-- fields
-- 341968
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Inspire Geoportal of the European Commission](https://inspire-geoportal.ec.europa.eu/srv/eng/catalog.search#/metadata/2a0d9be0-ac3d-443e-9db0-a7cfb0f128e2) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2022: converted 2026-08-22 from <https://geoservices.wallonie.be/geotraitement/spwdatadownload/get/2a0d9be0-ac3d-443e-9db0-a7cfb0f128e2/LU_ExistingLandUse_SIGEC2022.gml.zip?blocksize=0>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

other — [No conditions apply to access and use. Distributed through Inspire guidelines](https://inspire-geoportal.ec.europa.eu/srv/eng/catalog.search#/metadata/2a0d9be0-ac3d-443e-9db0-a7cfb0f128e2) (converter: `No conditions apply to access and use. Distributed through Inspire guidelines <https://inspire-geoportal.ec.europa.eu/srv/eng/catalog.search#/metadata/2a0d9be0-ac3d-443e-9db0-a7cfb0f128e2>`). Attribute the data to Inspire Geoportal of the European Commission.
