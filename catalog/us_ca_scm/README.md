# California (US) Statewide Crop Mapping

For many years, the California Department of Water Resources (DWR) has collected land use data throughout the state
and used this information to develop water use estimates for statewide and regional planning efforts, including water
use projections, water use efficiency evaluation, groundwater model development, and water transfers. The statewide
crop maps are made from remote sensing by Land IQ under contract to DWR. 2024 is provisional.

- **Source data provider:** [California Department of Water Resources](https://data.cnra.ca.gov/dataset/statewide-crop-mapping)
- **License:** CC0-1.0
- **Editions:** 2014, 2016, 2018, 2019, 2020, 2021, 2022, 2023, 2024 (one GeoParquet per year)
- **Fields in the latest edition (2024):** 447,944
- **Coordinate reference system:** EPSG:4269 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.3.1 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/us_ca_scm.py))
- **Data survey:** [US-CA-SCM.md](https://github.com/fiboa/data-survey/blob/main/data/US-CA-SCM.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/us_ca_scm/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/us_ca_scm/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2014 | 359,484 | [86.8 MB](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2014/us_ca_scm-2014.parquet) | — | [us_ca_scm-2014.json](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2014/us_ca_scm-2014.json) |
| 2016 | 388,543 | [96.1 MB](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2016/us_ca_scm-2016.parquet) | — | [us_ca_scm-2016.json](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2016/us_ca_scm-2016.json) |
| 2018 | 406,662 | [99.1 MB](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2018/us_ca_scm-2018.parquet) | — | [us_ca_scm-2018.json](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2018/us_ca_scm-2018.json) |
| 2019 | 409,513 | [130.4 MB](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2019/us_ca_scm-2019.parquet) | — | [us_ca_scm-2019.json](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2019/us_ca_scm-2019.json) |
| 2020 | 421,540 | [134.6 MB](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2020/us_ca_scm-2020.parquet) | — | [us_ca_scm-2020.json](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2020/us_ca_scm-2020.json) |
| 2021 | 425,534 | [136.1 MB](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2021/us_ca_scm-2021.parquet) | — | [us_ca_scm-2021.json](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2021/us_ca_scm-2021.json) |
| 2022 | 431,776 | [137.8 MB](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2022/us_ca_scm-2022.parquet) | — | [us_ca_scm-2022.json](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2022/us_ca_scm-2022.json) |
| 2023 | 439,642 | [139.7 MB](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2023/us_ca_scm-2023.parquet) | — | [us_ca_scm-2023.json](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2023/us_ca_scm-2023.json) |
| 2024 | 447,944 | [141.5 MB](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2024/us_ca_scm-2024.parquet) | [74.1 MB](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2024/us_ca_scm-2024.pmtiles) | [us_ca_scm-2024.json](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2024/us_ca_scm-2024.json) |

The latest edition is also available at a stable path: [us_ca_scm/latest/us_ca_scm.parquet](https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/latest/us_ca_scm.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/us_ca_scm/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/us_ca_scm/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

2024 is provisional (DWR release of 2025-12-08) until DWR publishes the final edition. The crop column differs by edition: from 2019 the source's `MAIN_CROP`; in 2016 and 2018 the main-season `CROPTYP2`; 2014 names its crops only, and `crop:code` there comes from the names' codes in 2016. 2014 and 2016 carry no identifier, so there `id` is a row number. DWR maps the whole state; its urban mask (`U`, or `****` in 2020–2022: some 1,600 to 6,800 polygons per edition covering about 2 million ha, the largest close to 590,000 ha), urban landscape (`UL2`) and riparian vegetation (`NR`) are left out, as they are not fields.

## Columns

| Column | Type | Description |
|---|---|---|
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `admin_level_2` | string | County (source column `COUNTY`, per the fiboa data survey) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2024-07-01T00:00:00Z`
- `admin:country_code`: `US`
- `admin:subdivision_code`: `CA`
- `crop:code_list`: `https://fiboa.org/code/us/ca/scm.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/latest/us_ca_scm.parquet');
-- fields | hectares
-- 447944 | 3912101.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [California Department of Water Resources](https://data.cnra.ca.gov/dataset/statewide-crop-mapping) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.3.1:

- 2014: converted 2026-10-07 from <https://data.cnra.ca.gov/dataset/6c3d65e3-35bb-49e1-a51e-49d5a2cf09a9/resource/04f89c79-59d1-4981-a3ab-853fdbc79d37/download/i15_crop_mapping_2014_gdb.zip>
- 2016: converted 2026-10-07 from <https://data.cnra.ca.gov/dataset/6c3d65e3-35bb-49e1-a51e-49d5a2cf09a9/resource/489d7ab8-f68a-45b4-8113-bb89bc4d9a9c/download/i15_crop_mapping_2016_gdb.zip>
- 2018: converted 2026-10-07 from <https://data.cnra.ca.gov/dataset/6c3d65e3-35bb-49e1-a51e-49d5a2cf09a9/resource/05dc698d-9587-453a-a494-a07beadbbe62/download/i15_crop_mapping_2018_gdb.zip>
- 2019: converted 2026-10-07 from <https://data.cnra.ca.gov/dataset/6c3d65e3-35bb-49e1-a51e-49d5a2cf09a9/resource/519a6ac2-77f5-4da6-85f3-ada74d7eddee/download/i15_crop_mapping_2019_gdb.zip>
- 2020: converted 2026-10-07 from <https://data.cnra.ca.gov/dataset/6c3d65e3-35bb-49e1-a51e-49d5a2cf09a9/resource/44c1bde8-7ac4-4582-b8de-d09264e180fb/download/i15_crop_mapping_2020-gdb.zip>
- 2021: converted 2026-10-07 from <https://data.cnra.ca.gov/dataset/6c3d65e3-35bb-49e1-a51e-49d5a2cf09a9/resource/cd1ce211-ac75-44b4-9ea4-345ce2fd0548/download/i15_crop_mapping_2021_gdb.zip>
- 2022: converted 2026-10-07 from <https://data.cnra.ca.gov/dataset/6c3d65e3-35bb-49e1-a51e-49d5a2cf09a9/resource/e41f74d2-7ff9-4871-bc95-1e9673fc53cb/download/i15_crop_mapping_2022.gdb.zip>
- 2023: converted 2026-10-07 from <https://data.cnra.ca.gov/dataset/6c3d65e3-35bb-49e1-a51e-49d5a2cf09a9/resource/4e17ca38-268e-4bf5-bbc5-09636d44ed60/download/i15_crop_mapping_2023_final.gdb.zip>
- 2024: converted 2026-10-07 from <https://data.cnra.ca.gov/dataset/6c3d65e3-35bb-49e1-a51e-49d5a2cf09a9/resource/157956a5-507e-4c6c-b161-b21361488576/download/i15_crop_mapping_2024_provisional_20251208.gdb.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC0-1.0. Attribution: California Department of Water Resources, Statewide Crop Mapping
