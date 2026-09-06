# Field boundaries for Estonia - Eurocrops 2021

Geospatial Aid Application Estonia Agricultural parcels.
The original dataset is provided by ARIB and obtained from the INSPIRE theme GSAA (specifically Geospaial Aid Application Estonia Agricultural parcels) through which the data layer Fields and Eco Areas (GSAA) is made available.
The data comes from ARIB's database of agricultural parcels.

- **Source data provider:** [Põllumajanduse Registrite ja Informatsiooni Amet <http://data.europa.eu/88u/dataset/pria-pollud>, EuroCrops](https://github.com/maja601/EuroCrops)
- **License:** CC-BY-SA-4.0
- **Editions:** 2021 (one GeoParquet per year)
- **Fields in the latest edition (2021):** 176,066
- **Coordinate reference system:** EPSG:4326 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.16 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ec_ee.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/ec_ee/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ec_ee/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2021 | 176,066 | [291.9 MB](https://data.source.coop/ftw/harmonized-field-data/ec_ee/year=2021/ec_ee.parquet) | [83.4 MB](https://data.source.coop/ftw/harmonized-field-data/ec_ee/year=2021/ec_ee.pmtiles) | [ec_ee-2021.json](https://data.source.coop/ftw/harmonized-field-data/ec_ee/year=2021/ec_ee-2021.json) |

The latest edition is also available at a stable path: [ec_ee/latest/ec_ee.parquet](https://data.source.coop/ftw/harmonized-field-data/ec_ee/latest/ec_ee.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/ec_ee/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ec_ee/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `viimase_muutmise_aeg` | string | Carried over from the source column `viimase_mu`; the publisher documents no meaning for it. |
| `taotleja_nimi` | string | Carried over from the source column `taotleja_n`; the publisher documents no meaning for it. |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `taotletud_toetus` | string | Carried over from the source column `taotletu_2`; the publisher documents no meaning for it. |
| `taotleja_registrikood` | string | Carried over from the source column `taotleja_r`; the publisher documents no meaning for it. |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `taotletud_maakasutus` | string | Carried over from the source column `taotletu_1`; the publisher documents no meaning for it. |
| `niitmise_tuvast_ajavahemik` | string | Carried over from the source column `niitmise_1`; the publisher documents no meaning for it. |
| `niitmise_tuvastamise_staatus` | string | Carried over from the source column `niitmise_t`; the publisher documents no meaning for it. |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2021-01-01T00:00:00Z`
- `crop:code_list`: `https://raw.githubusercontent.com/maja601/EuroCrops/refs/heads/main/csvs/country_mappings/ee_2021.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/ec_ee/latest/ec_ee.parquet');
-- fields | hectares
-- 176066 | 973955.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Põllumajanduse Registrite ja Informatsiooni Amet <http://data.europa.eu/88u/dataset/pria-pollud>, EuroCrops](https://github.com/maja601/EuroCrops) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.16:

- 2021: converted 2026-09-04 from <https://zenodo.org/records/14094196/files/EE_2021.zip?download=1>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-SA-4.0. Attribution: © Põllumajanduse Registrite ja Informatsiooni Amet
