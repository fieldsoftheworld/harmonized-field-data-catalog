# Agent guidance — Latvia Lauki Parcels

Latvia field boundaries in the [fiboa](https://github.com/fiboa/specification) schema, 11 editions (2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025). Every claim below is quoted from the source, the converter, or measured from the published files; each query was run before it was written down, and its output follows it as comments.

## Access

- Latest edition, stable path: `https://data.source.coop/ftw/harmonized-field-data/lv/latest/lv.parquet`
- One edition: `https://data.source.coop/ftw/harmonized-field-data/lv/year=<year>/<file>.parquet`, e.g. `https://data.source.coop/ftw/harmonized-field-data/lv/year=2025/lv-2025.parquet`
- All editions (hive partitioned): `s3://ftw/harmonized-field-data/lv/year=*/*.parquet` — the S3 form of the same prefix through the Source Cooperative proxy, because `*` needs a listing that plain https does not provide. In DuckDB: `CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');` then `read_parquet(glob, hive_partitioning = true)` adds the `year` column. No credentials are needed.
- PMTiles for maps: `https://data.source.coop/ftw/harmonized-field-data/lv/year=2025/lv-2025.pmtiles`, layer `lv`; MapLibre styles in `styles/`.

## Quirks that produce silently wrong answers

- **CRS is EPSG:3059, not WGS84.** `ST_Area`/`ST_Distance` return units of that CRS; transform with `ST_Transform` if you need lon/lat, or use `metrics:area`.
- **`metrics:area` is in square metres** (source column `shape_area`; where the source value is missing or 0 the converter computed it from the geometry, in EPSG:6933 when the CRS is not metric). Divide by 10 000 for hectares.
- **`year` is the edition, not the observation date.** It is the year of the source publication (the converter variant). `determination:datetime`, where present, is the source's own date for a field.
- **`id` is only guaranteed unique within one edition** (fiboa requires uniqueness per file; it is the source column `id`). Whether an id persists across editions is not verified here; do not join editions on it without checking.
- **`hcat:code` is hierarchical.** The first 4/6/8 digits are increasingly specific crop groups; compare prefixes, not equality, to aggregate (see the crop query below). Source crops without a mapping in the converter's HCAT table (`https://fiboa.org/code/lv/lv.csv`) have `NULL`.
- **Some fiboa properties are not columns.** Values constant for the whole file are stored once in the GeoParquet `collection` key-value metadata: `determination:datetime` = `2025-01-01T00:00:00Z`, `admin:country_code` = `LV`, `crop:code_list` = `https://fiboa.org/code/lv/lv.csv` (2025 edition). Read them with `parquet_kv_metadata()` in DuckDB or `pyarrow.parquet.ParquetFile(f).schema_arrow.metadata[b'collection']`; they differ per edition where the source does.
- Published until 2026-09-15 as one edition labelled 2026, which was a snapshot of the rolling WFS rather than a campaign; these editions replace it. The yearly releases carry the crop code without a name, so crop:name is resolved through the code list. Code 619 has no HCAT mapping (3,989 fields of 2022, 0.93% of that edition): the Rural Support Service publishes no code list and the code does not appear in the WFS.

## Tested queries

Fields and hectares per edition, through the partition glob:

```sql
INSTALL httpfs; LOAD httpfs;
CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');
SELECT year, count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('s3://ftw/harmonized-field-data/lv/year=*/*.parquet', hive_partitioning = true)
GROUP BY year ORDER BY year;
-- year | fields | hectares
-- 2015 | 448209 | 1690902.0
-- 2016 | 438841 | 1714045.0
-- 2017 | 433332 | 1727757.0
-- 2018 | 440028 | 1739337.0
-- 2019 | 438838 | 1759996.0
-- 2020 | 440654 | 1778078.0
-- 2021 | 435259 | 1783596.0
-- 2022 | 429259 | 1782362.0
-- ... 3 more rows
```

Largest crop groups in the latest edition (HCAT level 3 = first 6 digits):

```sql
SELECT substr(CAST("hcat:code" AS VARCHAR), 1, 6) AS hcat_group, mode("hcat:name") AS most_common_name,
       count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/lv/latest/lv.parquet')
WHERE "hcat:code" IS NOT NULL
GROUP BY 1 ORDER BY hectares DESC LIMIT 5;
-- hcat_group | most_common_name | fields | hectares
-- 330101 | winter_common_soft_wheat | 109270 | 767919.0
-- 330200 | pasture_meadow_grassland_grass | 175144 | 483607.0
-- 330109 | poaceae_grasses | 43560 | 170677.0
-- 330106 | winter_rapeseed_rape | 16217 | 153536.0
-- 330102 | peas | 13065 | 91914.0
```

Fields around a point, transforming the point into the data's CRS instead of the data into WGS84:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT id, round("metrics:area") AS m2
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/lv/latest/lv.parquet')
WHERE ST_Intersects(geometry, ST_Buffer(ST_Transform(ST_Point(56.8381, 24.6327), 'EPSG:4326', 'EPSG:3059'), 500))
LIMIT 5;
-- id | m2
```

## Related collections

Every collection in this catalog shares the fiboa core columns, so the same queries work across countries; `s3://ftw/harmonized-field-data/*/latest/*.parquet` with `union_by_name = true` reads the newest edition of all of them (see the catalog [AGENTS.md](https://source.coop/ftw/harmonized-field-data/AGENTS.md)).

## Structure

Assets and structural links resolve relative to the object that carries them; there is no `self` link. Source: this collection is generated by [tools/catalogize.py](https://github.com/fieldsoftheworld/harmonized-field-data-catalog/blob/main/tools/catalogize.py) in the catalog repository — fix documentation there.
