# Field blocks for Saxony, Germany

Feldblöcke und förderfähige Elemente in Sachsen 2026

- **Source data provider:** [Sächsisches Landesamt für Umwelt, Landwirtschaft und Geologie](https://geoportal.sachsen.de)
- **License:** DL-DE-BY-2.0
- **Editions:** 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 95,305
- **Coordinate reference system:** EPSG:25833 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.3.1 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/de_sax.py))
- **Data survey:** [DE-SAX.md](https://github.com/fiboa/data-survey/blob/main/data/DE-SAX.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/de_sax/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_sax/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2026 | 95,305 | [69.1 MB](https://data.source.coop/ftw/harmonized-field-data/de_sax/year=2026/de_sax.parquet) | [31.1 MB](https://data.source.coop/ftw/harmonized-field-data/de_sax/year=2026/de_sax.pmtiles) | [de_sax-2026.json](https://data.source.coop/ftw/harmonized-field-data/de_sax/year=2026/de_sax-2026.json) |

The latest edition is also available at a stable path: [de_sax/latest/de_sax.parquet](https://data.source.coop/ftw/harmonized-field-data/de_sax/latest/de_sax.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/de_sax/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_sax/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `FB_BEZEICH` | string | Descriptive label (per the fiboa data survey) |
| `WT_WRRL` | bool | Water Framework Directive water body (per the fiboa data survey) |
| `FB_SPA` | bool | Inside a Special Protection Area (SPA) (per the fiboa data survey) |
| `REG_SAAT` | string | Regional seed code (per the fiboa data survey) |
| `GLOEZ2` | bool | GLOEZ-2 (permanent grassland) restriction (per the fiboa data survey) |
| `BERG` | uint8 | Mountain-area classification (per the fiboa data survey) |
| `AGROFORST` | bool | Agroforestry registered (per the fiboa data survey) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `AGRIPV` | bool | Agri-photovoltaic installation (per the fiboa data survey) |
| `NITRAT_TG` | bool | Nitrate-sensitive partial area (per the fiboa data survey) |
| `KWASSER` | uint8 | Water-erosion class (per the fiboa data survey) |
| `FB_FFH` | bool | Inside an FFH (Natura 2000) area (per the fiboa data survey) |
| `FB_BN_KAT` | string | Land-use category (Bodennutzungskategorie) (per the fiboa data survey) |
| `ZUSTAENDIG` | uint8 | Responsible authority code (per the fiboa data survey) |
| `OER_UNZUL` | string | "Öko-Regelung unzulässig" remark (per the fiboa data survey) |
| `NITRAT` | bool | Nitrate-vulnerable zone (per the fiboa data survey) |
| `KWIND` | uint8 | Wind-erosion class (per the fiboa data survey) |
| `FB_NB` | string | Nature-protection remarks (per the fiboa data survey) |
| `flik` | string | The area identifier (FLIK code) is a 16-character string. ([spec](https://github.com/fiboa/flik-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2026-01-01T00:00:00Z`
- `admin:country_code`: `DE`
- `admin:subdivision_code`: `SN`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/de_sax/latest/de_sax.parquet');
-- fields | hectares
-- 95305 | 925788.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Sächsisches Landesamt für Umwelt, Landwirtschaft und Geologie](https://geoportal.sachsen.de) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.3.1:

- 2026: converted 2026-09-27 from <https://www.smul.sachsen.de/gis-online/download/FBZ_ISS_Bereiche/gesamt_2026_RE.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

DL-DE-BY-2.0. Attribution: Sächsisches Landesamt für Umwelt, Landwirtschaft und Geologie
