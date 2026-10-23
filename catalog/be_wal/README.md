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
- **License:** CC-BY-4.0
- **Editions:** 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 (one GeoParquet per year)
- **Fields in the latest edition (2023):** 342,315
- **Coordinate reference system:** EPSG:3035 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.4.0 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/be_wal.py))
- **Data survey:** [BE-WAL.md](https://github.com/fiboa/data-survey/blob/main/data/BE-WAL.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/be_wal/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/be_wal/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2015 | 338,208 | [95.9 MB](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2015/be_wal-2015.parquet) | — | [be_wal-2015.json](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2015/be_wal-2015.json) |
| 2016 | 338,341 | [96.5 MB](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2016/be_wal-2016.parquet) | — | [be_wal-2016.json](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2016/be_wal-2016.json) |
| 2017 | 341,654 | [98.6 MB](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2017/be_wal-2017.parquet) | — | [be_wal-2017.json](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2017/be_wal-2017.json) |
| 2018 | 344,053 | [99.5 MB](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2018/be_wal-2018.parquet) | — | [be_wal-2018.json](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2018/be_wal-2018.json) |
| 2019 | 340,899 | [99.6 MB](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2019/be_wal-2019.parquet) | — | [be_wal-2019.json](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2019/be_wal-2019.json) |
| 2020 | 343,118 | [101.4 MB](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2020/be_wal-2020.parquet) | — | [be_wal-2020.json](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2020/be_wal-2020.json) |
| 2021 | 339,536 | [102.4 MB](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2021/be_wal-2021.parquet) | — | [be_wal-2021.json](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2021/be_wal-2021.json) |
| 2022 | 341,968 | [104.5 MB](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2022/be_wal-2022.parquet) | — | [be_wal-2022.json](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2022/be_wal-2022.json) |
| 2023 | 342,315 | [106.0 MB](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2023/be_wal-2023.parquet) | [27.2 MB](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2023/be_wal-2023.pmtiles) | [be_wal-2023.json](https://data.source.coop/ftw/harmonized-field-data/be_wal/year=2023/be_wal-2023.json) |

The latest edition is also available at a stable path: [be_wal/latest/be_wal.parquet](https://data.source.coop/ftw/harmonized-field-data/be_wal/latest/be_wal.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/be_wal/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/be_wal/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

The 2015, 2016, 2017, 2018, 2019, 2020, 2021 and 2023 editions, which the source above does not offer, come from Belgium Wallonia: Parcellaire Agricole Anonyme — EuroCrops V2 (Joint Research Centre, European Commission, converter `ec_be_wal`), under CC-BY-4.0; attribution: European Commission, Joint Research Centre — EuroCropsV2; their items carry those terms.

## Columns

| Column | Type | Description |
|---|---|---|
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `BE`
- `determination:datetime`: `2023-01-01T00:00:00Z`
- `crop:code_list`: `https://raw.githubusercontent.com/maja601/EuroCrops/refs/heads/main/csvs/country_mappings/be_wal_all_years.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/be_wal/latest/be_wal.parquet');
-- fields | hectares
-- 342315 | 799405.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Inspire Geoportal of the European Commission](https://inspire-geoportal.ec.europa.eu/srv/eng/catalog.search#/metadata/2a0d9be0-ac3d-443e-9db0-a7cfb0f128e2) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.4.0:

- 2015: converted 2026-10-15 from <https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/DRLL/EuroCropsV2/gpqtv202/be3_2015.parquet>
- 2016: converted 2026-10-15 from <https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/DRLL/EuroCropsV2/gpqtv202/be3_2016.parquet>
- 2017: converted 2026-10-15 from <https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/DRLL/EuroCropsV2/gpqtv202/be3_2017.parquet>
- 2018: converted 2026-10-15 from <https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/DRLL/EuroCropsV2/gpqtv202/be3_2018.parquet>
- 2019: converted 2026-10-15 from <https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/DRLL/EuroCropsV2/gpqtv202/be3_2019.parquet>
- 2020: converted 2026-10-15 from <https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/DRLL/EuroCropsV2/gpqtv202/be3_2020.parquet>
- 2021: converted 2026-10-15 from <https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/DRLL/EuroCropsV2/gpqtv202/be3_2021.parquet>
- 2022: converted 2026-10-12 from <https://geoservices.wallonie.be/geotraitement/spwdatadownload/get/2a0d9be0-ac3d-443e-9db0-a7cfb0f128e2/LU_ExistingLandUse_SIGEC2022.gml.zip?blocksize=0>
- 2023: converted 2026-10-15 from <https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/DRLL/EuroCropsV2/gpqtv202/be3_2023.parquet>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribute the data to Inspire Geoportal of the European Commission. The 2015, 2016, 2017, 2018, 2019, 2020, 2021 and 2023 editions, which the source above does not offer, come from Belgium Wallonia: Parcellaire Agricole Anonyme — EuroCrops V2 (Joint Research Centre, European Commission, converter `ec_be_wal`), under CC-BY-4.0; attribution: European Commission, Joint Research Centre — EuroCropsV2; their items carry those terms.
