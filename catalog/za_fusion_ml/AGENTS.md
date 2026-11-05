# Agent guidance — South Africa Crop Field Boundaries (Fusion Competition) with splits

South Africa (Fusion) with splits field boundaries in the [fiboa](https://github.com/fiboa/specification) schema, 1 edition (2017). Every claim below is quoted from the source, the converter, or measured from the published files; each query was run before it was written down, and its output follows it as comments.

## Access

- Latest edition, stable path: `https://data.source.coop/ftw/harmonized-field-data/za_fusion_ml/latest/za_fusion_ml.parquet`
- One edition: `https://data.source.coop/ftw/harmonized-field-data/za_fusion_ml/year=<year>/<file>.parquet`, e.g. `https://data.source.coop/ftw/harmonized-field-data/za_fusion_ml/year=2017/za_fusion_ml-2017.parquet`
- All editions (hive partitioned): `s3://ftw/harmonized-field-data/za_fusion_ml/year=*/*.parquet` — the S3 form of the same prefix through the Source Cooperative proxy, because `*` needs a listing that plain https does not provide. In DuckDB: `CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');` then `read_parquet(glob, hive_partitioning = true)` adds the `year` column. No credentials are needed.
- PMTiles for maps: `https://data.source.coop/ftw/harmonized-field-data/za_fusion_ml/year=2017/za_fusion_ml-2017.pmtiles`, layer `za_fusion_ml`; MapLibre styles in `styles/`.

## Quirks that produce silently wrong answers

- **CRS is EPSG:4326, not WGS84.** `ST_Area`/`ST_Distance` return units of that CRS; transform with `ST_Transform` if you need lon/lat, or use `metrics:area`.
- **`metrics:area` is in square metres** (source column `SHAPE_AREA`; where the source value is missing or 0 the converter computed it from the geometry, in EPSG:6933 when the CRS is not metric). Divide by 10 000 for hectares.
- **`year` is the edition, not the observation date.** It is the year of the source publication (the converter variant). `determination:datetime`, where present, is the source's own date for a field.
- **`id` is only guaranteed unique within one edition** (fiboa requires uniqueness per file; it is the source column `id`). Whether an id persists across editions is not verified here; do not join editions on it without checking.
- **`hcat:code` is hierarchical.** The first 4/6/8 digits are increasingly specific crop groups; compare prefixes, not equality, to aggregate (see the crop query below). Source crops without a mapping in the converter's HCAT table (`None`) have `NULL`. All 6,568 rows of the 2017 edition carry one.
- **Some fiboa properties are not columns.** Values constant for the whole file are stored once in the GeoParquet `collection` key-value metadata: `determination:datetime` = `2017-01-01T00:00:00Z`, `crop:code_list` = `https://fiboa.org/code/za/fusion/crop.csv` (2017 edition). Read them with `parquet_kv_metadata()` in DuckDB or `pyarrow.parquet.ParquetFile(f).schema_arrow.metadata[b'collection']`; they differ per edition where the source does.

## Tested queries

Fields and hectares per edition, through the partition glob:

```sql
INSTALL httpfs; LOAD httpfs;
CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');
SELECT year, count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('s3://ftw/harmonized-field-data/za_fusion_ml/year=*/*.parquet', hive_partitioning = true)
GROUP BY year ORDER BY year;
-- year | fields | hectares
-- 2017 | 6568 | 90442.0
```

Largest crop groups in the latest edition (HCAT level 3 = first 6 digits):

```sql
SELECT substr(CAST("hcat:code" AS VARCHAR), 1, 6) AS hcat_group, mode("hcat:name") AS most_common_name,
       count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/za_fusion_ml/latest/za_fusion_ml.parquet')
WHERE "hcat:code" IS NOT NULL
GROUP BY 1 ORDER BY hectares DESC LIMIT 5;
-- hcat_group | most_common_name | fields | hectares
-- 330109 | legumes_harvested_green | 4012 | 44535.0
-- 330101 | common_soft_wheat | 1906 | 33674.0
-- 330106 | rapeseed_rape | 650 | 12233.0
```

Fields around a point, transforming the point into the data's CRS instead of the data into WGS84:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT id, round("metrics:area") AS m2
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/za_fusion_ml/latest/za_fusion_ml.parquet')
WHERE ST_Intersects(geometry, ST_Buffer(ST_Transform(ST_Point(-34.1899, 20.7825), 'EPSG:4326', 'EPSG:4326'), 500))
LIMIT 5;
-- id | m2
-- train_82517 | 139767.0
-- train_82520 | 98651.0
-- train_269857 | 6814.0
-- train_82601 | 101521.0
-- train_82523 | 195515.0
```

## Related collections

Every collection in this catalog shares the fiboa core columns, so the same queries work across countries; `s3://ftw/harmonized-field-data/*/latest/*.parquet` with `union_by_name = true` reads the newest edition of all of them (see the catalog [AGENTS.md](https://source.coop/ftw/harmonized-field-data/AGENTS.md)).

## Structure

Assets and structural links resolve relative to the object that carries them; there is no `self` link. Source: this collection is generated by [tools/catalogize.py](https://github.com/fieldsoftheworld/harmonized-field-data-catalog/blob/main/tools/catalogize.py) in the catalog repository — fix documentation there.
