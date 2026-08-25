# Agent guidance — Field boundaries for Flanders, Belgium

Belgium, Flanders field boundaries in the [fiboa](https://github.com/fiboa/specification) schema, 4 editions (2023, 2024, 2025, 2026). Every claim below is quoted from the source, the converter, or measured from the published files; each query was run before it was written down, and its output follows it as comments.

## Access

- Latest edition, stable path: `https://data.source.coop/ftw/harmonized-field-data/be_vlg/latest/be_vlg.parquet`
- One edition: `https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=<year>/<file>.parquet`, e.g. `https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2026/be_vlg-2026.parquet`
- All editions (hive partitioned): `s3://ftw/harmonized-field-data/be_vlg/year=*/*.parquet` — the S3 form of the same prefix through the Source Cooperative proxy, because `*` needs a listing that plain https does not provide. In DuckDB: `CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');` then `read_parquet(glob, hive_partitioning = true)` adds the `year` column. No credentials are needed.
- PMTiles for maps: `https://data.source.coop/ftw/harmonized-field-data/be_vlg/year=2026/be_vlg-2026.pmtiles`, layer `be_vlg`; MapLibre styles in `styles/`.

## Quirks that produce silently wrong answers

- **CRS is EPSG:31370, not WGS84.** `ST_Area`/`ST_Distance` return units of that CRS; transform with `ST_Transform` if you need lon/lat, or use `metrics:area`.
- **`metrics:area` is in square metres**, taken from the source column `GRAF_OPP` (hectares × 10 000). Divide by 10 000 for hectares.
- **`year` is the edition, not the observation date.** It is the year of the source publication (the converter variant). `determination:datetime`, where present, is the source's own date for a field.
- **`id` is only guaranteed unique within one edition** (fiboa requires uniqueness per file; it is the source column `REF_ID`). Whether an id persists across editions is not verified here; do not join editions on it without checking.
- **`hcat:code` is hierarchical.** The first 4/6/8 digits are increasingly specific crop groups; compare prefixes, not equality, to aggregate (see the crop query below). Source crops without a mapping in the converter's HCAT table (`be_vlg_2021.csv`) have `NULL`.
- **Some fiboa properties are not columns.** Values constant for the whole file are stored once in the GeoParquet `collection` key-value metadata: `typology` = `None`, `admin:country_code` = `BE`, `admin:subdivision_code` = `VLG`, `determination:datetime` = `2026-01-01T00:00:00Z`, `crop:code_list` = `https://raw.githubusercontent.com/maja601/EuroCrops/refs/heads/main/csvs/country_mappings/be_vlg_2021.csv` (2026 edition). Read them with `parquet_kv_metadata()` in DuckDB or `pyarrow.parquet.ParquetFile(f).schema_arrow.metadata[b'collection']`; they differ per edition where the source does.

## Tested queries

Fields and hectares per edition, through the partition glob:

```sql
INSTALL httpfs; LOAD httpfs;
CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');
SELECT year, count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('s3://ftw/harmonized-field-data/be_vlg/year=*/*.parquet', hive_partitioning = true)
GROUP BY year ORDER BY year;
-- year | fields | hectares
-- 2023 | 588192 | 672046.0
-- 2024 | 589749 | 669055.0
-- 2025 | 594732 | 672201.0
-- 2026 | 597088 | 671328.0
```

Largest crop groups in the latest edition (HCAT level 3 = first 6 digits):

```sql
SELECT substr(CAST("hcat:code" AS VARCHAR), 1, 6) AS hcat_group, mode("hcat:name") AS most_common_name,
       count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/be_vlg/latest/be_vlg.parquet')
WHERE "hcat:code" IS NOT NULL
GROUP BY 1 ORDER BY hectares DESC LIMIT 5;
-- hcat_group | most_common_name | fields | hectares
-- 330200 | pasture_meadow_grassland_grass | 231205 | 237309.0
-- 330109 | green_silo_maize | 88753 | 142715.0
-- 330101 | grain_maize_corn_popcorn | 73378 | 130982.0
-- 330103 | potatoes | 19707 | 46044.0
-- 330129 | sugar_beet | 10469 | 23780.0
```

Fields around a point, transforming the point into the data's CRS instead of the data into WGS84:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT id, round("metrics:area") AS m2
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/be_vlg/latest/be_vlg.parquet')
WHERE ST_Intersects(geometry, ST_Buffer(ST_Transform(ST_Point(51.0848, 4.2319), 'EPSG:4326', 'EPSG:31370'), 500))
LIMIT 5;
-- id | m2
-- 2532766693.0 | 13975.0
-- 926964130.0 | 9874.0
-- 1119557630.0 | 1860.0
-- 1860236189.0 | 3712.0
-- 1860235987.0 | 5699.0
```

## Related collections

Every collection in this catalog shares the fiboa core columns, so the same queries work across countries; `s3://ftw/harmonized-field-data/*/latest/*.parquet` with `union_by_name = true` reads the newest edition of all of them (see the catalog [AGENTS.md](https://source.coop/ftw/harmonized-field-data/AGENTS.md)).

## Structure

Assets and structural links resolve relative to the object that carries them; there is no `self` link. Source: this collection is generated by [tools/catalogize.py](https://github.com/fieldsoftheworld/harmonized-field-data-catalog/blob/main/tools/catalogize.py) in the catalog repository — fix documentation there.
