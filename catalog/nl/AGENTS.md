# Agent guidance — BRP Crop Field Boundaries for The Netherlands (CAP-based)

Netherlands (Crops) field boundaries in the [fiboa](https://github.com/fiboa/specification) schema, 22 editions (2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026). Every claim below is quoted from the source, the converter, or measured from the published files; each query was run before it was written down, and its output follows it as comments.

## Access

- Latest edition, stable path: `https://data.source.coop/ftw/harmonized-field-data/nl/latest/nl.parquet`
- One edition: `https://data.source.coop/ftw/harmonized-field-data/nl/year=<year>/<file>.parquet`, e.g. `https://data.source.coop/ftw/harmonized-field-data/nl/year=2026/nl-2026.parquet`
- All editions (hive partitioned): `s3://ftw/harmonized-field-data/nl/year=*/*.parquet` — the S3 form of the same prefix through the Source Cooperative proxy, because `*` needs a listing that plain https does not provide. In DuckDB: `CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');` then `read_parquet(glob, hive_partitioning = true)` adds the `year` column. No credentials are needed.
- PMTiles for maps: `https://data.source.coop/ftw/harmonized-field-data/nl/year=2026/nl-2026.pmtiles`, layer `nl`; MapLibre styles in `styles/`.

## Quirks that produce silently wrong answers

- **CRS is EPSG:28992, not WGS84.** `ST_Area`/`ST_Distance` return units of that CRS; transform with `ST_Transform` if you need lon/lat, or use `metrics:area`.
- **`metrics:area` is in square metres**, computed by the converter from the geometry (EPSG:6933 when the CRS is not metric). Divide by 10 000 for hectares.
- **`year` is the year the boundaries represent**: the declaration year or season of a register, the year a snapshot was taken, or (for a source covering several years) the year of each field's own `determination:datetime`. `determination:datetime`, where present, is the source's own date for a field.
- **`id` is only guaranteed unique within one edition** (fiboa requires uniqueness per file; it is assigned by the converter). Whether an id persists across editions is not verified here; do not join editions on it without checking.
- **`hcat:code` is hierarchical.** The first 4/6/8 digits are increasingly specific crop groups; compare prefixes, not equality, to aggregate (see the crop query below). Source crops without a mapping in the converter's HCAT table (`None`) have `NULL`. All 1,266,361 rows of the 2026 edition carry one.
- **Some fiboa properties are not columns.** Values constant for the whole file are stored once in the GeoParquet `collection` key-value metadata: `determination:datetime` = `2026-05-15T00:00:00Z`, `admin:country_code` = `NL`, `crop:code_list` = `https://fiboa.org/code/nl/nl.csv` (2026 edition). Read them with `parquet_kv_metadata()` in DuckDB or `pyarrow.parquet.ParquetFile(f).schema_arrow.metadata[b'collection']`; they differ per edition where the source does.
- The editions 2005-2008 were published by RVO under the same license and are no longer downloadable from PDOK; they are converted from copies of the original shapefiles, which also keep fallow (`Braakland`) and crops without a category. RVO gave some crop codes a new crop over the years: an edition before the new meaning carries the code with an `o` suffix (`1934o`, starch potatoes, against `1934`, shallots, from 2019), which the code list maps to the old crop.

## Tested queries

Fields and hectares per edition, through the partition glob:

```sql
INSTALL httpfs; LOAD httpfs;
CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');
SELECT year, count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('s3://ftw/harmonized-field-data/nl/year=*/*.parquet', hive_partitioning = true)
GROUP BY year ORDER BY year;
-- year | fields | hectares
-- 2005 | 731927 | 1838037.0
-- 2006 | 771385 | 1897673.0
-- 2007 | 759230 | 1908446.0
-- 2008 | 755057 | 1922893.0
-- 2009 | 809814 | 1887471.0
-- 2010 | 776291 | 1881098.0
-- 2011 | 773361 | 1871345.0
-- 2012 | 763436 | 1836951.0
-- ... 14 more rows
```

Largest crop groups in the latest edition (HCAT level 3 = first 6 digits):

```sql
SELECT substr(CAST("hcat:code" AS VARCHAR), 1, 6) AS hcat_group, mode("hcat:name") AS most_common_name,
       count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/nl/latest/nl.parquet')
WHERE "hcat:code" IS NOT NULL
GROUP BY 1 ORDER BY hectares DESC LIMIT 5;
-- hcat_group | most_common_name | fields | hectares
-- 330200 | pasture_meadow_grassland_grass | 686528 | 755069.0
-- 330109 | temporary_grass | 250514 | 422321.0
-- 330101 | winter_common_soft_wheat | 58401 | 187476.0
-- 330103 | potatoes | 32434 | 149306.0
-- 330129 | sugar_beet | 17692 | 81570.0
```

Fields within 500 m of a point given in lon/lat, transforming the point into the data's CRS instead of the data into WGS84:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT id, round("metrics:area") AS m2
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/nl/latest/nl.parquet')
WHERE ST_Intersects(geometry, ST_Buffer(ST_Transform(ST_Point(5.3027, 52.1488), 'EPSG:4326', 'EPSG:28992', always_xy := true), 500))
LIMIT 5;
-- id | m2
-- 1165738 | 8640.0
```

## Related collections

Every collection in this catalog shares the fiboa core columns, so the same queries work across countries; `s3://ftw/harmonized-field-data/*/latest/*.parquet` with `union_by_name = true` reads the newest edition of all of them (see the catalog [AGENTS.md](https://source.coop/ftw/harmonized-field-data/AGENTS.md)).

## Structure

Assets and structural links resolve relative to the object that carries them; there is no `self` link. Source: this collection is generated by [tools/catalogize.py](https://github.com/fieldsoftheworld/harmonized-field-data-catalog/blob/main/tools/catalogize.py) in the catalog repository — fix documentation there.
