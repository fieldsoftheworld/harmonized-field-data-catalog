# Field boundaries for Thuringia, Germany

For use in the application procedure of the Integrated Administration and Control System (IACS), digital data layers are required that represent the current situation of agricultural use with the required accuracy. The field block is a contiguous agricultural area of one or more farmers surrounded by permanent boundaries. The field block thus contains information on the geographical location of the outer boundaries of the agricultural area. Reference parcels are uniquely numbered throughout Germany (Feldblockident - FBI). They also have a field block size (maximum eligible area) and a land use category.

The following field block types exist:

- Utilized agricultural area (UAA)
- Landscape elements (LE)
- Special use areas (SF)
- Forest areas (FF)

The field blocks are classified separately according to the main land uses of arable land (`AL`), grassland (`GL`), permanent crops (`DA`, `OB`, `WB`), including agroforestry systems with an approved utilization concept and according to the BNK for no "agricultural land" (`NW`, `EF` and `PK`) and others.

Landscape elements (LE) are considered part of the eligible agricultural area under defined conditions. In Thuringia, these permanent conditional features are designated as a separate field block (FB) and are therefore part of the Thuringian area reference system (field block reference). They must have a clear reference to an UAA (agricultural land), i.e. they are located within an arable, permanent grassland or permanent crop area or border directly on it.

To produce the DGK-Lw, (official) orthophotos from the Thuringian Land Registry and Surveying Administration (TLBG) and orthophotos from the TLLLR's own aerial surveys are interpreted. The origin of this image data is 50% of the state area each year, so that up-to-date image data is available for the entire Thuringian state area every year.

- **Source data provider:** [Thüringer Landesamt für Landwirtschaft und Ländlichen Raum](https://geomis.geoportal-th.de/geonetwork/srv/ger/catalog.search#/metadata/D872F2D6-60BC-11D6-B67D-00E0290F5BA0)
- **License:** DL-DE-BY-2.0
- **Editions:** 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 102,076
- **Coordinate reference system:** EPSG:25832 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/de_th.py))
- **Data survey:** [DE-TH.md](https://github.com/fiboa/data-survey/blob/main/data/DE-TH.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/de_th/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_th/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2026 | 102,076 | [81.7 MB](https://data.source.coop/ftw/harmonized-field-data/de_th/year=2026/de_th.parquet) | [36.5 MB](https://data.source.coop/ftw/harmonized-field-data/de_th/year=2026/de_th.pmtiles) | [de_th-2026.json](https://data.source.coop/ftw/harmonized-field-data/de_th/year=2026/de_th-2026.json) |

The latest edition is also available at a stable path: [de_th/latest/de_th.parquet](https://data.source.coop/ftw/harmonized-field-data/de_th/latest/de_th.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/de_th/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_th/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `tk10` | string | Sheet of the 1:10,000 topographic map covering the centroid of the field block. Example: `51334` (source column `TK10`, per the fiboa data survey) |
| `determination:datetime` | timestamp[ms, tz=UTC] | The last timestamp at which the field did exist and was observed. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `change` | bool | Whether the field block changed since the previous update: `Geaendert` → true, `Unveraendert` → false, `Neu` → null (source column `AENDERUNG`, per the fiboa data survey) |
| `flik` | string | The area identifier (FLIK code) is a 16-character string. ([spec](https://github.com/fiboa/flik-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `flik_last_year` | list<element: string> | FLIK identifier(s) of the previous year, split on `,` (source column `FBI_VJ`, per the fiboa data survey) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `area_last_year` | float | Area in the previous year, in ha (source column `FB_FL_VJ`, per the fiboa data survey) |
| `bnk` | string | Category of main land use, short code (source column `BNK`, per the fiboa data survey) |
| `afo` | bool | Whether the field block is an agroforestry system (`J` → true, otherwise false) (source column `AFO`, per the fiboa data survey) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `valid_year`: `2026`
- `kond_le`: `False`
- `admin:country_code`: `DE`
- `admin:subdivision_code`: `TH`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/de_th/latest/de_th.parquet');
-- fields | hectares
-- 102076 | 801996.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Thüringer Landesamt für Landwirtschaft und Ländlichen Raum](https://geomis.geoportal-th.de/geonetwork/srv/ger/catalog.search#/metadata/D872F2D6-60BC-11D6-B67D-00E0290F5BA0) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2026: converted 2026-08-22 from <https://www.geoproxy.geoportal-th.de/download-service/opendata/agrar/DGK_Thue.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

DL-DE-BY-2.0. Attribution: © GDI-Th
