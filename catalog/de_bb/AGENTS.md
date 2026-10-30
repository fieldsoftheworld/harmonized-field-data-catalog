# Agent guidance — Field boundaries for Berlin / Brandenburg, Germany

Germany, Berlin/Brandenburg field boundaries in the [fiboa](https://github.com/fiboa/specification) schema, 15 editions (2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2026). Every claim below is quoted from the source, the converter, or measured from the published files; each query was run before it was written down, and its output follows it as comments.

## Access

- Latest edition, stable path: `https://data.source.coop/ftw/harmonized-field-data/de_bb/latest/de_bb.parquet`
- One edition: `https://data.source.coop/ftw/harmonized-field-data/de_bb/year=<year>/<file>.parquet`, e.g. `https://data.source.coop/ftw/harmonized-field-data/de_bb/year=2026/de_bb-2026.parquet`
- All editions (hive partitioned): `s3://ftw/harmonized-field-data/de_bb/year=*/*.parquet` — the S3 form of the same prefix through the Source Cooperative proxy, because `*` needs a listing that plain https does not provide. In DuckDB: `CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');` then `read_parquet(glob, hive_partitioning = true)` adds the `year` column. No credentials are needed.
- PMTiles for maps: `https://data.source.coop/ftw/harmonized-field-data/de_bb/year=2026/de_bb-2026.pmtiles`, layer `de_bb`; MapLibre styles in `styles/`.

## Quirks that produce silently wrong answers

- **CRS is EPSG:25833, not WGS84.** `ST_Area`/`ST_Distance` return units of that CRS; transform with `ST_Transform` if you need lon/lat, or use `metrics:area`.
- **`metrics:area` is in square metres** (source column `groesse`, hectares × 10 000; where the source value is missing or 0 the converter computed it from the geometry, in EPSG:6933 when the CRS is not metric). Divide by 10 000 for hectares.
- **`year` is the edition, not the observation date.** It is the year of the source publication (the converter variant). `determination:datetime`, where present, is the source's own date for a field.
- **`id` is only guaranteed unique within one edition** (fiboa requires uniqueness per file; it is assigned by the converter). Whether an id persists across editions is not verified here; do not join editions on it without checking.
- **`hcat:code` is hierarchical.** The first 4/6/8 digits are increasingly specific crop groups; compare prefixes, not equality, to aggregate (see the crop query below). Source crops without a mapping in the converter's HCAT table (`None`) have `NULL`. All 181,768 rows of the 2026 edition carry one.
- **Some fiboa properties are not columns.** Values constant for the whole file are stored once in the GeoParquet `collection` key-value metadata: `admin:country_code` = `DE`, `admin:subdivision_code` = `BB`, `crop:code_list` = `https://raw.githubusercontent.com/maja601/EuroCrops/refs/heads/main/csvs/country_mappings/de.csv` (2026 edition). Read them with `parquet_kv_metadata()` in DuckDB or `pyarrow.parquet.ParquetFile(f).schema_arrow.metadata[b'collection']`; they differ per edition where the source does.
- **Not every edition comes from the same source.** The 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022 and 2023 editions, which the source above does not offer, come from Field boundaries for Berlin / Brandenburg, Germany — EuroCrops V2 (Joint Research Centre, European Commission, converter `ec_de_bb`), under CC-BY-4.0; attribution: European Commission, Joint Research Centre — EuroCropsV2; their items carry those terms.

## Tested queries

Fields and hectares per edition, through the partition glob:

```sql
INSTALL httpfs; LOAD httpfs;
CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');
SELECT year, count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('s3://ftw/harmonized-field-data/de_bb/year=*/*.parquet', hive_partitioning = true)
GROUP BY year ORDER BY year;
-- year | fields | hectares
-- 2010 | 156686 | 1313100.0
-- 2011 | 160258 | 1309174.0
-- 2012 | 158028 | 1288174.0
-- 2013 | 156241 | 1285621.0
-- 2014 | 155308 | 1281086.0
-- 2015 | 158313 | 1289129.0
-- 2016 | 159093 | 1308007.0
-- 2017 | 161429 | 1309533.0
-- ... 7 more rows
```

Largest crop groups in the latest edition (HCAT level 3 = first 6 digits):

```sql
SELECT substr(CAST("hcat:code" AS VARCHAR), 1, 6) AS hcat_group, mode("hcat:name") AS most_common_name,
       count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/de_bb/latest/de_bb.parquet')
WHERE "hcat:code" IS NOT NULL
GROUP BY 1 ORDER BY hectares DESC LIMIT 5;
-- hcat_group | most_common_name | fields | hectares
-- 330101 | winter_rye | 35105 | 499869.0
-- 330200 | pasture_meadow_grassland_grass | 79682 | 340180.0
-- 330109 | green_silo_maize | 17360 | 206411.0
-- 330106 | winter_rapeseed_rape | 7052 | 127556.0
-- 330111 | fallow_land_not_crop | 27597 | 59227.0
```

Fields around a point, transforming the point into the data's CRS instead of the data into WGS84:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT id, round("metrics:area") AS m2
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/de_bb/latest/de_bb.parquet')
WHERE ST_Intersects(geometry, ST_Buffer(ST_Transform(ST_Point(52.4588, 13.0172), 'EPSG:4326', 'EPSG:25833'), 500))
LIMIT 5;
-- id | m2
-- 120682 | 63332.0
-- 120683 | 21874.0
-- 120662 | 6888.0
-- 120661 | 65257.0
-- 120660 | 503.0
```

## Related collections

Every collection in this catalog shares the fiboa core columns, so the same queries work across countries; `s3://ftw/harmonized-field-data/*/latest/*.parquet` with `union_by_name = true` reads the newest edition of all of them (see the catalog [AGENTS.md](https://source.coop/ftw/harmonized-field-data/AGENTS.md)).

## Structure

Assets and structural links resolve relative to the object that carries them; there is no `self` link. Source: this collection is generated by [tools/catalogize.py](https://github.com/fieldsoftheworld/harmonized-field-data-catalog/blob/main/tools/catalogize.py) in the catalog repository — fix documentation there.
