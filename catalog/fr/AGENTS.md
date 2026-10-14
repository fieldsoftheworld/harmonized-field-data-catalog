# Agent guidance — Registre Parcellaire Graphique; Crop Fields France

France field boundaries in the [fiboa](https://github.com/fiboa/specification) schema, 10 editions (2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024). Every claim below is quoted from the source, the converter, or measured from the published files; each query was run before it was written down, and its output follows it as comments.

## Access

- Latest edition, stable path: `https://data.source.coop/ftw/harmonized-field-data/fr/latest/fr.parquet`
- One edition: `https://data.source.coop/ftw/harmonized-field-data/fr/year=<year>/<file>.parquet`, e.g. `https://data.source.coop/ftw/harmonized-field-data/fr/year=2024/fr-2024.parquet`
- All editions (hive partitioned): `s3://ftw/harmonized-field-data/fr/year=*/*.parquet` — the S3 form of the same prefix through the Source Cooperative proxy, because `*` needs a listing that plain https does not provide. In DuckDB: `CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');` then `read_parquet(glob, hive_partitioning = true)` adds the `year` column. No credentials are needed.
- PMTiles for maps: `https://data.source.coop/ftw/harmonized-field-data/fr/year=2024/fr-2024.pmtiles`, layer `fr`; MapLibre styles in `styles/`.

## Quirks that produce silently wrong answers

- **CRS is EPSG:2154, not WGS84.** `ST_Area`/`ST_Distance` return units of that CRS; transform with `ST_Transform` if you need lon/lat, or use `metrics:area`.
- **`metrics:area` is in square metres** (source column `surf_parc`, hectares × 10 000; where the source value is missing or 0 the converter computed it from the geometry, in EPSG:6933 when the CRS is not metric). Divide by 10 000 for hectares.
- **`year` is the edition, not the observation date.** It is the year of the source publication (the converter variant). `determination:datetime`, where present, is the source's own date for a field.
- **`id` is only guaranteed unique within one edition** (fiboa requires uniqueness per file; it is the source column `id`). Whether an id persists across editions is not verified here; do not join editions on it without checking.
- **`hcat:code` is hierarchical.** The first 4/6/8 digits are increasingly specific crop groups; compare prefixes, not equality, to aggregate (see the crop query below). Source crops without a mapping in the converter's HCAT table (`None`) have `NULL`. 60,765 of the 9,671,682 rows of the 2024 edition (0.63%) have none, so a query that filters or groups on crop silently leaves them out.
- **Some fiboa properties are not columns.** Values constant for the whole file are stored once in the GeoParquet `collection` key-value metadata: `admin:country_code` = `FR`, `determination:datetime` = `2024-01-01T00:00:00Z`, `crop:code_list` = `https://fiboa.org/code/fr/fr.csv` (2024 edition). Read them with `parquet_kv_metadata()` in DuckDB or `pyarrow.parquet.ParquetFile(f).schema_arrow.metadata[b'collection']`; they differ per edition where the source does.
- **Not every edition comes from the same source.** The 2015, 2016 and 2018 editions, which the source above does not offer, come from Registre Parcellaire Graphique; Crop Fields France — EuroCrops V2 (Joint Research Centre, European Commission, converter `ec_fr`), under CC-BY-4.0; attribution: European Commission, Joint Research Centre — EuroCropsV2; their items carry those terms.

## Tested queries

Fields and hectares per edition, through the partition glob:

```sql
INSTALL httpfs; LOAD httpfs;
CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');
SELECT year, count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('s3://ftw/harmonized-field-data/fr/year=*/*.parquet', hive_partitioning = true)
GROUP BY year ORDER BY year;
-- year | fields | hectares
-- 2015 | 9434038 | 27867116.0
-- 2016 | 9333351 | 27886804.0
-- 2017 | 9389434 | 27890010.0
-- 2018 | 9516722 | 27922092.0
-- 2019 | 9599079 | 27960148.0
-- 2020 | 9772765 | 27998174.0
-- 2021 | 9848527 | 28021954.0
-- 2022 | 9888758 | 28009283.0
-- ... 2 more rows
```

Largest crop groups in the latest edition (HCAT level 3 = first 6 digits):

```sql
SELECT substr(CAST("hcat:code" AS VARCHAR), 1, 6) AS hcat_group, mode("hcat:name") AS most_common_name,
       count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/fr/latest/fr.parquet')
WHERE "hcat:code" IS NOT NULL
GROUP BY 1 ORDER BY hectares DESC LIMIT 5;
-- hcat_group | most_common_name | fields | hectares
-- 330200 | pasture_meadow_grassland_grass | 3304569 | 9952637.0
-- 330101 | grain_maize_corn_popcorn | 2174948 | 9813969.0
-- 330106 | winter_rapeseed_rape | 443974 | 2383876.0
-- 330109 | temporary_grass | 925055 | 2084728.0
-- 330102 | legumes_dried_pulses_protein_crops | 236973 | 809057.0
```

Fields around a point, transforming the point into the data's CRS instead of the data into WGS84:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT id, round("metrics:area") AS m2
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/fr/latest/fr.parquet')
WHERE ST_Intersects(geometry, ST_Buffer(ST_Transform(ST_Point(46.2206, 2.2165), 'EPSG:4326', 'EPSG:2154'), 500))
LIMIT 5;
-- id | m2
-- 9527516 | 7000.0
-- 2889833 | 38400.0
-- 9030792 | 7100.0
-- 6449879 | 13700.0
-- 891462 | 5800.0
```

## Related collections

Every collection in this catalog shares the fiboa core columns, so the same queries work across countries; `s3://ftw/harmonized-field-data/*/latest/*.parquet` with `union_by_name = true` reads the newest edition of all of them (see the catalog [AGENTS.md](https://source.coop/ftw/harmonized-field-data/AGENTS.md)).

## Structure

Assets and structural links resolve relative to the object that carries them; there is no `self` link. Source: this collection is generated by [tools/catalogize.py](https://github.com/fieldsoftheworld/harmonized-field-data-catalog/blob/main/tools/catalogize.py) in the catalog repository — fix documentation there.
