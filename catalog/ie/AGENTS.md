# Agent guidance — Ireland INSPIRE Geospatial aid application (GSAA) dataset

Ireland field boundaries in the [fiboa](https://github.com/fiboa/specification) schema, 3 editions (2022, 2023, 2024). Every claim below is quoted from the source, the converter, or measured from the published files; each query was run before it was written down, and its output follows it as comments.

## Access

- Latest edition, stable path: `https://data.source.coop/ftw/harmonized-field-data/ie/latest/ie.parquet`
- One edition: `https://data.source.coop/ftw/harmonized-field-data/ie/year=<year>/<file>.parquet`, e.g. `https://data.source.coop/ftw/harmonized-field-data/ie/year=2024/ie-2024.parquet`
- All editions (hive partitioned): `s3://ftw/harmonized-field-data/ie/year=*/*.parquet` — the S3 form of the same prefix through the Source Cooperative proxy, because `*` needs a listing that plain https does not provide. In DuckDB: `CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');` then `read_parquet(glob, hive_partitioning = true)` adds the `year` column. No credentials are needed.
- PMTiles for maps: `https://data.source.coop/ftw/harmonized-field-data/ie/year=2024/ie-2024.pmtiles`, layer `ie`; MapLibre styles in `styles/`.

## Quirks that produce silently wrong answers

- **CRS is EPSG:4258, not WGS84.** `ST_Area`/`ST_Distance` return units of that CRS; transform with `ST_Transform` if you need lon/lat, or use `metrics:area`.
- **`metrics:area` is in square metres** (source column `metrics:area`, hectares × 10 000; where the source value is missing or 0 the converter computed it from the geometry, in EPSG:6933 when the CRS is not metric). Divide by 10 000 for hectares.
- **`year` is the year the boundaries represent**: the declaration year or season of a register, the year a snapshot was taken, or (for a source covering several years) the year of each field's own `determination:datetime`. `determination:datetime`, where present, is the source's own date for a field.
- **`id` is only guaranteed unique within one edition** (fiboa requires uniqueness per file; it is the source column `gml_id`). Whether an id persists across editions is not verified here; do not join editions on it without checking.
- **`hcat:code` is hierarchical.** The first 4/6/8 digits are increasingly specific crop groups; compare prefixes, not equality, to aggregate (see the crop query below). Source crops without a mapping in the converter's HCAT table (`https://fiboa.org/code/ie/ie.csv`) have `NULL`. All 1,119,949 rows of the 2024 edition carry one.
- **Some fiboa properties are not columns.** Values constant for the whole file are stored once in the GeoParquet `collection` key-value metadata: `determination:datetime` = `2024-12-31T00:00:00Z`, `admin:country_code` = `IE`, `crop:code_list` = `https://fiboa.org/code/ie/ie.csv` (2024 edition). Read them with `parquet_kv_metadata()` in DuckDB or `pyarrow.parquet.ParquetFile(f).schema_arrow.metadata[b'collection']`; they differ per edition where the source does.
- The department's INSPIRE bucket serves GSAA_2022, GSAA_2023 and GSAA_2024; GSAA_2017 through GSAA_2021 answer 403, so the earlier campaigns EuroCrops lists are no longer downloadable there.

## Tested queries

Fields and hectares per edition, through the partition glob:

```sql
INSTALL httpfs; LOAD httpfs;
CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');
SELECT year, count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('s3://ftw/harmonized-field-data/ie/year=*/*.parquet', hive_partitioning = true)
GROUP BY year ORDER BY year;
-- year | fields | hectares
-- 2022 | 1026499 | 4616741.0
-- 2023 | 1117023 | 4966124.0
-- 2024 | 1119949 | 4946224.0
```

Largest crop groups in the latest edition (HCAT level 3 = first 6 digits):

```sql
SELECT substr(CAST("hcat:code" AS VARCHAR), 1, 6) AS hcat_group, mode("hcat:name") AS most_common_name,
       count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/ie/latest/ie.parquet')
WHERE "hcat:code" IS NOT NULL
GROUP BY 1 ORDER BY hectares DESC LIMIT 5;
-- hcat_group | most_common_name | fields | hectares
-- 330200 | pasture_meadow_grassland_grass | 1002148 | 4442415.0
-- 330101 | spring_barley | 57858 | 287068.0
-- 330109 | temporary_grass | 24186 | 78495.0
-- 330600 | tree_wood_forest | 8239 | 37507.0
-- 339900 | not_known_and_other | 11017 | 26305.0
```

Fields within about 500 m (0.005°; the CRS is in degrees) of a point given in lon/lat, transforming the point into the data's CRS instead of the data into WGS84:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT id, round("metrics:area") AS m2
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/ie/latest/ie.parquet')
WHERE ST_Intersects(geometry, ST_Buffer(ST_Transform(ST_Point(-8.2922, 53.4028), 'EPSG:4326', 'EPSG:4258', always_xy := true), 0.005))
LIMIT 5;
-- id | m2
-- id6b2ae18e-efd3-4c89-9bba-dc79f39f94bd | 93079.0
-- id70f14f2a-48eb-4ddd-ba49-6fa9b8b43616 | 252383.0
-- ida8f5fba2-fa8f-476f-a6db-53b8c0089f50 | 93653.0
-- idd34d4e94-3038-4136-907a-29eaac343f37 | 81349.0
-- idc1c84d71-2349-4bd6-9329-559cfecf92ae | 89798.0
```

## Related collections

Every collection in this catalog shares the fiboa core columns, so the same queries work across countries; `s3://ftw/harmonized-field-data/*/latest/*.parquet` with `union_by_name = true` reads the newest edition of all of them (see the catalog [AGENTS.md](https://source.coop/ftw/harmonized-field-data/AGENTS.md)).

## Structure

Assets and structural links resolve relative to the object that carries them; there is no `self` link. Source: this collection is generated by [tools/catalogize.py](https://github.com/fieldsoftheworld/harmonized-field-data-catalog/blob/main/tools/catalogize.py) in the catalog repository — fix documentation there.
