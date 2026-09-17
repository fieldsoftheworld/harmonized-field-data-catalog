# Agent guidance — Slovakia Agricultural Land Identification System

Slovakia field boundaries in the [fiboa](https://github.com/fiboa/specification) schema, 9 editions (2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026). Every claim below is quoted from the source, the converter, or measured from the published files; each query was run before it was written down, and its output follows it as comments.

## Access

- Latest edition, stable path: `https://data.source.coop/ftw/harmonized-field-data/sk/latest/sk.parquet`
- One edition: `https://data.source.coop/ftw/harmonized-field-data/sk/year=<year>/<file>.parquet`, e.g. `https://data.source.coop/ftw/harmonized-field-data/sk/year=2026/sk-2026.parquet`
- All editions (hive partitioned): `s3://ftw/harmonized-field-data/sk/year=*/*.parquet` — the S3 form of the same prefix through the Source Cooperative proxy, because `*` needs a listing that plain https does not provide. In DuckDB: `CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');` then `read_parquet(glob, hive_partitioning = true)` adds the `year` column. No credentials are needed.
- PMTiles for maps: `https://data.source.coop/ftw/harmonized-field-data/sk/year=2026/sk-2026.pmtiles`, layer `sk`; MapLibre styles in `styles/`.

## Quirks that produce silently wrong answers

- **CRS is EPSG:5514, not WGS84.** `ST_Area`/`ST_Distance` return units of that CRS; transform with `ST_Transform` if you need lon/lat, or use `metrics:area`.
- **`metrics:area` is in square metres**, taken from the source column `VYMERA` (hectares × 10 000). Divide by 10 000 for hectares.
- **`year` is the edition, not the observation date.** It is the year of the source publication (the converter variant). `determination:datetime`, where present, is the source's own date for a field.
- **`id` is only guaranteed unique within one edition** (fiboa requires uniqueness per file; it is the source column `id`). Whether an id persists across editions is not verified here; do not join editions on it without checking.
- **`hcat:code` is hierarchical.** The first 4/6/8 digits are increasingly specific crop groups; compare prefixes, not equality, to aggregate (see the crop query below). Source crops without a mapping in the converter's HCAT table (`https://fiboa.org/code/sk/sk.csv`) have `NULL`. 588 of the 271,807 rows of the 2026 edition (0.22%) have none, so a query that filters or groups on crop silently leaves them out.
- **Some fiboa properties are not columns.** Values constant for the whole file are stored once in the GeoParquet `collection` key-value metadata: `admin:country_code` = `SK`, `determination:datetime` = `2026-01-01T00:00:00Z`, `crop:code_list` = `https://fiboa.org/code/sk/sk.csv` (2026 edition). Read them with `parquet_kv_metadata()` in DuckDB or `pyarrow.parquet.ParquetFile(f).schema_arrow.metadata[b'collection']`; they differ per edition where the source does.
- The portal also publishes the 2016 and 2017 campaigns, but as 7-Zip archives, which the conversion pipeline cannot extract.

## Tested queries

Fields and hectares per edition, through the partition glob:

```sql
INSTALL httpfs; LOAD httpfs;
CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');
SELECT year, count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('s3://ftw/harmonized-field-data/sk/year=*/*.parquet', hive_partitioning = true)
GROUP BY year ORDER BY year;
-- year | fields | hectares
-- 2018 | 240600 | 1849445.0
-- 2019 | 247544 | 1840660.0
-- 2020 | 249393 | 1832832.0
-- 2021 | 255712 | 1824522.0
-- 2022 | 264084 | 1810145.0
-- 2023 | 275830 | 1778770.0
-- 2024 | 275049 | 1772291.0
-- 2025 | 273387 | 1778026.0
-- ... 1 more rows
```

Largest crop groups in the latest edition (HCAT level 3 = first 6 digits):

```sql
SELECT substr(CAST("hcat:code" AS VARCHAR), 1, 6) AS hcat_group, mode("hcat:name") AS most_common_name,
       count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/sk/latest/sk.parquet')
WHERE "hcat:code" IS NOT NULL
GROUP BY 1 ORDER BY hectares DESC LIMIT 5;
-- hcat_group | most_common_name | fields | hectares
-- 330101 | winter_common_soft_wheat | 63039 | 683713.0
-- 330200 | pasture_meadow_grassland_grass | 121422 | 491868.0
-- 330106 | winter_rapeseed_rape | 15506 | 241008.0
-- 330109 | plants_harvested_green | 23632 | 177442.0
-- 330111 | fallow_land_not_crop | 27730 | 59312.0
```

Fields around a point, transforming the point into the data's CRS instead of the data into WGS84:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT id, round("metrics:area") AS m2
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/sk/latest/sk.parquet')
WHERE ST_Intersects(geometry, ST_Buffer(ST_Transform(ST_Point(48.6740, 19.6250), 'EPSG:4326', 'EPSG:5514'), 500))
LIMIT 5;
-- id | m2
-- 22507 | 37900.0
-- 22504 | 9600.0
-- 22506 | 17300.0
-- 22505 | 12600.0
```

## Related collections

Every collection in this catalog shares the fiboa core columns, so the same queries work across countries; `s3://ftw/harmonized-field-data/*/latest/*.parquet` with `union_by_name = true` reads the newest edition of all of them (see the catalog [AGENTS.md](https://source.coop/ftw/harmonized-field-data/AGENTS.md)).

## Structure

Assets and structural links resolve relative to the object that carries them; there is no `self` link. Source: this collection is generated by [tools/catalogize.py](https://github.com/fieldsoftheworld/harmonized-field-data-catalog/blob/main/tools/catalogize.py) in the catalog repository — fix documentation there.
