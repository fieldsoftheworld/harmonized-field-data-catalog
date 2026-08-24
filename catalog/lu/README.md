# Luxembourg FLIK Parcels

The Land Parcel Identification System (LPIS) is a reference database of the agriculture parcels used as a basis for area-related payments to farmers in relation to the Common Agricultural Policy (CAP). These payments are (co)financed by the European Agricultural Guarantee Fund (‘EAGF’) and the European Agricultural Fund for Rural Development (‘EAFRD’).

To ensure that payments are regular, the CAP relies on the Integrated Administration and Control System (IACS), a set of comprehensive administrative and on-the-spot checks on subsidy applications, which is managed by the Member States. The Land Parcel Identification System (LPIS) is a key component of the IACS. It is an IT system based on ortho imagery (aerial or satellite photographs) which records all agricultural parcels in the Member States.

- **Source data provider:** [Administration des services techniques de l'agriculture](https://asta.etat.lu/en)
- **License:** CC-BY-4.0
- **Editions:** 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 87,997
- **Coordinate reference system:** EPSG:2169 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/lu.py))
- **Data survey:** [LU.md](https://github.com/fiboa/data-survey/blob/main/data/LU.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/lu/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/lu/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2026 | 87,997 | [20.4 MB](https://data.source.coop/ftw/harmonized-field-data/lu/year=2026/lu.parquet) | [9.8 MB](https://data.source.coop/ftw/harmonized-field-data/lu/year=2026/lu.pmtiles) | [lu-2026.json](https://data.source.coop/ftw/harmonized-field-data/lu/year=2026/lu-2026.json) |

The latest edition is also available at a stable path: [lu/latest/lu.parquet](https://data.source.coop/ftw/harmonized-field-data/lu/latest/lu.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/lu/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/lu/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `LU`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/lu/latest/lu.parquet');
-- fields
-- 87997
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Administration des services techniques de l'agriculture](https://asta.etat.lu/en) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2026: converted 2026-08-23 from <https://data.public.lu/fr/datasets/r/b4ae6690-7e4c-4454-8b60-9fa33ba6a61b>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: Luxembourg ministry of Agriculture
