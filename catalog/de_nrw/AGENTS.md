# Agent guidance — Field blocks for North Rhine-Westphalia (NRW), Germany

Germany, North Rhine-Westphalia field boundaries in the [fiboa](https://github.com/fiboa/specification) schema, 6 editions (2019, 2020, 2021, 2022, 2023, 2026). Every claim below is quoted from the source, the converter, or measured from the published files; each query was run before it was written down, and its output follows it as comments.

## Access

- Latest edition, stable path: `https://data.source.coop/ftw/harmonized-field-data/de_nrw/latest/de_nrw.parquet`
- One edition: `https://data.source.coop/ftw/harmonized-field-data/de_nrw/year=<year>/<file>.parquet`, e.g. `https://data.source.coop/ftw/harmonized-field-data/de_nrw/year=2026/de_nrw-2026.parquet`
- All editions (hive partitioned): `s3://ftw/harmonized-field-data/de_nrw/year=*/*.parquet` — the S3 form of the same prefix through the Source Cooperative proxy, because `*` needs a listing that plain https does not provide. In DuckDB: `CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');` then `read_parquet(glob, hive_partitioning = true)` adds the `year` column. No credentials are needed.
- PMTiles for maps: `https://data.source.coop/ftw/harmonized-field-data/de_nrw/year=2026/de_nrw-2026.pmtiles`, layer `de_nrw`; MapLibre styles in `styles/`.

## Quirks that produce silently wrong answers

- **CRS is EPSG:25832, not WGS84.** `ST_Area`/`ST_Distance` return units of that CRS; transform with `ST_Transform` if you need lon/lat, or use `metrics:area`.
- **`metrics:area` is in square metres** (source column `AREA_HA`, hectares × 10 000; where the source value is missing or 0 the converter computed it from the geometry, in EPSG:6933 when the CRS is not metric). Divide by 10 000 for hectares.
- **`year` is the edition, not the observation date.** It is the year of the source publication (the converter variant). `determination:datetime`, where present, is the source's own date for a field.
- **`id` is only guaranteed unique within one edition** (fiboa requires uniqueness per file; it is the source column `ID`). Whether an id persists across editions is not verified here; do not join editions on it without checking.
- **`hcat:code` is hierarchical.** The first 4/6/8 digits are increasingly specific crop groups; compare prefixes, not equality, to aggregate (see the crop query below). Source crops without a mapping in the converter's HCAT table (`None`) have `NULL`. 565 of the 743,072 rows of the 2026 edition (0.08%) have none, so a query that filters or groups on crop silently leaves them out.
- **Some fiboa properties are not columns.** Values constant for the whole file are stored once in the GeoParquet `collection` key-value metadata: `admin:country_code` = `DE`, `admin:subdivision_code` = `NW`, `crop:code_list` = `https://raw.githubusercontent.com/maja601/EuroCrops/refs/heads/main/csvs/country_mappings/de_nrw_2021.csv` (2026 edition). Read them with `parquet_kv_metadata()` in DuckDB or `pyarrow.parquet.ParquetFile(f).schema_arrow.metadata[b'collection']`; they differ per edition where the source does.
- **Not every edition comes from the same source.** The 2019, 2020, 2021, 2022 and 2023 editions, which the source above does not offer, come from Field blocks for North Rhine-Westphalia (NRW), Germany — EuroCrops V2 (Joint Research Centre, European Commission, converter `ec_de_nrw`), under CC-BY-4.0; attribution: European Commission, Joint Research Centre — EuroCropsV2; their items carry those terms.

## Tested queries

Fields and hectares per edition, through the partition glob:

```sql
INSTALL httpfs; LOAD httpfs;
CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');
SELECT year, count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('s3://ftw/harmonized-field-data/de_nrw/year=*/*.parquet', hive_partitioning = true)
GROUP BY year ORDER BY year;
-- year | fields | hectares
-- 2019 | 728203 | 1496399.0
-- 2020 | 734231 | 1493229.0
-- 2021 | 734863 | 1490920.0
-- 2022 | 737376 | 1485190.0
-- 2023 | 748208 | 1473576.0
-- 2026 | 743072 | 1460343.0
```

Largest crop groups in the latest edition (HCAT level 3 = first 6 digits):

```sql
SELECT substr(CAST("hcat:code" AS VARCHAR), 1, 6) AS hcat_group, mode("hcat:name") AS most_common_name,
       count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/de_nrw/latest/de_nrw.parquet')
WHERE "hcat:code" IS NOT NULL
GROUP BY 1 ORDER BY hectares DESC LIMIT 5;
-- hcat_group | most_common_name | fields | hectares
-- 330101 | winter_common_soft_wheat | 171670 | 550261.0
-- 330200 | pasture_meadow_grassland_grass | 316272 | 442954.0
-- 330109 | green_silo_maize | 75221 | 208356.0
-- 330106 | winter_rapeseed_rape | 17583 | 62983.0
-- 330129 | sugar_beet | 13014 | 54120.0
```

Fields around a point, transforming the point into the data's CRS instead of the data into WGS84:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT id, round("metrics:area") AS m2
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/de_nrw/latest/de_nrw.parquet')
WHERE ST_Intersects(geometry, ST_Buffer(ST_Transform(ST_Point(51.4271, 7.6639), 'EPSG:4326', 'EPSG:25832'), 500))
LIMIT 5;
-- id | m2
-- 9627372 | 14990.0
-- 9710739 | 7673.0
-- 9710688 | 3053.0
-- 9627367 | 1498.0
-- 9627383 | 2642.0
```

## Related collections

Every collection in this catalog shares the fiboa core columns, so the same queries work across countries; `s3://ftw/harmonized-field-data/*/latest/*.parquet` with `union_by_name = true` reads the newest edition of all of them (see the catalog [AGENTS.md](https://source.coop/ftw/harmonized-field-data/AGENTS.md)).

## Structure

Assets and structural links resolve relative to the object that carries them; there is no `self` link. Source: this collection is generated by [tools/catalogize.py](https://github.com/fieldsoftheworld/harmonized-field-data-catalog/blob/main/tools/catalogize.py) in the catalog repository — fix documentation there.
