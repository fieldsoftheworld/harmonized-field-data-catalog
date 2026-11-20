# Agent guidance — Finnish Crop Fields (Maatalousmaa)

Finland field boundaries in the [fiboa](https://github.com/fiboa/specification) schema, 6 editions (2020, 2021, 2022, 2023, 2024, 2025). Every claim below is quoted from the source, the converter, or measured from the published files; each query was run before it was written down, and its output follows it as comments.

## Access

- Latest edition, stable path: `https://data.source.coop/ftw/harmonized-field-data/fi/latest/fi.parquet`
- One edition: `https://data.source.coop/ftw/harmonized-field-data/fi/year=<year>/<file>.parquet`, e.g. `https://data.source.coop/ftw/harmonized-field-data/fi/year=2025/fi-2025.parquet`
- All editions (hive partitioned): `s3://ftw/harmonized-field-data/fi/year=*/*.parquet` — the S3 form of the same prefix through the Source Cooperative proxy, because `*` needs a listing that plain https does not provide. In DuckDB: `CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');` then `read_parquet(glob, hive_partitioning = true)` adds the `year` column. No credentials are needed.
- PMTiles for maps: `https://data.source.coop/ftw/harmonized-field-data/fi/year=2025/fi-2025.pmtiles`, layer `fi`; MapLibre styles in `styles/`.

## Quirks that produce silently wrong answers

- **CRS is EPSG:3067, not WGS84.** `ST_Area`/`ST_Distance` return units of that CRS; transform with `ST_Transform` if you need lon/lat, or use `metrics:area`.
- **`metrics:area` is in square metres** (source column `area`; where the source value is missing or 0 the converter computed it from the geometry, in EPSG:6933 when the CRS is not metric). Divide by 10 000 for hectares.
- **`year` is the year the boundaries represent**: the declaration year or season of a register, the year a snapshot was taken, or (for a source covering several years) the year of each field's own `determination:datetime`. `determination:datetime`, where present, is the source's own date for a field.
- **`id` is only guaranteed unique within one edition** (fiboa requires uniqueness per file; it is assigned by the converter). Whether an id persists across editions is not verified here; do not join editions on it without checking.
- **`hcat:code` is hierarchical.** The first 4/6/8 digits are increasingly specific crop groups; compare prefixes, not equality, to aggregate (see the crop query below). Source crops without a mapping in the converter's HCAT table (`None`) have `NULL`. 258 of the 985,483 rows of the 2025 edition (0.03%) have none, so a query that filters or groups on crop silently leaves them out.
- **Some fiboa properties are not columns.** Values constant for the whole file are stored once in the GeoParquet `collection` key-value metadata: `determination:datetime` = `2025-01-01T00:00:00Z`, `admin:country_code` = `FI`, `crop:code_list` = `https://fiboa.org/code/fi/fi_2023.csv` (2025 edition). Read them with `parquet_kv_metadata()` in DuckDB or `pyarrow.parquet.ParquetFile(f).schema_arrow.metadata[b'collection']`; they differ per edition where the source does.

## Tested queries

Fields and hectares per edition, through the partition glob:

```sql
INSTALL httpfs; LOAD httpfs;
CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');
SELECT year, count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('s3://ftw/harmonized-field-data/fi/year=*/*.parquet', hive_partitioning = true)
GROUP BY year ORDER BY year;
-- year | fields | hectares
-- 2020 | 1088750 | 2331882.0
-- 2021 | 1086365 | 2330619.0
-- 2022 | 1086995 | 2329463.0
-- 2023 | 1006584 | 2312738.0
-- 2024 | 998336 | 2301982.0
-- 2025 | 985483 | 2292367.0
```

Largest crop groups in the latest edition (HCAT level 3 = first 6 digits):

```sql
SELECT substr(CAST("hcat:code" AS VARCHAR), 1, 6) AS hcat_group, mode("hcat:name") AS most_common_name,
       count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/fi/latest/fi.parquet')
WHERE "hcat:code" IS NOT NULL
GROUP BY 1 ORDER BY hectares DESC LIMIT 5;
-- hcat_group | most_common_name | fields | hectares
-- 330101 | barley | 313477 | 998535.0
-- 330109 | temporary_grass | 456043 | 895408.0
-- 339900 | not_known_and_other | 61620 | 100931.0
-- 330106 | spring_rapeseed_rape | 27073 | 86198.0
-- 330111 | fallow_land_not_crop | 55370 | 79481.0
```

Fields within 500 m of a point given in lon/lat, transforming the point into the data's CRS instead of the data into WGS84:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT id, round("metrics:area") AS m2
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/fi/latest/fi.parquet')
WHERE ST_Intersects(geometry, ST_Buffer(ST_Transform(ST_Point(25.3640, 64.9529), 'EPSG:4326', 'EPSG:3067', always_xy := true), 500))
LIMIT 5;
-- id | m2
-- 5670009001:1 | 29592.0
-- 5670033047:1 | 65666.0
-- 5670034259:1 | 13864.0
-- 5670052750:1 | 10906.0
-- 5670070635:2 | 1216.0
```

## Related collections

Every collection in this catalog shares the fiboa core columns, so the same queries work across countries; `s3://ftw/harmonized-field-data/*/latest/*.parquet` with `union_by_name = true` reads the newest edition of all of them (see the catalog [AGENTS.md](https://source.coop/ftw/harmonized-field-data/AGENTS.md)).

## Structure

Assets and structural links resolve relative to the object that carries them; there is no `self` link. Source: this collection is generated by [tools/catalogize.py](https://github.com/fieldsoftheworld/harmonized-field-data-catalog/blob/main/tools/catalogize.py) in the catalog repository — fix documentation there.
