# Crop-cut farm polygons with crop type and yield for Kenya (ECAAS Bird's-Eye)

Farm polygons from crop-cutting experiments of the Bird's-Eye project, a collaboration between Pula
and Tetra Tech under the Enabling Crop Analytics at Scale (ECAAS) project, funded by the Bill &
Melinda Gates Foundation. Enumerators visited smallholder farms, walked the boundary of the crop in
question with a GPS device and placed harvest boxes (mostly 8 by 5 m) inside it; the boxes were
harvested and weighed (kg) and the weight converted to a yield per hectare. Geospatial experts then
checked the polygons against satellite imagery and corrected those that did not fit the farm.
The polygons are a sample of farms, not a wall-to-wall map. Each one carries the crop, the planting
and harvest dates, the season, the crop condition at box placement, whether and with what the crop
was intercropped, and the harvested weight and yield.

- **Source data provider:** [Pula Advisors](https://ecass-project-documentation.readthedocs.io/en/latest/modules/data_access.html)
- **License:** GPL-2.0-or-later
- **Editions:** 2021 (one GeoParquet per year)
- **Fields in the latest edition (2021):** 1,349
- **Coordinate reference system:** EPSG:4326 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.30.0, vecorel-cli 0.4.2 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ke_ecaas.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/ke_ecaas/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ke_ecaas/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2021 | 1,349 | [205.2 KB](https://data.source.coop/ftw/harmonized-field-data/ke_ecaas/year=2021/ke_ecaas-2021.parquet) | [433.6 KB](https://data.source.coop/ftw/harmonized-field-data/ke_ecaas/year=2021/ke_ecaas-2021.pmtiles) | [ke_ecaas-2021.json](https://data.source.coop/ftw/harmonized-field-data/ke_ecaas/year=2021/ke_ecaas-2021.json) |

The latest edition is also available at a stable path: [ke_ecaas/latest/ke_ecaas.parquet](https://data.source.coop/ftw/harmonized-field-data/ke_ecaas/latest/ke_ecaas.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/ke_ecaas/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ke_ecaas/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `planting_date` | date32[day] | Carried over from the source column `Planting_Date`; the publisher documents no meaning for it. |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `harvest_weight` | double | Carried over from the source column `Final_Weight`; the publisher documents no meaning for it. |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `admin_level_2` | string | Carried over from the source column `ADM2`; the publisher documents no meaning for it. |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `harvest_date` | date32[day] | Carried over from the source column `Harvesting_date`; the publisher documents no meaning for it. |
| `yield` | double | Carried over from the source column `Yield(Mt/ha)`; the publisher documents no meaning for it. |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop_condition` | string | Source-specific column; the publisher documents no meaning for it. |
| `intercrop` | string | Carried over from the source column `inter_with_which_crop`; the publisher documents no meaning for it. |
| `admin_level_1` | string | Carried over from the source column `ADM1`; the publisher documents no meaning for it. |
| `intercropped` | bool | Carried over from the source column `Intercropping`; the publisher documents no meaning for it. |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `season` | string | Source-specific column; the publisher documents no meaning for it. |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `KE`
- `crop:code_list`: `https://fiboa.org/code/ke/ecaas/crop.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/ke_ecaas/latest/ke_ecaas.parquet');
-- fields | hectares
-- 1349 | 336.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Pula Advisors](https://ecass-project-documentation.readthedocs.io/en/latest/modules/data_access.html) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.30.0, vecorel-cli 0.4.2:

- 2021: converted 2026-11-05 from <https://drive.usercontent.google.com/download?id=1z4ysK3Ezk7oDjf658pzMNcCDO06_Gk6S&export=download>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

GPL-2.0-or-later. Attribution: Pula Advisors and Tetra Tech, Bird's-Eye project, Enabling Crop Analytics at Scale (ECAAS)
