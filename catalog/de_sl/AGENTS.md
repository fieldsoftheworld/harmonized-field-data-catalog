# Agent guidance — Field boundaries for Saarland, Germany

Germany, Saarland field boundaries in the [fiboa](https://github.com/fiboa/specification) schema, 1 edition (2026). Every claim below is quoted from the source, the converter, or measured from the published files; each query was run before it was written down, and its output follows it as comments.

## Access

- Latest edition, stable path: `https://data.source.coop/ftw/harmonized-field-data/de_sl/latest/de_sl.parquet`
- One edition: `https://data.source.coop/ftw/harmonized-field-data/de_sl/year=<year>/<file>.parquet`, e.g. `https://data.source.coop/ftw/harmonized-field-data/de_sl/year=2026/de_sl-2026.parquet`
- All editions (hive partitioned): `s3://ftw/harmonized-field-data/de_sl/year=*/*.parquet` — the S3 form of the same prefix through the Source Cooperative proxy, because `*` needs a listing that plain https does not provide. In DuckDB: `CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');` then `read_parquet(glob, hive_partitioning = true)` adds the `year` column. No credentials are needed.
- PMTiles for maps: `https://data.source.coop/ftw/harmonized-field-data/de_sl/year=2026/de_sl-2026.pmtiles`, layer `de_sl`; MapLibre styles in `styles/`.

## Quirks that produce silently wrong answers

- **CRS is EPSG:4258, not WGS84.** `ST_Area`/`ST_Distance` return units of that CRS; transform with `ST_Transform` if you need lon/lat, or use `metrics:area`.
- **`metrics:area` is in square metres**, computed by the converter from the geometry (EPSG:6933 when the CRS is not metric). Divide by 10 000 for hectares.
- **`year` is the year the boundaries represent**: the declaration year or season of a register, the year a snapshot was taken, or (for a source covering several years) the year of each field's own `determination:datetime`. `determination:datetime`, where present, is the source's own date for a field.
- **`id` is only guaranteed unique within one edition** (fiboa requires uniqueness per file; it is the source column `identifier`). Whether an id persists across editions is not verified here; do not join editions on it without checking.
- **Some fiboa properties are not columns.** Values constant for the whole file are stored once in the GeoParquet `collection` key-value metadata: `admin:country_code` = `DE`, `admin:subdivision_code` = `SL` (2026 edition). Read them with `parquet_kv_metadata()` in DuckDB or `pyarrow.parquet.ParquetFile(f).schema_arrow.metadata[b'collection']`; they differ per edition where the source does.

## Tested queries

Fields and hectares per edition, through the partition glob:

```sql
INSTALL httpfs; LOAD httpfs;
CREATE SECRET sc (TYPE s3, PROVIDER config, ENDPOINT 'data.source.coop', URL_STYLE 'path', REGION 'us-west-2');
SELECT year, count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('s3://ftw/harmonized-field-data/de_sl/year=*/*.parquet', hive_partitioning = true)
GROUP BY year ORDER BY year;
-- year | fields | hectares
-- 2026 | 54038 | 78171.0
```

Fields within about 500 m (0.005°; the CRS is in degrees) of a point given in lon/lat, transforming the point into the data's CRS instead of the data into WGS84:

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT id, round("metrics:area") AS m2
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/de_sl/latest/de_sl.parquet')
WHERE ST_Intersects(geometry, ST_Buffer(ST_Transform(ST_Point(6.8802, 49.3735), 'EPSG:4326', 'EPSG:4258', always_xy := true), 0.005))
LIMIT 5;
-- id | m2
-- https://registry.gdi-de.org/id/de.sl.inspire.elu.invekos/ExistingLandUseObject_913d315552e1c0ea5f98c3bf972179587383d97bb6f33555c4ff689cc1463887_DESLLI03000110092265241 | 14698.0
-- https://registry.gdi-de.org/id/de.sl.inspire.elu.invekos/ExistingLandUseObject_28e47ad950aa7a7444c59dda25de3cd62579bc09dfb4917e266a3016f105014f_DESLLI03000109442270934 | 3413.0
-- https://registry.gdi-de.org/id/de.sl.inspire.elu.invekos/ExistingLandUseObject_19886f99dac9954f3c0dd0cd2b150e4d6c3b7fb1186ffa61c3ab9da492345c3f_DESLLI01001350132236398 | 2610.0
-- https://registry.gdi-de.org/id/de.sl.inspire.elu.invekos/ExistingLandUseObject_a612b25ef6a95ada61de2d93b21c52f63392e7becc45a4c204561c5cba6db066_DESLLI07000102322236407 | 4176.0
-- https://registry.gdi-de.org/id/de.sl.inspire.elu.invekos/ExistingLandUseObject_6de7077802e25a6f228161a6e599017e5813eae072de8993bc9bb1142d1a8f46_DESLLI09000102322248954 | 5415.0
```

## Related collections

Every collection in this catalog shares the fiboa core columns, so the same queries work across countries; `s3://ftw/harmonized-field-data/*/latest/*.parquet` with `union_by_name = true` reads the newest edition of all of them (see the catalog [AGENTS.md](https://source.coop/ftw/harmonized-field-data/AGENTS.md)).

## Structure

Assets and structural links resolve relative to the object that carries them; there is no `self` link. Source: this collection is generated by [tools/catalogize.py](https://github.com/fieldsoftheworld/harmonized-field-data-catalog/blob/main/tools/catalogize.py) in the catalog repository — fix documentation there.
