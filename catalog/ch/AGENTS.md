# Agent guidance — Field boundaries for Switzerland

Field boundaries in the [fiboa](https://github.com/fiboa/specification) schema from 20 sources, each with its own fiboa-cli converter and terms, 40 editions (2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026). Every claim below is quoted from the source, the converters, or measured from the published files; each query was run before it was written down, and its output follows it as comments.

## Access

- Newest edition of one source, stable path: `https://data.source.coop/ftw/harmonized-field-data/ch/latest/<converter>.parquet`, e.g. `https://data.source.coop/ftw/harmonized-field-data/ch/latest/ch_ag.parquet`. Converters: `ch_ag`, `ch_ai`, `ch_ar`, `ch_be`, `ch_bl`, `ch_fr`, `ch_ge`, `ch_gl`, `ch_gr`, `ch_ju`, `ch_lu`, `ch_sg`, `ch_sh`, `ch_so`, `ch_sz`, `ch_tg`, `ch_ur`, `ch_vs`, `ch_zg`, `ch_zh`.
- Newest edition of every source: `s3://ftw/harmonized-field-data/ch/latest/*.parquet`, and every edition: `s3://ftw/harmonized-field-data/ch/year=*/*.parquet` — the S3 form of the same prefix through the Source Cooperative proxy, because `*` needs a listing that plain https does not provide. In DuckDB: `CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');` then `read_parquet(glob, union_by_name = true, filename = true)`; `hive_partitioning = true` adds the `year` column. No credentials are needed.
- One edition: `https://data.source.coop/ftw/harmonized-field-data/ch/year=<year>/<converter>-<year>.parquet`, e.g. `https://data.source.coop/ftw/harmonized-field-data/ch/year=2025/ch_ag-2025.parquet`
- PMTiles for maps: `https://data.source.coop/ftw/harmonized-field-data/ch/latest/ch.pmtiles`, layer `ch`, the newest edition of every source; MapLibre styles in `styles/`.

## Quirks that produce silently wrong answers

- **The terms differ per source.** The collection's `license` is `other`; the terms of a row are those of its file's STAC item (`license`, `attribution`, `providers`): `ch_ag` CC-BY-4.0; `ch_ai` CC-BY-4.0; `ch_ar` CC0-1.0; `ch_be` CC-BY-4.0; `ch_bl` CC-BY-4.0; `ch_fr` CC-BY-4.0; `ch_ge` CC-BY-4.0; `ch_gl` CC0-1.0; `ch_gr` other — [Nutzungsbestimmungen für Geodaten](https://geo.gr.ch/geodaten/nutzungsbedingungen); `ch_ju` CC-BY-4.0; `ch_lu` CC-BY-4.0; `ch_sg` other — [Nutzungsbedingungen für Geodaten](https://www.sg.ch/bauen/geoinformation/datenbezug/agb.html); `ch_sh` CC0-1.0; `ch_so` CC0-1.0; `ch_sz` CC-BY-4.0; `ch_tg` CC-BY-4.0; `ch_ur` CC-BY-4.0; `ch_vs` CC-BY-4.0; `ch_zg` CC-BY-4.0; `ch_zh` CC0-1.0.
- **The files do not have the same columns.** A value that is the same for every field of a file is stored once in its GeoParquet `collection` metadata instead of as a column (read it with `parquet_kv_metadata()`), so read the files with `union_by_name = true` and take the source from the file name (`filename = true`).
- **CRS is EPSG:2056, not WGS84.** `ST_Area`/`ST_Distance` return units of that CRS; transform with `ST_Transform` if you need lon/lat, or use `metrics:area`.
- **`metrics:area` is in square metres.** Divide by 10 000 for hectares.
- **`year` is the edition, not the observation date.** For a converter with variants it is the variant; a source without variants is converted once and filed under the most frequent year of its `determination:datetime`, and its item says when the file holds other years too.
- **`id` is only guaranteed unique within one file** (fiboa requires uniqueness per file). Whether an id persists across editions is not verified here; do not join editions on it without checking.
- **`hcat:code` is hierarchical.** The first 4/6/8 digits are increasingly specific crop groups; compare prefixes, not equality, to aggregate (see the crop query below). 284 of the 1,520,805 rows of the newest editions (0.02%) have none, so a query that filters or groups on crop silently leaves them out.
- **Switzerland, Geneva:** The current year (2026) is provisional until December.

## Tested queries

Fields and hectares per edition and source, through the partition glob:

```sql
INSTALL httpfs; LOAD httpfs;
CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');
SELECT year, regexp_extract(filename, '([^/]+)-[0-9]{4}\.parquet$', 1) AS source, count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('s3://ftw/harmonized-field-data/ch/year=*/*.parquet', hive_partitioning = true, union_by_name = true, filename = true)
GROUP BY 1, 2 ORDER BY 1, 2;
-- year | source | fields | hectares
-- 2017 | ch_ge | 9519 | 11685.0
-- 2017 | ch_zh | 11777 | 7809.0
-- 2018 | ch_ge | 9695 | 11712.0
-- 2018 | ch_zh | 63987 | 43563.0
-- 2019 | ch_ge | 9619 | 11563.0
-- 2019 | ch_zh | 101690 | 67977.0
-- 2020 | ch_ge | 9732 | 11533.0
-- 2020 | ch_zh | 106152 | 69205.0
-- ... 32 more rows
```

Largest crop groups in the newest edition of every source (HCAT level 3 = first 6 digits):

```sql
INSTALL httpfs; LOAD httpfs;
CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');
SELECT substr(CAST("hcat:code" AS VARCHAR), 1, 6) AS hcat_group, mode("hcat:name") AS most_common_name,
       count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('s3://ftw/harmonized-field-data/ch/latest/*.parquet', union_by_name = true)
WHERE "hcat:code" IS NOT NULL
GROUP BY 1 ORDER BY hectares DESC LIMIT 5;
-- hcat_group | most_common_name | fields | hectares
-- 330200 | pasture_meadow_grassland_grass | 1027201 | 882129.0
-- 330109 | temporary_grass | 140902 | 148968.0
-- 330101 | winter_common_soft_wheat | 79123 | 106600.0
-- 330106 | rapeseed_rape | 13503 | 20798.0
-- 330600 | tree_wood_forest | 15794 | 16351.0
```

Fields around a point in the largest source (Switzerland, Valais), transforming the point into the data's CRS instead of the data into WGS84:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT id, round("metrics:area") AS m2
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/ch/latest/ch_vs.parquet')
WHERE ST_Intersects(geometry, ST_Buffer(ST_Transform(ST_Point(46.2641, 7.5795), 'EPSG:4326', 'EPSG:2056'), 500))
LIMIT 5;
-- id | m2
-- VS-0050569D8BFE1EED8A881DCFA548D522 | 6081.0
-- VS-0050569D8BFE1EDEB4F6155525000000 | 1241.0
-- VS-0050569D8BFE1EDEB4F6A01820CA4000 | 986.0
-- VS-0050569D8BFE1EDDADB801EA659980C7 | 319.0
-- VS-0050569D8BFE1EDDADB9F9976CBAE0C7 | 800.0
```

## Related collections

Every collection in this catalog shares the fiboa core columns, so the same queries work across countries; `s3://ftw/harmonized-field-data/*/latest/*.parquet` with `union_by_name = true` reads the newest edition of all of them (see the catalog [AGENTS.md](https://source.coop/ftw/harmonized-field-data/AGENTS.md)).

## Structure

Assets and structural links resolve relative to the object that carries them; there is no `self` link. Source: this collection is generated by [tools/catalogize_parts.py](https://github.com/fieldsoftheworld/harmonized-field-data-catalog/blob/main/tools/catalogize_parts.py) in the catalog repository — fix documentation there.
