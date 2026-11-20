# Agent guidance — Lithuania crop fields

Lithuania field boundaries in the [fiboa](https://github.com/fiboa/specification) schema, 2 editions (2024, 2025). Every claim below is quoted from the source, the converter, or measured from the published files; each query was run before it was written down, and its output follows it as comments.

## Access

- Latest edition, stable path: `https://data.source.coop/ftw/harmonized-field-data/lt/latest/lt.parquet`
- One edition: `https://data.source.coop/ftw/harmonized-field-data/lt/year=<year>/<file>.parquet`, e.g. `https://data.source.coop/ftw/harmonized-field-data/lt/year=2025/lt-2025.parquet`
- All editions (hive partitioned): `s3://ftw/harmonized-field-data/lt/year=*/*.parquet` — the S3 form of the same prefix through the Source Cooperative proxy, because `*` needs a listing that plain https does not provide. In DuckDB: `CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');` then `read_parquet(glob, hive_partitioning = true)` adds the `year` column. No credentials are needed.
- PMTiles for maps: `https://data.source.coop/ftw/harmonized-field-data/lt/year=2025/lt-2025.pmtiles`, layer `lt`; MapLibre styles in `styles/`.

## Quirks that produce silently wrong answers

- **CRS is EPSG:3035, not WGS84.** `ST_Area`/`ST_Distance` return units of that CRS; transform with `ST_Transform` if you need lon/lat, or use `metrics:area`.
- **`metrics:area` is in square metres** (source column `field_size`, hectares × 10 000; where the source value is missing or 0 the converter computed it from the geometry, in EPSG:6933 when the CRS is not metric). Divide by 10 000 for hectares.
- **`year` is the year the boundaries represent**: the declaration year or season of a register, the year a snapshot was taken, or (for a source covering several years) the year of each field's own `determination:datetime`. `determination:datetime`, where present, is the source's own date for a field.
- **`id` is only guaranteed unique within one edition** (fiboa requires uniqueness per file; it is the source column `field_id`). Whether an id persists across editions is not verified here; do not join editions on it without checking.
- **`hcat:code` is hierarchical.** The first 4/6/8 digits are increasingly specific crop groups; compare prefixes, not equality, to aggregate (see the crop query below). Source crops without a mapping in the converter's HCAT table (`None`) have `NULL`. All 1,156,767 rows of the 2025 edition carry one.
- **Some fiboa properties are not columns.** Values constant for the whole file are stored once in the GeoParquet `collection` key-value metadata: `determination:datetime` = `2025-01-01T00:00:00Z`, `crop:code_list` = `https://fiboa.org/code/lt/lt_2021.csv` (2025 edition). Read them with `parquet_kv_metadata()` in DuckDB or `pyarrow.parquet.ParquetFile(f).schema_arrow.metadata[b'collection']`; they differ per edition where the source does.
- The source is the Harmonized IACS inventory of Europe-LAND (Jänicke et al. 2025), which republishes the Lithuanian GSA data; the national agency NMA is the producer. Version 1.3 of the inventory is the first to carry 2025.

## Tested queries

Fields and hectares per edition, through the partition glob:

```sql
INSTALL httpfs; LOAD httpfs;
CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');
SELECT year, count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('s3://ftw/harmonized-field-data/lt/year=*/*.parquet', hive_partitioning = true)
GROUP BY year ORDER BY year;
-- year | fields | hectares
-- 2024 | 1213520 | 2912898.0
-- 2025 | 1156767 | 2915116.0
```

Largest crop groups in the latest edition (HCAT level 3 = first 6 digits):

```sql
SELECT substr(CAST("hcat:code" AS VARCHAR), 1, 6) AS hcat_group, mode("hcat:name") AS most_common_name,
       count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/lt/latest/lt.parquet')
WHERE "hcat:code" IS NOT NULL
GROUP BY 1 ORDER BY hectares DESC LIMIT 5;
-- hcat_group | most_common_name | fields | hectares
-- 330101 | winter_unspecified_cereals | 328037 | 1334571.0
-- 330200 | pasture_meadow_grassland_grass | 455270 | 781350.0
-- 330106 | rapeseed_rape | 61180 | 367204.0
-- 330102 | legumes_dried_pulses_protein_crops | 45018 | 198620.0
-- 330199 | other_arable_land_crops | 45789 | 52298.0
```

Fields within 500 m of a point given in lon/lat, transforming the point into the data's CRS instead of the data into WGS84:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT id, round("metrics:area") AS m2
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/lt/latest/lt.parquet')
WHERE ST_Intersects(geometry, ST_Buffer(ST_Transform(ST_Point(23.9379, 55.1800), 'EPSG:4326', 'EPSG:3035', always_xy := true), 500))
LIMIT 5;
-- id | m2
-- 604038 | 1157400.0
-- 78035 | 6100.0
-- 469562 | 231200.0
-- 789265 | 6900.0
```

## Related collections

Every collection in this catalog shares the fiboa core columns, so the same queries work across countries; `s3://ftw/harmonized-field-data/*/latest/*.parquet` with `union_by_name = true` reads the newest edition of all of them (see the catalog [AGENTS.md](https://source.coop/ftw/harmonized-field-data/AGENTS.md)).

## Structure

Assets and structural links resolve relative to the object that carries them; there is no `self` link. Source: this collection is generated by [tools/catalogize.py](https://github.com/fieldsoftheworld/harmonized-field-data-catalog/blob/main/tools/catalogize.py) in the catalog repository — fix documentation there.
