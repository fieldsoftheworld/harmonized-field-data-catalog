# Field boundaries for Switzerland

The agricultural usage areas of Switzerland ("Nutzungsflächen", federal model 153.1) are the plots whose use each canton records as the basis for direct payments. Every canton publishes its own data under its own terms; geodienste.ch distributes them as one GeoPackage per canton in the shared model, current state only. Three cantons keep earlier years on their own portals: [Zürich](https://github.com/fiboa/data-survey/blob/main/data/CH-ZH.md) (2017–2025), [Geneva](https://github.com/fiboa/data-survey/blob/main/data/CH-GE.md) (2017–2026) and [Schwyz](https://github.com/fiboa/data-survey/blob/main/data/CH-SZ.md) (2022–2024).

- **Sources:** 20, each converted by its own fiboa-cli converter and published under its own terms (see [Sources](#sources))
- **License:** other — per source, carried by each item (see [License](#license))
- **Editions:** 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 (40 files, one per source and year)
- **Fields in the newest edition of every source:** 1,520,805
- **Coordinate reference system:** EPSG:2056 (as published by the sources; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.3.1
- **Data survey:** [CH.md](https://github.com/fiboa/data-survey/blob/main/data/CH.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/ch/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ch/AGENTS.md) for tested queries.

## Sources

| Source | Converter | Editions | Fields (newest) | License | Source data provider |
|---|---|---|---:|---|---|
| Switzerland, Aargau | [`ch_ag`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_ag.py) | 2025 | 97,527 | CC-BY-4.0 | [Kanton Aargau, via geodienste.ch](https://www.geodienste.ch/services/lwb_nutzungsflaechen) |
| Switzerland, Appenzell Innerrhoden | [`ch_ai`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_ai.py) | 2025 | 6,972 | CC-BY-4.0 | [Kanton Appenzell Innerrhoden, via geodienste.ch](https://www.geodienste.ch/services/lwb_nutzungsflaechen) |
| Switzerland, Appenzell Ausserrhoden | [`ch_ar`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_ar.py) | 2025 | 18,125 | CC0-1.0 | [Kanton Appenzell Ausserrhoden, via geodienste.ch](https://www.geodienste.ch/services/lwb_nutzungsflaechen) |
| Switzerland, Bern | [`ch_be`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_be.py) | 2025 | 241,573 | CC-BY-4.0 | [Kanton Bern, via geodienste.ch](https://www.geodienste.ch/services/lwb_nutzungsflaechen) |
| Switzerland, Basel-Landschaft | [`ch_bl`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_bl.py) | 2025 | 29,488 | CC-BY-4.0 | [Kanton Basel-Landschaft, via geodienste.ch](https://www.geodienste.ch/services/lwb_nutzungsflaechen) |
| Switzerland, Fribourg | [`ch_fr`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_fr.py) | 2025 | 69,430 | CC-BY-4.0 | [Kanton Fribourg, via geodienste.ch](https://www.geodienste.ch/services/lwb_nutzungsflaechen) |
| Switzerland, Geneva | [`ch_ge`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_ge.py) | 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 | 10,201 | CC-BY-4.0 | [État de Genève, Office cantonal de l'agriculture et de la nature](https://ge.ch/sitg/) |
| Switzerland, Glarus | [`ch_gl`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_gl.py) | 2026 | 13,878 | CC0-1.0 | [Kanton Glarus, via geodienste.ch](https://www.geodienste.ch/services/lwb_nutzungsflaechen) |
| Switzerland, Graubünden | [`ch_gr`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_gr.py) | 2026 | 175,057 | other — [Nutzungsbestimmungen für Geodaten](https://geo.gr.ch/geodaten/nutzungsbedingungen) | [Kanton Graubünden, via geodienste.ch](https://www.geodienste.ch/services/lwb_nutzungsflaechen) |
| Switzerland, Jura | [`ch_ju`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_ju.py) | 2025 | 28,203 | CC-BY-4.0 | [Kanton Jura, via geodienste.ch](https://www.geodienste.ch/services/lwb_nutzungsflaechen) |
| Switzerland, Luzern | [`ch_lu`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_lu.py) | 2025 | 99,839 | CC-BY-4.0 | [Kanton Luzern, via geodienste.ch](https://www.geodienste.ch/services/lwb_nutzungsflaechen) |
| Switzerland, St. Gallen | [`ch_sg`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_sg.py) | 2025 | 105,091 | other — [Nutzungsbedingungen für Geodaten](https://www.sg.ch/bauen/geoinformation/datenbezug/agb.html) | [Kanton St. Gallen, via geodienste.ch](https://www.geodienste.ch/services/lwb_nutzungsflaechen) |
| Switzerland, Schaffhausen | [`ch_sh`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_sh.py) | 2025 | 22,228 | CC0-1.0 | [Kanton Schaffhausen, via geodienste.ch](https://www.geodienste.ch/services/lwb_nutzungsflaechen) |
| Switzerland, Solothurn | [`ch_so`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_so.py) | 2025 | 36,731 | CC0-1.0 | [Kanton Solothurn, via geodienste.ch](https://www.geodienste.ch/services/lwb_nutzungsflaechen) |
| Switzerland, Schwyz | [`ch_sz`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_sz.py) | 2022, 2023, 2024, 2025 | 30,451 | CC-BY-4.0 | [Kanton Schwyz, Amt für Landwirtschaft](https://www.sz.ch/landwirtschaft) |
| Switzerland, Thurgau | [`ch_tg`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_tg.py) | 2025 | 57,780 | CC-BY-4.0 | [Kanton Thurgau, via geodienste.ch](https://www.geodienste.ch/services/lwb_nutzungsflaechen) |
| Switzerland, Uri | [`ch_ur`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_ur.py) | 2025 | 11,551 | CC-BY-4.0 | [Kanton Uri, via geodienste.ch](https://www.geodienste.ch/services/lwb_nutzungsflaechen) |
| Switzerland, Valais | [`ch_vs`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_vs.py) | 2025 | 307,027 | CC-BY-4.0 | [Kanton Valais, via geodienste.ch](https://www.geodienste.ch/services/lwb_nutzungsflaechen) |
| Switzerland, Zug | [`ch_zg`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_zg.py) | 2025 | 13,318 | CC-BY-4.0 | [Kanton Zug, via geodienste.ch](https://www.geodienste.ch/services/lwb_nutzungsflaechen) |
| Switzerland, Zürich | [`ch_zh`](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ch_zh.py) | 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025 | 146,335 | CC0-1.0 | [Kanton Zürich, Amt für Landschaft und Natur](https://www.zh.ch/de/umwelt-tiere/landwirtschaft.html) |

- **Switzerland, Geneva:** The current year (2026) is provisional until December.

## Files

| Year | Source | Fields | GeoParquet | STAC item |
|---|---|---:|---|---|
| 2017 | Switzerland, Geneva | 9,519 | [2.3 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2017/ch_ge-2017.parquet) | [ch_ge-2017.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2017/ch_ge-2017.json) |
| 2017 | Switzerland, Zürich | 11,777 | [5.7 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2017/ch_zh-2017.parquet) | [ch_zh-2017.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2017/ch_zh-2017.json) |
| 2018 | Switzerland, Geneva | 9,695 | [2.3 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2018/ch_ge-2018.parquet) | [ch_ge-2018.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2018/ch_ge-2018.json) |
| 2018 | Switzerland, Zürich | 63,987 | [23.2 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2018/ch_zh-2018.parquet) | [ch_zh-2018.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2018/ch_zh-2018.json) |
| 2019 | Switzerland, Geneva | 9,619 | [2.1 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2019/ch_ge-2019.parquet) | [ch_ge-2019.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2019/ch_ge-2019.json) |
| 2019 | Switzerland, Zürich | 101,690 | [33.5 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2019/ch_zh-2019.parquet) | [ch_zh-2019.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2019/ch_zh-2019.json) |
| 2020 | Switzerland, Geneva | 9,732 | [2.2 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2020/ch_ge-2020.parquet) | [ch_ge-2020.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2020/ch_ge-2020.json) |
| 2020 | Switzerland, Zürich | 106,152 | [26.9 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2020/ch_zh-2020.parquet) | [ch_zh-2020.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2020/ch_zh-2020.json) |
| 2021 | Switzerland, Geneva | 9,678 | [2.2 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2021/ch_ge-2021.parquet) | [ch_ge-2021.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2021/ch_ge-2021.json) |
| 2021 | Switzerland, Zürich | 127,717 | [31.6 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2021/ch_zh-2021.parquet) | [ch_zh-2021.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2021/ch_zh-2021.json) |
| 2022 | Switzerland, Geneva | 9,810 | [2.2 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2022/ch_ge-2022.parquet) | [ch_ge-2022.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2022/ch_ge-2022.json) |
| 2022 | Switzerland, Schwyz | 31,007 | [13.2 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2022/ch_sz-2022.parquet) | [ch_sz-2022.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2022/ch_sz-2022.json) |
| 2022 | Switzerland, Zürich | 140,229 | [39.5 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2022/ch_zh-2022.parquet) | [ch_zh-2022.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2022/ch_zh-2022.json) |
| 2023 | Switzerland, Geneva | 9,992 | [2.2 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2023/ch_ge-2023.parquet) | [ch_ge-2023.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2023/ch_ge-2023.json) |
| 2023 | Switzerland, Schwyz | 31,910 | [11.2 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2023/ch_sz-2023.parquet) | [ch_sz-2023.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2023/ch_sz-2023.json) |
| 2023 | Switzerland, Zürich | 143,016 | [39.8 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2023/ch_zh-2023.parquet) | [ch_zh-2023.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2023/ch_zh-2023.json) |
| 2024 | Switzerland, Geneva | 10,097 | [2.2 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2024/ch_ge-2024.parquet) | [ch_ge-2024.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2024/ch_ge-2024.json) |
| 2024 | Switzerland, Schwyz | 32,209 | [11.2 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2024/ch_sz-2024.parquet) | [ch_sz-2024.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2024/ch_sz-2024.json) |
| 2024 | Switzerland, Zürich | 145,437 | [40.3 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2024/ch_zh-2024.parquet) | [ch_zh-2024.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2024/ch_zh-2024.json) |
| 2025 | Switzerland, Aargau | 97,527 | [17.8 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_ag-2025.parquet) | [ch_ag-2025.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_ag-2025.json) |
| 2025 | Switzerland, Appenzell Innerrhoden | 6,972 | [5.6 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_ai-2025.parquet) | [ch_ai-2025.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_ai-2025.json) |
| 2025 | Switzerland, Appenzell Ausserrhoden | 18,125 | [5.9 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_ar-2025.parquet) | [ch_ar-2025.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_ar-2025.json) |
| 2025 | Switzerland, Bern | 241,573 | [47.3 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_be-2025.parquet) | [ch_be-2025.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_be-2025.json) |
| 2025 | Switzerland, Basel-Landschaft | 29,488 | [6.9 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_bl-2025.parquet) | [ch_bl-2025.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_bl-2025.json) |
| 2025 | Switzerland, Fribourg | 69,430 | [13.8 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_fr-2025.parquet) | [ch_fr-2025.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_fr-2025.json) |
| 2025 | Switzerland, Geneva | 10,013 | [2.2 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_ge-2025.parquet) | [ch_ge-2025.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_ge-2025.json) |
| 2025 | Switzerland, Jura | 28,203 | [8.0 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_ju-2025.parquet) | [ch_ju-2025.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_ju-2025.json) |
| 2025 | Switzerland, Luzern | 99,839 | [34.9 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_lu-2025.parquet) | [ch_lu-2025.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_lu-2025.json) |
| 2025 | Switzerland, St. Gallen | 105,091 | [53.0 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_sg-2025.parquet) | [ch_sg-2025.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_sg-2025.json) |
| 2025 | Switzerland, Schaffhausen | 22,228 | [4.2 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_sh-2025.parquet) | [ch_sh-2025.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_sh-2025.json) |
| 2025 | Switzerland, Solothurn | 36,731 | [8.1 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_so-2025.parquet) | [ch_so-2025.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_so-2025.json) |
| 2025 | Switzerland, Schwyz | 30,451 | [10.8 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_sz-2025.parquet) | [ch_sz-2025.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_sz-2025.json) |
| 2025 | Switzerland, Thurgau | 57,780 | [14.1 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_tg-2025.parquet) | [ch_tg-2025.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_tg-2025.json) |
| 2025 | Switzerland, Uri | 11,551 | [11.0 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_ur-2025.parquet) | [ch_ur-2025.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_ur-2025.json) |
| 2025 | Switzerland, Valais | 307,027 | [39.3 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_vs-2025.parquet) | [ch_vs-2025.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_vs-2025.json) |
| 2025 | Switzerland, Zug | 13,318 | [7.1 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_zg-2025.parquet) | [ch_zg-2025.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_zg-2025.json) |
| 2025 | Switzerland, Zürich | 146,335 | [39.3 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_zh-2025.parquet) | [ch_zh-2025.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_zh-2025.json) |
| 2026 | Switzerland, Geneva | 10,201 | [2.3 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2026/ch_ge-2026.parquet) | [ch_ge-2026.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2026/ch_ge-2026.json) |
| 2026 | Switzerland, Glarus | 13,878 | [4.6 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2026/ch_gl-2026.parquet) | [ch_gl-2026.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2026/ch_gl-2026.json) |
| 2026 | Switzerland, Graubünden | 175,057 | [44.3 MB](https://data.source.coop/ftw/harmonized-field-data/ch/year=2026/ch_gr-2026.parquet) | [ch_gr-2026.json](https://data.source.coop/ftw/harmonized-field-data/ch/year=2026/ch_gr-2026.json) |

The newest edition of every source is also at a stable path, `ch/latest/<converter>.parquet` (e.g. [ch_ag.parquet](https://data.source.coop/ftw/harmonized-field-data/ch/latest/ch_ag.parquet)), and tiled together in [ch/latest/ch.pmtiles](https://data.source.coop/ftw/harmonized-field-data/ch/latest/ch.pmtiles). `s3://ftw/harmonized-field-data/ch/latest/*.parquet` reads the newest editions together, `s3://ftw/harmonized-field-data/ch/year=*/*.parquet` every edition (S3 globs; see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ch/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

A value that is the same for every field of a file is stored once, in the file's GeoParquet `collection` metadata, rather than as a column; that is why the sources' files do not all have the same columns.

## Access

Query the published files in place with DuckDB; nothing needs downloading first. Fields per source in their newest editions:

```sql
INSTALL spatial; LOAD spatial;
INSTALL httpfs; LOAD httpfs;
CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');
SELECT regexp_extract(filename, '([^/]+)\.parquet$', 1) AS source, count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('s3://ftw/harmonized-field-data/ch/latest/*.parquet', union_by_name = true, filename = true)
GROUP BY 1 ORDER BY 1;
-- source | fields | hectares
-- ch_ag | 97527 | 61408.0
-- ch_ai | 6972 | 9523.0
-- ch_ar | 18125 | 13657.0
-- ch_be | 241573 | 336919.0
-- ch_bl | 29488 | 22233.0
-- ch_fr | 69430 | 97038.0
-- ch_ge | 10201 | 11601.0
-- ch_gl | 13878 | 19841.0
-- ... 12 more rows
```

## Provenance

This catalog is a mirror: the data is produced and licensed by the sources listed above and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from its source and converted with fiboa-cli 0.21.0, vecorel-cli 0.3.1:

- 2017, Switzerland, Geneva: converted 2026-09-28 from <https://ge.ch/sitg/geodata/SITG/OPENDATA/AGR_SURFACE_AGRICOLE_RECENSEE-SHP.zip>
- 2017, Switzerland, Zürich: converted 2026-09-28 from <https://maps.zh.ch/wfs/OGDZHWFS?service=WFS&version=2.0.0&request=GetFeature&typeNames=ms%3Aogd-0170_giszhpub_lw_nutzungsflaechen_2017_f&count=1000000&startIndex=0>
- 2018, Switzerland, Geneva: converted 2026-09-28 from <https://ge.ch/sitg/geodata/SITG/OPENDATA/AGR_SURFACE_AGRICOLE_RECENSEE-SHP.zip>
- 2018, Switzerland, Zürich: converted 2026-09-28 from <https://maps.zh.ch/wfs/OGDZHWFS?service=WFS&version=2.0.0&request=GetFeature&typeNames=ms%3Aogd-0170_giszhpub_lw_nutzungsflaechen_2018_f&count=1000000&startIndex=0>
- 2019, Switzerland, Geneva: converted 2026-09-28 from <https://ge.ch/sitg/geodata/SITG/OPENDATA/AGR_SURFACE_AGRICOLE_RECENSEE-SHP.zip>
- 2019, Switzerland, Zürich: converted 2026-09-28 from <https://maps.zh.ch/wfs/OGDZHWFS?service=WFS&version=2.0.0&request=GetFeature&typeNames=ms%3Aogd-0170_giszhpub_lw_nutzungsflaechen_2019_f&count=1000000&startIndex=0>
- 2020, Switzerland, Geneva: converted 2026-09-28 from <https://ge.ch/sitg/geodata/SITG/OPENDATA/AGR_SURFACE_AGRICOLE_RECENSEE-SHP.zip>
- 2020, Switzerland, Zürich: converted 2026-09-28 from <https://maps.zh.ch/wfs/OGDZHWFS?service=WFS&version=2.0.0&request=GetFeature&typeNames=ms%3Aogd-0170_giszhpub_lw_nutzungsflaechen_2020_f&count=1000000&startIndex=0>
- 2021, Switzerland, Geneva: converted 2026-09-28 from <https://ge.ch/sitg/geodata/SITG/OPENDATA/AGR_SURFACE_AGRICOLE_RECENSEE-SHP.zip>
- 2021, Switzerland, Zürich: converted 2026-09-28 from <https://maps.zh.ch/wfs/OGDZHWFS?service=WFS&version=2.0.0&request=GetFeature&typeNames=ms%3Aogd-0170_giszhpub_lw_nutzungsflaechen_2021_f&count=1000000&startIndex=0>
- 2022, Switzerland, Geneva: converted 2026-09-28 from <https://ge.ch/sitg/geodata/SITG/OPENDATA/AGR_SURFACE_AGRICOLE_RECENSEE-SHP.zip>
- 2022, Switzerland, Schwyz: converted 2026-09-28 from <https://map.geo.sz.ch/mapserv_proxy?service=WFS&version=2.0.0&request=GetFeature&typeNames=ms%3Ach.sz.a002a.nutzung.2022&sortBy=nutzungsid&count=20000&startIndex=0>, <https://map.geo.sz.ch/mapserv_proxy?service=WFS&version=2.0.0&request=GetFeature&typeNames=ms%3Ach.sz.a002a.nutzung.2022&sortBy=nutzungsid&count=20000&startIndex=20000>
- 2022, Switzerland, Zürich: converted 2026-09-28 from <https://maps.zh.ch/wfs/OGDZHWFS?service=WFS&version=2.0.0&request=GetFeature&typeNames=ms%3Aogd-0170_giszhpub_lw_nutzungsflaechen_2022_f&count=1000000&startIndex=0>
- 2023, Switzerland, Geneva: converted 2026-09-28 from <https://ge.ch/sitg/geodata/SITG/OPENDATA/AGR_SURFACE_AGRICOLE_RECENSEE-SHP.zip>
- 2023, Switzerland, Schwyz: converted 2026-09-28 from <https://map.geo.sz.ch/mapserv_proxy?service=WFS&version=2.0.0&request=GetFeature&typeNames=ms%3Ach.sz.a002a.nutzung.2023&sortBy=nutzungsid&count=20000&startIndex=0>, <https://map.geo.sz.ch/mapserv_proxy?service=WFS&version=2.0.0&request=GetFeature&typeNames=ms%3Ach.sz.a002a.nutzung.2023&sortBy=nutzungsid&count=20000&startIndex=20000>
- 2023, Switzerland, Zürich: converted 2026-09-28 from <https://maps.zh.ch/wfs/OGDZHWFS?service=WFS&version=2.0.0&request=GetFeature&typeNames=ms%3Aogd-0170_giszhpub_lw_nutzungsflaechen_2023_f&count=1000000&startIndex=0>
- 2024, Switzerland, Geneva: converted 2026-09-28 from <https://ge.ch/sitg/geodata/SITG/OPENDATA/AGR_SURFACE_AGRICOLE_RECENSEE-SHP.zip>
- 2024, Switzerland, Schwyz: converted 2026-09-28 from <https://map.geo.sz.ch/mapserv_proxy?service=WFS&version=2.0.0&request=GetFeature&typeNames=ms%3Ach.sz.a002a.nutzung.2024&sortBy=nutzungsid&count=20000&startIndex=0>, <https://map.geo.sz.ch/mapserv_proxy?service=WFS&version=2.0.0&request=GetFeature&typeNames=ms%3Ach.sz.a002a.nutzung.2024&sortBy=nutzungsid&count=20000&startIndex=20000>
- 2024, Switzerland, Zürich: converted 2026-09-28 from <https://maps.zh.ch/wfs/OGDZHWFS?service=WFS&version=2.0.0&request=GetFeature&typeNames=ms%3Aogd-0170_giszhpub_lw_nutzungsflaechen_2024_f&count=1000000&startIndex=0>
- 2025, Switzerland, Aargau: converted 2026-09-28 from <https://www.geodienste.ch/downloads/geopackage/lwb_nutzungsflaechen/AG/deu/lwb_nutzungsflaechen_v2_0_AG_gpkg_lv95.zip>
- 2025, Switzerland, Appenzell Innerrhoden: converted 2026-09-28 from <https://www.geodienste.ch/downloads/geopackage/lwb_nutzungsflaechen/AI/deu/lwb_nutzungsflaechen_v3_0_AI_gpkg_lv95.zip>
- 2025, Switzerland, Appenzell Ausserrhoden: converted 2026-09-28 from <https://www.geodienste.ch/downloads/geopackage/lwb_nutzungsflaechen/AR/deu/lwb_nutzungsflaechen_v2_0_AR_gpkg_lv95.zip>
- 2025, Switzerland, Bern: converted 2026-09-28 from <https://www.geodienste.ch/downloads/geopackage/lwb_nutzungsflaechen/BE/deu/lwb_nutzungsflaechen_v3_0_BE_gpkg_lv95.zip>
- 2025, Switzerland, Basel-Landschaft: converted 2026-09-28 from <https://www.geodienste.ch/downloads/geopackage/lwb_nutzungsflaechen/BL/deu/lwb_nutzungsflaechen_v3_0_BL_gpkg_lv95.zip>
- 2025, Switzerland, Fribourg: converted 2026-09-28 from <https://www.geodienste.ch/downloads/geopackage/lwb_nutzungsflaechen/FR/deu/lwb_nutzungsflaechen_v3_0_FR_gpkg_lv95.zip>
- 2025, Switzerland, Geneva: converted 2026-09-28 from <https://ge.ch/sitg/geodata/SITG/OPENDATA/AGR_SURFACE_AGRICOLE_RECENSEE-SHP.zip>
- 2025, Switzerland, Jura: converted 2026-09-28 from <https://www.geodienste.ch/downloads/geopackage/lwb_nutzungsflaechen/JU/deu/lwb_nutzungsflaechen_v3_0_JU_gpkg_lv95.zip>
- 2025, Switzerland, Luzern: converted 2026-09-28 from <https://www.geodienste.ch/downloads/geopackage/lwb_nutzungsflaechen/LU/deu/lwb_nutzungsflaechen_v3_0_LU_gpkg_lv95.zip>
- 2025, Switzerland, St. Gallen: converted 2026-09-28 from <https://www.geodienste.ch/downloads/geopackage/lwb_nutzungsflaechen/SG/deu/lwb_nutzungsflaechen_v2_0_SG_gpkg_lv95.zip>
- 2025, Switzerland, Schaffhausen: converted 2026-09-28 from <https://www.geodienste.ch/downloads/geopackage/lwb_nutzungsflaechen/SH/deu/lwb_nutzungsflaechen_v3_0_SH_gpkg_lv95.zip>
- 2025, Switzerland, Solothurn: converted 2026-09-28 from <https://www.geodienste.ch/downloads/geopackage/lwb_nutzungsflaechen/SO/deu/lwb_nutzungsflaechen_v3_0_SO_gpkg_lv95.zip>
- 2025, Switzerland, Schwyz: converted 2026-09-28 from <https://www.geodienste.ch/downloads/geopackage/lwb_nutzungsflaechen/SZ/deu/lwb_nutzungsflaechen_v3_0_SZ_gpkg_lv95.zip>
- 2025, Switzerland, Thurgau: converted 2026-09-28 from <https://www.geodienste.ch/downloads/geopackage/lwb_nutzungsflaechen/TG/deu/lwb_nutzungsflaechen_v3_0_TG_gpkg_lv95.zip>
- 2025, Switzerland, Uri: converted 2026-09-28 from <https://www.geodienste.ch/downloads/geopackage/lwb_nutzungsflaechen/UR/deu/lwb_nutzungsflaechen_v2_0_UR_gpkg_lv95.zip>
- 2025, Switzerland, Valais: converted 2026-09-28 from <https://www.geodienste.ch/downloads/geopackage/lwb_nutzungsflaechen/VS/deu/lwb_nutzungsflaechen_v3_0_VS_gpkg_lv95.zip>
- 2025, Switzerland, Zug: converted 2026-09-28 from <https://www.geodienste.ch/downloads/geopackage/lwb_nutzungsflaechen/ZG/deu/lwb_nutzungsflaechen_v3_0_ZG_gpkg_lv95.zip>
- 2025, Switzerland, Zürich: converted 2026-09-28 from <https://maps.zh.ch/wfs/OGDZHWFS?service=WFS&version=2.0.0&request=GetFeature&typeNames=ms%3Aogd-0170_giszhpub_lw_nutzungsflaechen_2025_f&count=1000000&startIndex=0>
- 2026, Switzerland, Geneva: converted 2026-09-28 from <https://ge.ch/sitg/geodata/SITG/OPENDATA/AGR_SURFACE_AGRICOLE_RECENSEE-SHP.zip>
- 2026, Switzerland, Glarus: converted 2026-09-28 from <https://www.geodienste.ch/downloads/geopackage/lwb_nutzungsflaechen/GL/deu/lwb_nutzungsflaechen_v3_0_GL_gpkg_lv95.zip>
- 2026, Switzerland, Graubünden: converted 2026-09-28 from <https://www.geodienste.ch/downloads/geopackage/lwb_nutzungsflaechen/GR/deu/lwb_nutzungsflaechen_v3_0_GR_gpkg_lv95.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

Each source publishes under its own terms, and the STAC item of every edition carries them (`license`, `attribution`, `providers`). The collection's license is `other`. The map tiles show all sources together and name each of them in their attribution.

- Switzerland, Aargau (`ch_ag`): CC-BY-4.0. Attribution: Daten des Kantons Aargau — Landwirtschaftliche Nutzungsflächen, https://www.geodienste.ch/services/lwb_nutzungsflaechen
- Switzerland, Appenzell Innerrhoden (`ch_ai`): CC-BY-4.0. Attribution: Grundlage/Quelle: Geodaten Kanton/Bezirke Appenzell I.Rh. — Landwirtschaftliche Nutzungsflächen, https://www.geodienste.ch/services/lwb_nutzungsflaechen
- Switzerland, Appenzell Ausserrhoden (`ch_ar`): CC0-1.0. Attribution: Kanton Appenzell Ausserrhoden — Landwirtschaftliche Nutzungsflächen, https://www.geodienste.ch/services/lwb_nutzungsflaechen
- Switzerland, Bern (`ch_be`): CC-BY-4.0. Attribution: Kanton Bern, Amt für Geoinformation — Landwirtschaftliche Nutzungsflächen, https://www.geodienste.ch/services/lwb_nutzungsflaechen
- Switzerland, Basel-Landschaft (`ch_bl`): CC-BY-4.0. Attribution: Kanton Basel-Landschaft — Landwirtschaftliche Nutzungsflächen, https://www.geodienste.ch/services/lwb_nutzungsflaechen
- Switzerland, Fribourg (`ch_fr`): CC-BY-4.0. Attribution: État de Fribourg / Kanton Freiburg — Landwirtschaftliche Nutzungsflächen, https://www.geodienste.ch/services/lwb_nutzungsflaechen
- Switzerland, Geneva (`ch_ge`): CC-BY-4.0. Attribution: Données SITG, État de Genève — Surfaces agricoles recensées, https://ge.ch/sitg/geodata/SITG/OPENDATA/AGR_SURFACE_AGRICOLE_RECENSEE-SHP.zip
- Switzerland, Glarus (`ch_gl`): CC0-1.0. Attribution: Kanton Glarus — Landwirtschaftliche Nutzungsflächen, https://www.geodienste.ch/services/lwb_nutzungsflaechen
- Switzerland, Graubünden (`ch_gr`): other — [Nutzungsbestimmungen für Geodaten](https://geo.gr.ch/geodaten/nutzungsbedingungen). Attribution: Quelle: Landwirtschaftliche Nutzungsflächen, Kanton Graubünden, https://www.geodienste.ch/services/lwb_nutzungsflaechen
- Switzerland, Jura (`ch_ju`): CC-BY-4.0. Attribution: Géodonnées de la République et Canton du Jura — Landwirtschaftliche Nutzungsflächen, https://www.geodienste.ch/services/lwb_nutzungsflaechen
- Switzerland, Luzern (`ch_lu`): CC-BY-4.0. Attribution: Kanton Luzern — Landwirtschaftliche Nutzungsflächen, https://www.geodienste.ch/services/lwb_nutzungsflaechen
- Switzerland, St. Gallen (`ch_sg`): other — [Nutzungsbedingungen für Geodaten](https://www.sg.ch/bauen/geoinformation/datenbezug/agb.html). Attribution: Kanton St.Gallen — Landwirtschaftliche Nutzungsflächen, https://www.geodienste.ch/services/lwb_nutzungsflaechen
- Switzerland, Schaffhausen (`ch_sh`): CC0-1.0. Attribution: Kanton Schaffhausen — Landwirtschaftliche Nutzungsflächen, https://www.geodienste.ch/services/lwb_nutzungsflaechen
- Switzerland, Solothurn (`ch_so`): CC0-1.0. Attribution: Kanton Solothurn — Landwirtschaftliche Nutzungsflächen, https://www.geodienste.ch/services/lwb_nutzungsflaechen
- Switzerland, Schwyz (`ch_sz`): CC-BY-4.0. Attribution: Amt für Landwirtschaft (AFL), Kanton Schwyz — Landwirtschaftliche Nutzungsflächen, https://www.geodienste.ch/services/lwb_nutzungsflaechen
- Switzerland, Thurgau (`ch_tg`): CC-BY-4.0. Attribution: Kanton Thurgau — Landwirtschaftliche Nutzungsflächen, https://www.geodienste.ch/services/lwb_nutzungsflaechen
- Switzerland, Uri (`ch_ur`): CC-BY-4.0. Attribution: Quelle: Lisag AG (GIS Uri) — Landwirtschaftliche Nutzungsflächen, https://www.geodienste.ch/services/lwb_nutzungsflaechen
- Switzerland, Valais (`ch_vs`): CC-BY-4.0. Attribution: Canton du Valais / Kanton Wallis — Landwirtschaftliche Nutzungsflächen, https://www.geodienste.ch/services/lwb_nutzungsflaechen
- Switzerland, Zug (`ch_zg`): CC-BY-4.0. Attribution: Quelle: GIS Kanton Zug — Landwirtschaftliche Nutzungsflächen, https://www.geodienste.ch/services/lwb_nutzungsflaechen
- Switzerland, Zürich (`ch_zh`): CC0-1.0. Attribution: Kanton Zürich, Amt für Landschaft und Natur — Landwirtschaftliche Kulturflächen, https://maps.zh.ch/wfs/OGDZHWFS
