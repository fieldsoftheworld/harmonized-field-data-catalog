# Agent guidance — California (US) Statewide Crop Mapping

US, California (SCM) field boundaries in the [fiboa](https://github.com/fiboa/specification) schema, 9 editions (2014, 2016, 2018, 2019, 2020, 2021, 2022, 2023, 2024). Every claim below is quoted from the source, the converter, or measured from the published files; each query was run before it was written down, and its output follows it as comments.

## Access

- Latest edition, stable path: `https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/latest/us_ca_scm.parquet`
- One edition: `https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=<year>/<file>.parquet`, e.g. `https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2024/us_ca_scm-2024.parquet`
- All editions (hive partitioned): `s3://ftw/harmonized-field-data/us_ca_scm/year=*/*.parquet` — the S3 form of the same prefix through the Source Cooperative proxy, because `*` needs a listing that plain https does not provide. In DuckDB: `CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');` then `read_parquet(glob, hive_partitioning = true)` adds the `year` column. No credentials are needed.
- PMTiles for maps: `https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/year=2024/us_ca_scm-2024.pmtiles`, layer `us_ca_scm`; MapLibre styles in `styles/`.

## Quirks that produce silently wrong answers

- **CRS is EPSG:4269, not WGS84.** `ST_Area`/`ST_Distance` return units of that CRS; transform with `ST_Transform` if you need lon/lat, or use `metrics:area`.
- **`metrics:area` is in square metres**, computed by the converter from the geometry (EPSG:6933 when the CRS is not metric). Divide by 10 000 for hectares.
- **`year` is the edition, not the observation date.** It is the year of the source publication (the converter variant). `determination:datetime`, where present, is the source's own date for a field.
- **`id` is only guaranteed unique within one edition** (fiboa requires uniqueness per file; it is the source column `UniqueID`). Whether an id persists across editions is not verified here; do not join editions on it without checking.
- **`hcat:code` is hierarchical.** The first 4/6/8 digits are increasingly specific crop groups; compare prefixes, not equality, to aggregate (see the crop query below). Source crops without a mapping in the converter's HCAT table (`None`) have `NULL`. All 447,944 rows of the 2024 edition carry one.
- **Some fiboa properties are not columns.** Values constant for the whole file are stored once in the GeoParquet `collection` key-value metadata: `determination:datetime` = `2024-07-01T00:00:00Z`, `admin:country_code` = `US`, `admin:subdivision_code` = `CA`, `crop:code_list` = `https://fiboa.org/code/us/ca/scm.csv` (2024 edition). Read them with `parquet_kv_metadata()` in DuckDB or `pyarrow.parquet.ParquetFile(f).schema_arrow.metadata[b'collection']`; they differ per edition where the source does.
- 2024 is provisional (DWR release of 2025-12-08) until DWR publishes the final edition. The crop column differs by edition: from 2019 the source's `MAIN_CROP`; in 2016 and 2018 the main-season `CROPTYP2`; 2014 names its crops only, and `crop:code` there comes from the names' codes in 2016. 2014 and 2016 carry no identifier, so there `id` is a row number. DWR maps the whole state; its urban mask (`U`, or `****` in 2020–2022: some 1,600 to 6,800 polygons per edition covering about 2 million ha, the largest close to 590,000 ha), urban landscape (`UL2`) and riparian vegetation (`NR`) are left out, as they are not fields.

## Tested queries

Fields and hectares per edition, through the partition glob:

```sql
INSTALL httpfs; LOAD httpfs;
CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');
SELECT year, count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('s3://ftw/harmonized-field-data/us_ca_scm/year=*/*.parquet', hive_partitioning = true)
GROUP BY year ORDER BY year;
-- year | fields | hectares
-- 2014 | 359484 | 3672258.0
-- 2016 | 388543 | 3805644.0
-- 2018 | 406662 | 3838838.0
-- 2019 | 409513 | 3850704.0
-- 2020 | 421540 | 3897700.0
-- 2021 | 425534 | 3901874.0
-- 2022 | 431776 | 3910351.0
-- 2023 | 439642 | 3917052.0
-- ... 1 more rows
```

Largest crop groups in the latest edition (HCAT level 3 = first 6 digits):

```sql
SELECT substr(CAST("hcat:code" AS VARCHAR), 1, 6) AS hcat_group, mode("hcat:name") AS most_common_name,
       count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/latest/us_ca_scm.parquet')
WHERE "hcat:code" IS NOT NULL
GROUP BY 1 ORDER BY hectares DESC LIMIT 5;
-- hcat_group | most_common_name | fields | hectares
-- 330303 | almond | 75165 | 1018754.0
-- 330101 | cereal | 30932 | 549981.0
-- 330200 | pasture_meadow_grassland_grass | 39132 | 373394.0
-- 330306 | vineyards_wine_vine_rebland_grapes | 69875 | 300113.0
-- 330109 | alfalfa_lucerne | 12573 | 230196.0
```

Fields around a point, transforming the point into the data's CRS instead of the data into WGS84:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT id, round("metrics:area") AS m2
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/us_ca_scm/latest/us_ca_scm.parquet')
WHERE ST_Intersects(geometry, ST_Buffer(ST_Transform(ST_Point(37.2752, -119.4334), 'EPSG:4326', 'EPSG:4269'), 500))
LIMIT 5;
-- id | m2
-- 3705084 | 40562.0
-- 3705118 | 34449.0
-- 3710129 | 61027.0
-- 3722789 | 24574.0
-- 3701239 | 127584.0
```

## Related collections

Every collection in this catalog shares the fiboa core columns, so the same queries work across countries; `s3://ftw/harmonized-field-data/*/latest/*.parquet` with `union_by_name = true` reads the newest edition of all of them (see the catalog [AGENTS.md](https://source.coop/ftw/harmonized-field-data/AGENTS.md)).

## Structure

Assets and structural links resolve relative to the object that carries them; there is no `self` link. Source: this collection is generated by [tools/catalogize.py](https://github.com/fieldsoftheworld/harmonized-field-data-catalog/blob/main/tools/catalogize.py) in the catalog repository — fix documentation there.
