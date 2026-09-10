# Slovenia Crop Fields

The Slovenian government provides slightly different, relevant open data sets called GERK, KMRS, RABA and EKRZ.
This converter uses the KRMS dataset, which includes CAP applications of the last year and discerns
around 150 different crop categories.

- **Source data provider:** [Ministry of Agriculture, Forestry and Food (Ministrstvo za kmetijstvo, gozdarstvo in prehrano)](https://www.gov.si/drzavni-organi/ministrstva/ministrstvo-za-kmetijstvo-gozdarstvo-in-prehrano/)
- **License:** other — [Javno dostopni podatki: Publicly available data](https://rkg.gov.si/vstop/) (converter: `Javno dostopni podatki: Publicly available data <https://rkg.gov.si/vstop/>`)
- **Editions:** 2019, 2020, 2021, 2022, 2023, 2024 (one GeoParquet per year)
- **Fields in the latest edition (2024):** 809,044
- **Coordinate reference system:** EPSG:3794 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/si.py))
- **Data survey:** [SI.md](https://github.com/fiboa/data-survey/blob/main/data/SI.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/si/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/si/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2019 | 820,151 | [184.7 MB](https://data.source.coop/ftw/harmonized-field-data/si/year=2019/si-2019.parquet) | — | [si-2019.json](https://data.source.coop/ftw/harmonized-field-data/si/year=2019/si-2019.json) |
| 2020 | 819,620 | [187.3 MB](https://data.source.coop/ftw/harmonized-field-data/si/year=2020/si-2020.parquet) | — | [si-2020.json](https://data.source.coop/ftw/harmonized-field-data/si/year=2020/si-2020.json) |
| 2021 | 824,532 | [165.8 MB](https://data.source.coop/ftw/harmonized-field-data/si/year=2021/si-2021.parquet) | — | [si-2021.json](https://data.source.coop/ftw/harmonized-field-data/si/year=2021/si-2021.json) |
| 2022 | 826,354 | [174.2 MB](https://data.source.coop/ftw/harmonized-field-data/si/year=2022/si-2022.parquet) | — | [si-2022.json](https://data.source.coop/ftw/harmonized-field-data/si/year=2022/si-2022.json) |
| 2023 | 830,856 | [175.5 MB](https://data.source.coop/ftw/harmonized-field-data/si/year=2023/si-2023.parquet) | — | [si-2023.json](https://data.source.coop/ftw/harmonized-field-data/si/year=2023/si-2023.json) |
| 2024 | 809,044 | [238.7 MB](https://data.source.coop/ftw/harmonized-field-data/si/year=2024/si-2024.parquet) | [140.2 MB](https://data.source.coop/ftw/harmonized-field-data/si/year=2024/si-2024.pmtiles) | [si-2024.json](https://data.source.coop/ftw/harmonized-field-data/si/year=2024/si-2024.json) |

The latest edition is also available at a stable path: [si/latest/si.parquet](https://data.source.coop/ftw/harmonized-field-data/si/latest/si.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/si/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/si/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `crop:name` | large_string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `id` | large_string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name_en` | large_string | Crop name in English. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `block_id` | uint64 | Gerk ID (source column `GERK_PID`, per the fiboa data survey) |
| `hcat:name` | large_string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | large_binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `collection` | large_string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name_en` | large_string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:code` | large_string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `SI`
- `crop:code_list`: `https://fiboa.org/code/si/si.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/si/latest/si.parquet');
-- fields | hectares
-- 809044 | 466663.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Ministry of Agriculture, Forestry and Food (Ministrstvo za kmetijstvo, gozdarstvo in prehrano)](https://www.gov.si/drzavni-organi/ministrstva/ministrstvo-za-kmetijstvo-gozdarstvo-in-prehrano/) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2019: converted 2026-09-10 from <https://rkg.gov.si/razno/portal_analysis/KMRS_2019.rar>
- 2020: converted 2026-09-10 from <https://rkg.gov.si/razno/portal_analysis/KMRS_2020.rar>
- 2021: converted 2026-09-10 from <https://rkg.gov.si/razno/portal_analysis/KMRS_2021.rar>
- 2022: converted 2026-09-10 from <https://rkg.gov.si/razno/portal_analysis/KMRS_2022.rar>
- 2023: converted 2026-09-10 from <https://rkg.gov.si/razno/portal_analysis/KMRS_2023.rar>
- 2024: converted 2026-08-28 from <https://rkg.gov.si/razno/portal_analysis/KMRS_2024.rar>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

other — [Javno dostopni podatki: Publicly available data](https://rkg.gov.si/vstop/) (converter: `Javno dostopni podatki: Publicly available data <https://rkg.gov.si/vstop/>`). Attribute the data to Ministry of Agriculture, Forestry and Food (Ministrstvo za kmetijstvo, gozdarstvo in prehrano).
