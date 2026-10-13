# Italy Tuscany (ITI1) Crop Fields — EuroCropsV2

EuroCropsV2 harmonised Geo-Spatial Application (GSA) declarations for Tuscany (NUTS-2: ITI1), Italy. Produced by
the JRC, EUROSTAT and Technical University of Munich from the Italian paying agency's parcel-level crop
declarations.

The source is distributed as one GeoParquet per year (2016-2023) in EPSG:3035 (LAEA Europe). HCAT3 names and
codes are joined in from the EuroCropsV2 NUTS mapping table at conversion time.

- **Source data provider:** [Joint Research Centre, European Commission](https://data.jrc.ec.europa.eu/dataset/b9fb9e67-78a9-4327-9d59-39a928d812d3)
- **License:** CC-BY-4.0
- **Editions:** 2016, 2018, 2019, 2020, 2022 (one GeoParquet per year)
- **Fields in the latest edition (2022):** 667,107
- **Coordinate reference system:** EPSG:3035 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.4.0 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/it_1.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/it_1/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/it_1/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2016 | 685,555 | [252.3 MB](https://data.source.coop/ftw/harmonized-field-data/it_1/year=2016/it_1-2016.parquet) | — | [it_1-2016.json](https://data.source.coop/ftw/harmonized-field-data/it_1/year=2016/it_1-2016.json) |
| 2018 | 642,298 | [224.4 MB](https://data.source.coop/ftw/harmonized-field-data/it_1/year=2018/it_1-2018.parquet) | — | [it_1-2018.json](https://data.source.coop/ftw/harmonized-field-data/it_1/year=2018/it_1-2018.json) |
| 2019 | 579,075 | [181.6 MB](https://data.source.coop/ftw/harmonized-field-data/it_1/year=2019/it_1-2019.parquet) | — | [it_1-2019.json](https://data.source.coop/ftw/harmonized-field-data/it_1/year=2019/it_1-2019.json) |
| 2020 | 670,813 | [236.6 MB](https://data.source.coop/ftw/harmonized-field-data/it_1/year=2020/it_1-2020.parquet) | — | [it_1-2020.json](https://data.source.coop/ftw/harmonized-field-data/it_1/year=2020/it_1-2020.json) |
| 2022 | 667,107 | [222.8 MB](https://data.source.coop/ftw/harmonized-field-data/it_1/year=2022/it_1-2022.parquet) | [110.0 MB](https://data.source.coop/ftw/harmonized-field-data/it_1/year=2022/it_1-2022.pmtiles) | [it_1-2022.json](https://data.source.coop/ftw/harmonized-field-data/it_1/year=2022/it_1-2022.json) |

The latest edition is also available at a stable path: [it_1/latest/it_1.parquet](https://data.source.coop/ftw/harmonized-field-data/it_1/latest/it_1.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/it_1/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/it_1/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

EuroCrops V2 also has 2017, 2021 and 2023, but they repeat an earlier year (2016, 2020 and 2019): the same parcels with the same crops. They are left out.

## Columns

| Column | Type | Description |
|---|---|---|
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `IT`
- `admin:subdivision_code`: `1`
- `determination:datetime`: `2022-01-01T00:00:00Z`
- `crop:code_list`: `https://fiboa.org/code/it/iti1.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/it_1/latest/it_1.parquet');
-- fields | hectares
-- 667107 | 730995.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Joint Research Centre, European Commission](https://data.jrc.ec.europa.eu/dataset/b9fb9e67-78a9-4327-9d59-39a928d812d3) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.4.0:

- 2016: converted 2026-10-11 from <https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/DRLL/EuroCropsV2/gpqtv202/iti1_2016.parquet>
- 2018: converted 2026-10-11 from <https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/DRLL/EuroCropsV2/gpqtv202/iti1_2018.parquet>
- 2019: converted 2026-10-11 from <https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/DRLL/EuroCropsV2/gpqtv202/iti1_2019.parquet>
- 2020: converted 2026-10-11 from <https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/DRLL/EuroCropsV2/gpqtv202/iti1_2020.parquet>
- 2022: converted 2026-10-11 from <https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/DRLL/EuroCropsV2/gpqtv202/iti1_2022.parquet>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: European Commission, Joint Research Centre — EuroCropsV2
