# Agent guidance — LPIS parcels for Ireland

Ireland (LPIS) field boundaries in the [fiboa](https://github.com/fiboa/specification) schema, 7 editions (2017, 2018, 2019, 2020, 2021, 2022, 2025). Every claim below is quoted from the source, the converter, or measured from the published files; each query was run before it was written down, and its output follows it as comments.

## Access

- Latest edition, stable path: `https://data.source.coop/ftw/harmonized-field-data/ie_lpis/latest/ie_lpis.parquet`
- One edition: `https://data.source.coop/ftw/harmonized-field-data/ie_lpis/year=<year>/<file>.parquet`, e.g. `https://data.source.coop/ftw/harmonized-field-data/ie_lpis/year=2025/ie_lpis-2025.parquet`
- All editions (hive partitioned): `s3://ftw/harmonized-field-data/ie_lpis/year=*/*.parquet` — the S3 form of the same prefix through the Source Cooperative proxy, because `*` needs a listing that plain https does not provide. In DuckDB: `CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');` then `read_parquet(glob, hive_partitioning = true)` adds the `year` column. No credentials are needed.
- PMTiles for maps: `https://data.source.coop/ftw/harmonized-field-data/ie_lpis/year=2025/ie_lpis-2025.pmtiles`, layer `ie_lpis`; MapLibre styles in `styles/`.

## Quirks that produce silently wrong answers

- **CRS is EPSG:2157, not WGS84.** `ST_Area`/`ST_Distance` return units of that CRS; transform with `ST_Transform` if you need lon/lat, or use `metrics:area`.
- **`metrics:area` is in square metres** (source column `DIGIT_AREA`; where the source value is missing or 0 the converter computed it from the geometry, in EPSG:6933 when the CRS is not metric). Divide by 10 000 for hectares.
- **`year` is the edition, not the observation date.** It is the year of the source publication (the converter variant). `determination:datetime`, where present, is the source's own date for a field.
- **`id` is only guaranteed unique within one edition** (fiboa requires uniqueness per file; it is the source column `PARC_LAB`). Whether an id persists across editions is not verified here; do not join editions on it without checking.
- **`hcat:code` is hierarchical.** The first 4/6/8 digits are increasingly specific crop groups; compare prefixes, not equality, to aggregate (see the crop query below). Source crops without a mapping in the converter's HCAT table (`None`) have `NULL`. All 1,454,480 rows of the 2025 edition carry one.
- **Some fiboa properties are not columns.** Values constant for the whole file are stored once in the GeoParquet `collection` key-value metadata: `admin:country_code` = `IE`, `determination:datetime` = `2025-01-01T00:00:00Z`, `crop:code_list` = `https://fiboa.org/code/ie/ie.csv` (2025 edition). Read them with `parquet_kv_metadata()` in DuckDB or `pyarrow.parquet.ParquetFile(f).schema_arrow.metadata[b'collection']`; they differ per edition where the source does.

## Tested queries

Fields and hectares per edition, through the partition glob:

```sql
INSTALL httpfs; LOAD httpfs;
CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');
SELECT year, count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('s3://ftw/harmonized-field-data/ie_lpis/year=*/*.parquet', hive_partitioning = true)
GROUP BY year ORDER BY year;
-- year | fields | hectares
-- 2017 | 1310933 | 5040668.0
-- 2018 | 1308587 | 5012300.0
-- 2019 | 1306462 | 4989220.0
-- 2020 | 1311162 | 4968745.0
-- 2021 | 1309443 | 4942761.0
-- 2022 | 1421266 | 5215900.0
-- 2025 | 1454480 | 5206763.0
```

Largest crop groups in the latest edition (HCAT level 3 = first 6 digits):

```sql
SELECT substr(CAST("hcat:code" AS VARCHAR), 1, 6) AS hcat_group, mode("hcat:name") AS most_common_name,
       count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/ie_lpis/latest/ie_lpis.parquet')
WHERE "hcat:code" IS NOT NULL
GROUP BY 1 ORDER BY hectares DESC LIMIT 5;
-- hcat_group | most_common_name | fields | hectares
-- 330200 | pasture_meadow_grassland_grass | 1031693 | 4472782.0
-- 330101 | spring_barley | 59305 | 300499.0
-- 339900 | not_known_and_other | 269430 | 141466.0
-- 330600 | tree_wood_forest | 36340 | 127984.0
-- 330109 | temporary_grass | 27969 | 92497.0
```

Fields around a point, transforming the point into the data's CRS instead of the data into WGS84:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT id, round("metrics:area") AS m2
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/ie_lpis/latest/ie_lpis.parquet')
WHERE ST_Intersects(geometry, ST_Buffer(ST_Transform(ST_Point(53.3855, -8.3393), 'EPSG:4326', 'EPSG:2157'), 500))
LIMIT 5;
-- id | m2
-- C12E99FE1281F8544DCD8AEB656108A98F7E39EFD4A0CC76B9F60A144CEE0F3E | 26700.0
-- 124EF3203F0337760BFED5E6BC0315E676951B7001D2A43EA17DB7A49593316A | 16700.0
-- 62183F67E281EF5281875153EC1E5BE4BB263982C34483F7567A62D5A4C6BDE7 | 65100.0
-- EB5CCBF81B512EE1366A3A9C99CEC716B582D444D038C69274959EDD8727A5D5 | 23300.0
-- 5D76EB58259DC53A3E1DED23A7A91C7E7936E87124DFC1A28FA341712B909D29 | 26500.0
```

## Related collections

Every collection in this catalog shares the fiboa core columns, so the same queries work across countries; `s3://ftw/harmonized-field-data/*/latest/*.parquet` with `union_by_name = true` reads the newest edition of all of them (see the catalog [AGENTS.md](https://source.coop/ftw/harmonized-field-data/AGENTS.md)).

## Structure

Assets and structural links resolve relative to the object that carries them; there is no `self` link. Source: this collection is generated by [tools/catalogize.py](https://github.com/fieldsoftheworld/harmonized-field-data-catalog/blob/main/tools/catalogize.py) in the catalog repository — fix documentation there.
