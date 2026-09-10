# Field boundaries for Flanders, Belgium

Since 2020, the Department of Agriculture and Fisheries has been publishing a more extensive set of data related to agricultural use plots (from the 2008 campaign).
From 2023, the downloadable dataset of agricultural use plots will also include the specialization given by the company (= company typology) and that is given to the plots of the company. Based on the typology, the companies are divided into 4 major specializations: arable farming, horticulture, livestock farming and mixed farms. The specialization of each company is calculated annually according to a European method and is based on the standard output of the various agricultural productions on the company. It is therefore an economic specialization and not a reflection of all agricultural production on the company.

- **Source data provider:** [Agentschap Landbouw & Zeevisserij (Government)](https://landbouwcijfers.vlaanderen.be/open-geodata-landbouwgebruikspercelen)
- **License:** other — [Licentie modellicentie-gratis-hergebruik/v1.0](https://data.vlaanderen.be/id/licentie/modellicentie-gratis-hergebruik/v1.0) (converter: `Licentie modellicentie-gratis-hergebruik/v1.0 <https://data.vlaanderen.be/id/licentie/modellicentie-gratis-hergebruik/v1.0>`)
- **Editions:** 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 597,088
- **Coordinate reference system:** EPSG:31370 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.16 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/be_vlg.py))
- **Data survey:** [BE-VLG.md](https://github.com/fiboa/data-survey/blob/main/data/BE-VLG.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/be_vlg/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/be_vlg/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2018 | 515,747 | [85.5 MB](https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2018/be_vlg-2018.parquet) | — | [be_vlg-2018.json](https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2018/be_vlg-2018.json) |
| 2019 | 521,395 | [84.7 MB](https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2019/be_vlg-2019.parquet) | — | [be_vlg-2019.json](https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2019/be_vlg-2019.json) |
| 2020 | 525,851 | [86.1 MB](https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2020/be_vlg-2020.parquet) | — | [be_vlg-2020.json](https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2020/be_vlg-2020.json) |
| 2021 | 591,899 | [91.3 MB](https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2021/be_vlg-2021.parquet) | — | [be_vlg-2021.json](https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2021/be_vlg-2021.json) |
| 2022 | 585,076 | [91.3 MB](https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2022/be_vlg-2022.parquet) | — | [be_vlg-2022.json](https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2022/be_vlg-2022.json) |
| 2023 | 588,192 | [91.3 MB](https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2023/be_vlg-2023.parquet) | — | [be_vlg-2023.json](https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2023/be_vlg-2023.json) |
| 2024 | 589,749 | [91.0 MB](https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2024/be_vlg-2024.parquet) | — | [be_vlg-2024.json](https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2024/be_vlg-2024.json) |
| 2025 | 594,732 | [93.8 MB](https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2025/be_vlg-2025.parquet) | — | [be_vlg-2025.json](https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2025/be_vlg-2025.json) |
| 2026 | 597,088 | [94.9 MB](https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2026/be_vlg-2026.parquet) | [67.6 MB](https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2026/be_vlg-2026.pmtiles) | [be_vlg-2026.json](https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2026/be_vlg-2026.json) |

The latest edition is also available at a stable path: [be_vlg/latest/be_vlg.parquet](https://data.source.coop/ftw/harmonized-field-data/be_vlg/latest/be_vlg.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/be_vlg/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/be_vlg/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `block_id` | string | Unique identification number for the field. (source column `REF_ID`, per the fiboa data survey) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `typology`: `None`
- `admin:country_code`: `BE`
- `admin:subdivision_code`: `VLG`
- `determination:datetime`: `2026-01-01T00:00:00Z`
- `crop:code_list`: `https://raw.githubusercontent.com/maja601/EuroCrops/refs/heads/main/csvs/country_mappings/be_vlg_2021.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/be_vlg/latest/be_vlg.parquet');
-- fields | hectares
-- 597088 | 671328.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Agentschap Landbouw & Zeevisserij (Government)](https://landbouwcijfers.vlaanderen.be/open-geodata-landbouwgebruikspercelen) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.16:

- 2018: converted 2026-09-10 from <https://www.landbouwvlaanderen.be/bestanden/gis/Landbouwgebruikspercelen_2018_-_Definitief_(extractie_23-03-2022)_GPKG.zip>
- 2019: converted 2026-09-10 from <https://www.landbouwvlaanderen.be/bestanden/gis/Landbouwgebruikspercelen_2019_-_Definitief_(extractie_20-03-2020)_GPKG.zip>
- 2020: converted 2026-09-10 from <https://www.landbouwvlaanderen.be/bestanden/gis/Landbouwgebruikspercelen_2020_uitgebreid_toestand_19-03-2021_GPKG.zip>
- 2021: converted 2026-09-10 from <https://www.landbouwvlaanderen.be/bestanden/gis/Landbouwgebruikspercelen_2021_-_Definitief_(extractie_15-03-2022)_GPKG.zip>
- 2022: converted 2026-09-10 from <https://www.landbouwvlaanderen.be/bestanden/gis/Landbouwgebruikspercelen_2022_-_Definitief_(extractie_26-06-2023)_GPKG.zip>
- 2023: converted 2026-09-10 from <https://www.landbouwvlaanderen.be/bestanden/gis/Landbouwgebruikspercelen_2023_-_Definitief_(extractie_28-03-2024)_GPKG.zip>
- 2024: converted 2026-09-10 from <https://www.landbouwvlaanderen.be/bestanden/gis/Landbouwgebruikspercelen_2024_-_Definitief_(extractie_27-03-2025)_GPKG.zip>
- 2025: converted 2026-09-10 from <https://www.landbouwvlaanderen.be/bestanden/gis/Landbouwgebruikspercelen_2025_-_Voorlopig_(extractie_02-06-2025)_GPKG.zip>
- 2026: converted 2026-09-10 from <https://www.landbouwvlaanderen.be/bestanden/gis/agpa_2026_2026-06-02_public.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

other — [Licentie modellicentie-gratis-hergebruik/v1.0](https://data.vlaanderen.be/id/licentie/modellicentie-gratis-hergebruik/v1.0) (converter: `Licentie modellicentie-gratis-hergebruik/v1.0 <https://data.vlaanderen.be/id/licentie/modellicentie-gratis-hergebruik/v1.0>`). Attribution: Bron: Dept. LV
