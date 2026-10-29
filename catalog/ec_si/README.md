# Field boundaries for Slovenia - Eurocrops 2021

This dataset contains the field boundaries for all of Slovenia in 2021. The data was collected by the Slovenian government.

- **Source data provider:** [Ministrstvo za kmetijstvo, gozdarstvo in prehrano <https://rkg.gov.si/vstop/>, EuroCrops](https://github.com/maja601/EuroCrops)
- **License:** CC-BY-SA-4.0
- **Editions:** 2021 (one GeoParquet per year)
- **Fields in the latest edition (2021):** 828,157
- **Coordinate reference system:** EPSG:3794 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.4.1 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ec_si.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/ec_si/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ec_si/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2021 | 828,157 | [166.4 MB](https://data.source.coop/ftw/harmonized-field-data/ec_si/year=2021/ec_si-2021.parquet) | [139.8 MB](https://data.source.coop/ftw/harmonized-field-data/ec_si/year=2021/ec_si-2021.pmtiles) | [ec_si-2021.json](https://data.source.coop/ftw/harmonized-field-data/ec_si/year=2021/ec_si-2021.json) |

The latest edition is also available at a stable path: [ec_si/latest/ec_si.parquet](https://data.source.coop/ftw/harmonized-field-data/ec_si/latest/ec_si.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/ec_si/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ec_si/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `color` | string | Carried over from the source column `COLOR`; the publisher documents no meaning for it. |
| `crop_lat_e` | string | Carried over from the source column `CROP_LAT_E`; the publisher documents no meaning for it. |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop_type_class` | string | Carried over from the source column `SIFRA_KMRS`; the publisher documents no meaning for it. |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `rastlina` | string | Carried over from the source column `RASTLINA`; the publisher documents no meaning for it. |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `gerk_pid` | uint64 | Carried over from the source column `GERK_PID`; the publisher documents no meaning for it. |
| `EC_NUTS3` | string | Source-specific column; the publisher documents no meaning for it. |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `crop:code_list`: `https://raw.githubusercontent.com/maja601/EuroCrops/refs/heads/main/csvs/country_mappings/si_2021.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/ec_si/latest/ec_si.parquet');
-- fields | hectares
-- 828157 | 475683.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Ministrstvo za kmetijstvo, gozdarstvo in prehrano <https://rkg.gov.si/vstop/>, EuroCrops](https://github.com/maja601/EuroCrops) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.4.1:

- 2021: converted 2026-10-27 from <https://zenodo.org/records/10118572/files/SI_2021.zip?download=1>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-SA-4.0. Attribution: Ministrstvo za kmetijstvo, gozdarstvo in prehrano
