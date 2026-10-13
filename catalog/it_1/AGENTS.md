# Agent guidance — Italy Tuscany (ITI1) Crop Fields — EuroCropsV2

Italy, Tuscany field boundaries in the [fiboa](https://github.com/fiboa/specification) schema, 5 editions (2016, 2018, 2019, 2020, 2022). Every claim below is quoted from the source, the converter, or measured from the published files; each query was run before it was written down, and its output follows it as comments.

## Access

- Latest edition, stable path: `https://data.source.coop/ftw/harmonized-field-data/it_1/latest/it_1.parquet`
- One edition: `https://data.source.coop/ftw/harmonized-field-data/it_1/year=<year>/<file>.parquet`, e.g. `https://data.source.coop/ftw/harmonized-field-data/it_1/year=2022/it_1-2022.parquet`
- All editions (hive partitioned): `s3://ftw/harmonized-field-data/it_1/year=*/*.parquet` — the S3 form of the same prefix through the Source Cooperative proxy, because `*` needs a listing that plain https does not provide. In DuckDB: `CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');` then `read_parquet(glob, hive_partitioning = true)` adds the `year` column. No credentials are needed.
- PMTiles for maps: `https://data.source.coop/ftw/harmonized-field-data/it_1/year=2022/it_1-2022.pmtiles`, layer `it_1`; MapLibre styles in `styles/`.

## Quirks that produce silently wrong answers

- **CRS is EPSG:3035, not WGS84.** `ST_Area`/`ST_Distance` return units of that CRS; transform with `ST_Transform` if you need lon/lat, or use `metrics:area`.
- **`metrics:area` is in square metres** (source column `area_ha`, hectares × 10 000; where the source value is missing or 0 the converter computed it from the geometry, in EPSG:6933 when the CRS is not metric). Divide by 10 000 for hectares.
- **`year` is the edition, not the observation date.** It is the year of the source publication (the converter variant). `determination:datetime`, where present, is the source's own date for a field.
- **`id` is only guaranteed unique within one edition** (fiboa requires uniqueness per file; it is the source column `cropfield`). Whether an id persists across editions is not verified here; do not join editions on it without checking.
- **`hcat:code` is hierarchical.** The first 4/6/8 digits are increasingly specific crop groups; compare prefixes, not equality, to aggregate (see the crop query below). Source crops without a mapping in the converter's HCAT table (`None`) have `NULL`. All 667,107 rows of the 2022 edition carry one.
- **Some fiboa properties are not columns.** Values constant for the whole file are stored once in the GeoParquet `collection` key-value metadata: `admin:country_code` = `IT`, `admin:subdivision_code` = `1`, `determination:datetime` = `2022-01-01T00:00:00Z`, `crop:code_list` = `https://fiboa.org/code/it/iti1.csv` (2022 edition). Read them with `parquet_kv_metadata()` in DuckDB or `pyarrow.parquet.ParquetFile(f).schema_arrow.metadata[b'collection']`; they differ per edition where the source does.
- EuroCrops V2 also has 2017, 2021 and 2023, but they repeat an earlier year (2016, 2020 and 2019): the same parcels with the same crops. They are left out.

## Tested queries

Fields and hectares per edition, through the partition glob:

```sql
INSTALL httpfs; LOAD httpfs;
CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');
SELECT year, count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('s3://ftw/harmonized-field-data/it_1/year=*/*.parquet', hive_partitioning = true)
GROUP BY year ORDER BY year;
-- year | fields | hectares
-- 2016 | 685555 | 694351.0
-- 2018 | 642298 | 695595.0
-- 2019 | 579075 | 722113.0
-- 2020 | 670813 | 727373.0
-- 2022 | 667107 | 730995.0
```

Largest crop groups in the latest edition (HCAT level 3 = first 6 digits):

```sql
SELECT substr(CAST("hcat:code" AS VARCHAR), 1, 6) AS hcat_group, mode("hcat:name") AS most_common_name,
       count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/it_1/latest/it_1.parquet')
WHERE "hcat:code" IS NOT NULL
GROUP BY 1 ORDER BY hectares DESC LIMIT 5;
-- hcat_group | most_common_name | fields | hectares
-- 330109 | poaceae_grasses | 72854 | 132774.0
-- 330600 | tree_wood_forest | 86675 | 122313.0
-- 330101 | durum_hard_wheat | 49257 | 115330.0
-- 330100 | arable_crops | 53313 | 73395.0
-- 330305 | olive_plantations | 120659 | 63388.0
```

Fields around a point, transforming the point into the data's CRS instead of the data into WGS84:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT id, round("metrics:area") AS m2
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/it_1/latest/it_1.parquet')
WHERE ST_Intersects(geometry, ST_Buffer(ST_Transform(ST_Point(43.3977, 11.0438), 'EPSG:4326', 'EPSG:3035'), 500))
LIMIT 5;
-- id | m2
```

## Related collections

Every collection in this catalog shares the fiboa core columns, so the same queries work across countries; `s3://ftw/harmonized-field-data/*/latest/*.parquet` with `union_by_name = true` reads the newest edition of all of them (see the catalog [AGENTS.md](https://source.coop/ftw/harmonized-field-data/AGENTS.md)).

## Structure

Assets and structural links resolve relative to the object that carries them; there is no `self` link. Source: this collection is generated by [tools/catalogize.py](https://github.com/fieldsoftheworld/harmonized-field-data-catalog/blob/main/tools/catalogize.py) in the catalog repository — fix documentation there.
