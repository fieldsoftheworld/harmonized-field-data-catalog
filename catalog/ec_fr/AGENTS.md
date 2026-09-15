# Agent guidance — Field boundaries for France - Eurocrops 2018

France - Eurocrops 2018 field boundaries in the [fiboa](https://github.com/fiboa/specification) schema, 1 edition (2018). Every claim below is quoted from the source, the converter, or measured from the published files; each query was run before it was written down, and its output follows it as comments.

## Access

- Latest edition, stable path: `https://data.source.coop/ftw/harmonized-field-data/ec_fr/latest/ec_fr.parquet`
- One edition: `https://data.source.coop/ftw/harmonized-field-data/ec_fr/year=<year>/<file>.parquet`, e.g. `https://data.source.coop/ftw/harmonized-field-data/ec_fr/year=2018/ec_fr.parquet`
- All editions (hive partitioned): `s3://ftw/harmonized-field-data/ec_fr/year=*/*.parquet` — the S3 form of the same prefix through the Source Cooperative proxy, because `*` needs a listing that plain https does not provide. In DuckDB: `CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');` then `read_parquet(glob, hive_partitioning = true)` adds the `year` column. No credentials are needed.
- PMTiles for maps: `https://data.source.coop/ftw/harmonized-field-data/ec_fr/year=2018/ec_fr.pmtiles`, layer `ec_fr`; MapLibre styles in `styles/`.

## Quirks that produce silently wrong answers

- **CRS is EPSG:2154, not WGS84.** `ST_Area`/`ST_Distance` return units of that CRS; transform with `ST_Transform` if you need lon/lat, or use `metrics:area`.
- **`metrics:area` is in square metres**, taken from the source column `SURF_PARC` (hectares × 10 000). Divide by 10 000 for hectares.
- **`year` is the edition, not the observation date.** It is the year of the source publication (the converter variant). `determination:datetime`, where present, is the source's own date for a field.
- **`id` is only guaranteed unique within one edition** (fiboa requires uniqueness per file; it is the source column `ID_PARCEL`). Whether an id persists across editions is not verified here; do not join editions on it without checking.
- **`hcat:code` is hierarchical.** The first 4/6/8 digits are increasingly specific crop groups; compare prefixes, not equality, to aggregate (see the crop query below). Source crops without a mapping in the converter's HCAT table (`fr_2018.csv`) have `NULL`.
- **Some fiboa properties are not columns.** Values constant for the whole file are stored once in the GeoParquet `collection` key-value metadata: `crop:code_list` = `https://raw.githubusercontent.com/maja601/EuroCrops/refs/heads/main/csvs/country_mappings/fr_2018.csv` (2018 edition). Read them with `parquet_kv_metadata()` in DuckDB or `pyarrow.parquet.ParquetFile(f).schema_arrow.metadata[b'collection']`; they differ per edition where the source does.
- The 2018 campaign of the Registre Parcellaire Graphique, which IGN publishes no archive for: its downloads run 2017 and 2019 onwards. SURF_PARC is rounded to 0.01 ha, so 4,913 parcels under 50 m2 take their area from the geometry.

## Tested queries

Fields and hectares per edition, through the partition glob:

```sql
INSTALL httpfs; LOAD httpfs;
CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');
SELECT year, count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('s3://ftw/harmonized-field-data/ec_fr/year=*/*.parquet', hive_partitioning = true)
GROUP BY year ORDER BY year;
-- year | fields | hectares
-- 2018 | 9517891 | 27917501.0
```

Largest crop groups in the latest edition (HCAT level 3 = first 6 digits):

```sql
SELECT substr(CAST("hcat:code" AS VARCHAR), 1, 6) AS hcat_group, mode("hcat:name") AS most_common_name,
       count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/ec_fr/latest/ec_fr.parquet')
WHERE "hcat:code" IS NOT NULL
GROUP BY 1 ORDER BY hectares DESC LIMIT 5;
-- hcat_group | most_common_name | fields | hectares
-- 330200 | pasture_meadow_grassland_grass | 3204782 | 9632408.0
-- 330101 | winter_common_soft_wheat | 2067101 | 9140227.0
-- 330109 | temporary_grass | 1234888 | 3254032.0
-- 330106 | winter_rapeseed_rape | 453755 | 2377266.0
-- 330102 | legumes_dried_pulses_protein_crops | 192621 | 668900.0
```

Fields around a point, transforming the point into the data's CRS instead of the data into WGS84:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT id, round("metrics:area") AS m2
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/ec_fr/latest/ec_fr.parquet')
WHERE ST_Intersects(geometry, ST_Buffer(ST_Transform(ST_Point(46.0777, 2.6994), 'EPSG:4326', 'EPSG:2154'), 500))
LIMIT 5;
-- id | m2
-- 6871729 | 19700.0
-- 6871730 | 8500.0
-- 6796871 | 4500.0
-- 6890318 | 3900.0
-- 6879616 | 19800.0
```

## Related collections

Every collection in this catalog shares the fiboa core columns, so the same queries work across countries; `s3://ftw/harmonized-field-data/*/latest/*.parquet` with `union_by_name = true` reads the newest edition of all of them (see the catalog [AGENTS.md](https://source.coop/ftw/harmonized-field-data/AGENTS.md)).

## Structure

Assets and structural links resolve relative to the object that carries them; there is no `self` link. Source: this collection is generated by [tools/catalogize.py](https://github.com/fieldsoftheworld/harmonized-field-data-catalog/blob/main/tools/catalogize.py) in the catalog repository — fix documentation there.
