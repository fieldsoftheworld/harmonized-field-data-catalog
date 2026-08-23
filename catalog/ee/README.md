# Field boundaries for Estonia

Geospatial Aid Application Estonia Agricultural parcels.
The original dataset is provided by ARIB and obtained from the INSPIRE theme GSAA (specifically Geospaial Aid Application Estonia Agricultural parcels) through which the data layer Fields and Eco Areas (GSAA) is made available.
The data comes from ARIB's database of agricultural parcels.

- **Source data provider:** [Põllumajanduse Registrite ja Informatsiooni Amet](http://data.europa.eu/88u/dataset/pria-pollud)
- **License:** CC-BY-SA-3.0
- **Editions:** 2024 (one GeoParquet per year)
- **Fields in the latest edition (2024):** 166,508
- **Coordinate reference system:** EPSG:3301 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ee.py))
- **Data survey:** [EE.md](https://github.com/fiboa/data-survey/blob/main/data/EE.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/ee/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ee/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2024 | 166,508 | [250.7 MB](https://data.source.coop/ftw/harmonized-field-data/ee/year=2024/ee-2024.parquet) | [67.3 MB](https://data.source.coop/ftw/harmonized-field-data/ee/year=2024/ee-2024.pmtiles) | [ee-2024.json](https://data.source.coop/ftw/harmonized-field-data/ee/year=2024/ee-2024.json) |

The latest edition is also available at a stable path: [ee/latest/ee.parquet](https://data.source.coop/ftw/harmonized-field-data/ee/latest/ee.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/ee/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ee/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2024-01-01T00:00:00Z`
- `crop:code_list`: `https://fiboa.org/code/ee/ee.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/ee/latest/ee.parquet');
-- fields | hectares
-- 166508 | 938538.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Põllumajanduse Registrite ja Informatsiooni Amet](http://data.europa.eu/88u/dataset/pria-pollud) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2024: converted 2026-08-22 from <https://kls.pria.ee/geoserver/inspire_gsaa/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=inspire_gsaa:LU.GSAA.AGRICULTURAL_PARCELS_2024&propertyName=geom,pollu_id,taotlusaasta,pindala_ha,taotletud_kultuur>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-SA-3.0. Attribution: © Põllumajanduse Registrite ja Informatsiooni Amet
