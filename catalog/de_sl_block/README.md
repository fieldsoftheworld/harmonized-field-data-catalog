# Field blocks for Saarland, Germany

The reference parcels ("Referenzschläge") of the Saarland Land Parcel Identification System (LPIS),
the reference system for area-based agricultural payments. The data is transformed into the INSPIRE
"Land Cover" data model, so each parcel carries a land cover class from the national IACS code list
alongside its FLIK. The area given is the eligible parcel size recorded in InVeKoS, not the
geometric area of the polygon. The complementary application parcels ("Antragsschläge") are
published separately.

- **Source data provider:** [Ministerium für Umwelt, Klima, Mobilität, Agrar und Verbraucherschutz](https://geoportal.saarland.de/spatial-objects/384)
- **License:** CC-BY-4.0
- **Editions:** 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 62,981
- **Coordinate reference system:** EPSG:4258 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.18 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/de_sl_block.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/de_sl_block/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_sl_block/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2026 | 62,981 | [18.6 MB](https://data.source.coop/ftw/harmonized-field-data/de_sl_block/year=2026/de_sl_block.parquet) | [14.2 MB](https://data.source.coop/ftw/harmonized-field-data/de_sl_block/year=2026/de_sl_block.pmtiles) | [de_sl_block-2026.json](https://data.source.coop/ftw/harmonized-field-data/de_sl_block/year=2026/de_sl_block-2026.json) |

The latest edition is also available at a stable path: [de_sl_block/latest/de_sl_block.parquet](https://data.source.coop/ftw/harmonized-field-data/de_sl_block/latest/de_sl_block.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/de_sl_block/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_sl_block/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `crop:name_en` | string | Crop name in English. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `flik` | string | The area identifier (FLIK code) is a 16-character string. ([spec](https://github.com/fiboa/flik-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `DE`
- `admin:subdivision_code`: `SL`
- `crop:code_list`: `https://fiboa.org/code/de/iacs/agricultural_area_type.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/de_sl_block/latest/de_sl_block.parquet');
-- fields | hectares
-- 62981 | 81450.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Ministerium für Umwelt, Klima, Mobilität, Agrar und Verbraucherschutz](https://geoportal.saarland.de/spatial-objects/384) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.18:

- 2026: converted 2026-09-16 from <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=0>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=2500>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=5000>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=7500>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=10000>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=12500>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=15000>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=17500>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=20000>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=22500>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=25000>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=27500>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=30000>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=32500>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=35000>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=37500>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=40000>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=42500>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=45000>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=47500>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=50000>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=52500>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=55000>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=57500>, <https://geoportal.saarland.de/gdi-sl/inspirewfs_Bodenbedeckung_LPIS?service=WFS&version=2.0.0&request=GetFeature&typeNames=lcv%3ALandCoverUnit&count=2500&startIndex=60000>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: © GDI-SL 2026, CC BY 4.0
