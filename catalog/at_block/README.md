# Field boundaries for Austria

**Field boundaries for Austria - INVEKOS Referenzen Österreich 2021.**

The layer includes all reference parcels ("Referenzparzellen") defined by the paying agency Agrarmarkt Austria and recorded landscape elements (landscape element layers) within the meaning of Art. 5 of Regulation (EU) No. 640/2014 and Regulation of the competent federal ministry with horizontal rules for the area of the Common Agricultural Policy (Horizontal CAP Regulation) StF: Federal Law Gazette II No. 100/2015.

Reference parcel: is the physical block that can be clearly delimited from the outside (e.g. forest, roads, water bodies) and is formed by contiguous agricultural areas that are recognizable in nature.

- **Source data provider:** [Agrarmarkt Austria](https://geometadatensuche.inspire.gv.at/metadatensuche/inspire/api/records/9db8a0c3-e92a-4df4-9d55-8210e326a7ed)
- **License:** CC-BY-4.0
- **Editions:** 2021 (one GeoParquet per year)
- **Fields in the latest edition (2021):** 1,299,755
- **Coordinate reference system:** EPSG:31287 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/at_block.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/at_block/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/at_block/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2021 | 1,299,755 | [467.5 MB](https://data.source.coop/ftw/harmonized-field-data/at_block/year=2021/at_block.parquet) | [244.1 MB](https://data.source.coop/ftw/harmonized-field-data/at_block/year=2021/at_block.pmtiles) | [at_block-2021.json](https://data.source.coop/ftw/harmonized-field-data/at_block/year=2021/at_block-2021.json) |

The latest edition is also available at a stable path: [at_block/latest/at_block.parquet](https://data.source.coop/ftw/harmonized-field-data/at_block/latest/at_block.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/at_block/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/at_block/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `referenz_kennung` | uint64 | Carried over from the source column `REFERENZ_KENNUNG`; the publisher documents no meaning for it. |
| `ref_art_bezeichnung` | string | Carried over from the source column `REF_ART_BEZEICHNUNG`; the publisher documents no meaning for it. |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `inspire:id` | string | INSPIRE-compliant ID, an absolute and fully resolvable URI. ([spec](https://github.com/fiboa/inspire-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `ref_art` | string | Carried over from the source column `REF_ART`; the publisher documents no meaning for it. |
| `determination:datetime` | timestamp[ms, tz=UTC] | The last timestamp at which the field did exist and was observed. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `fart_id`: `1696.0`
- `admin:country_code`: `AT`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/at_block/latest/at_block.parquet');
-- fields | hectares
-- 1299755 | 3293939.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Agrarmarkt Austria](https://geometadatensuche.inspire.gv.at/metadatensuche/inspire/api/records/9db8a0c3-e92a-4df4-9d55-8210e326a7ed) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2021: converted 2026-08-23 from <https://inspire.lfrz.gv.at/009501/ds/inspire_referenzen_2021_polygon.gpkg.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribute the data to Agrarmarkt Austria.
