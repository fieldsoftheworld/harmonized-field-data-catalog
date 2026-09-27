# Field blocks for Saxony-Anhalt, Germany

The field blocks ("Feldblöcke") of Saxony-Anhalt, the reference parcels of its Land Parcel
Identification System (LPIS). The data is derived from the InVeKoS records and transformed into the
INSPIRE "Land Cover" data model, so each field block carries a land cover class from the national
IACS code list alongside its FLIK. The landscape elements ("Landschaftselemente"), which the same
service publishes as a second layer, are not included. No area is published, so it is computed from
the geometry.

- **Source data provider:** [Ministerium für Wirtschaft, Tourismus, Landwirtschaft und Forsten (MWL) Sachsen-Anhalt](https://mwl.sachsen-anhalt.de)
- **License:** DL-DE-BY-2.0
- **Editions:** 2021, 2022, 2023 (one GeoParquet per year)
- **Fields in the latest edition (2023):** 78,714
- **Coordinate reference system:** EPSG:4326 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.3.1 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/de_st.py))
- **Data survey:** [DE-ST.md](https://github.com/fiboa/data-survey/blob/main/data/DE-ST.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/de_st/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_st/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2021 | 78,722 | [73.6 MB](https://data.source.coop/ftw/harmonized-field-data/de_st/year=2021/de_st-2021.parquet) | — | [de_st-2021.json](https://data.source.coop/ftw/harmonized-field-data/de_st/year=2021/de_st-2021.json) |
| 2022 | 78,689 | [74.3 MB](https://data.source.coop/ftw/harmonized-field-data/de_st/year=2022/de_st-2022.parquet) | — | [de_st-2022.json](https://data.source.coop/ftw/harmonized-field-data/de_st/year=2022/de_st-2022.json) |
| 2023 | 78,714 | [74.5 MB](https://data.source.coop/ftw/harmonized-field-data/de_st/year=2023/de_st-2023.parquet) | [25.7 MB](https://data.source.coop/ftw/harmonized-field-data/de_st/year=2023/de_st-2023.pmtiles) | [de_st-2023.json](https://data.source.coop/ftw/harmonized-field-data/de_st/year=2023/de_st-2023.json) |

The latest edition is also available at a stable path: [de_st/latest/de_st.parquet](https://data.source.coop/ftw/harmonized-field-data/de_st/latest/de_st.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/de_st/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_st/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `determination:datetime` | timestamp[ms, tz=UTC] | The last timestamp at which the field did exist and was observed. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name_en` | string | Crop name in English. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `flik` | string | The area identifier (FLIK code) is a 16-character string. ([spec](https://github.com/fiboa/flik-extension/blob/main/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `DE`
- `admin:subdivision_code`: `ST`
- `crop:code_list`: `https://fiboa.org/code/de/iacs/agricultural_area_type.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/de_st/latest/de_st.parquet');
-- fields | hectares
-- 78714 | 1201875.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Ministerium für Wirtschaft, Tourismus, Landwirtschaft und Forsten (MWL) Sachsen-Anhalt](https://mwl.sachsen-anhalt.de) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.3.1:

- 2021: converted 2026-09-27 from <REST>
- 2022: converted 2026-09-27 from <REST>
- 2023: converted 2026-09-27 from <REST>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

DL-DE-BY-2.0. Attribution: © Ministerium für Wirtschaft, Tourismus, Landwirtschaft und Forsten des Landes Sachsen-Anhalt, dl-de/by-2-0
