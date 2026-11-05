# Crop-cut farm polygons with crop type and yield for Zambia (ECAAS Bird's-Eye)

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
- **Editions:** 2022 (one GeoParquet per year)
- **Fields in the latest edition (2022):** 2,711
- **Coordinate reference system:** EPSG:4326 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.30.0, vecorel-cli 0.4.2 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/zm_ecaas.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/zm_ecaas/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/zm_ecaas/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2022 | 2,711 | [641.4 KB](https://data.source.coop/ftw/harmonized-field-data/zm_ecaas/year=2022/zm_ecaas-2022.parquet) | [3.2 MB](https://data.source.coop/ftw/harmonized-field-data/zm_ecaas/year=2022/zm_ecaas-2022.pmtiles) | [zm_ecaas-2022.json](https://data.source.coop/ftw/harmonized-field-data/zm_ecaas/year=2022/zm_ecaas-2022.json) |

The latest edition is also available at a stable path: [zm_ecaas/latest/zm_ecaas.parquet](https://data.source.coop/ftw/harmonized-field-data/zm_ecaas/latest/zm_ecaas.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/zm_ecaas/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/zm_ecaas/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `yield` | double | Carried over from the source column `Yield(Mt/ha)`; the publisher documents no meaning for it. |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `admin_level_1` | string | Carried over from the source column `ADM1`; the publisher documents no meaning for it. |
| `crop_condition` | string | Source-specific column; the publisher documents no meaning for it. |
| `intercrop` | string | Carried over from the source column `inter_with_which_crop`; the publisher documents no meaning for it. |
| `harvest_weight` | double | Carried over from the source column `Final_Weight`; the publisher documents no meaning for it. |
| `harvest_date` | date32[day] | Carried over from the source column `Harvesting_date`; the publisher documents no meaning for it. |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `intercropped` | bool | Carried over from the source column `Intercropping`; the publisher documents no meaning for it. |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `planting_date` | date32[day] | Carried over from the source column `Planting_Date`; the publisher documents no meaning for it. |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `admin_level_2` | string | Carried over from the source column `ADM2`; the publisher documents no meaning for it. |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `season`: `Main Season`
- `admin:country_code`: `ZM`
- `crop:code_list`: `https://fiboa.org/code/zm/ecaas/crop.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/zm_ecaas/latest/zm_ecaas.parquet');
-- fields | hectares
-- 2711 | 644.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Pula Advisors](https://ecass-project-documentation.readthedocs.io/en/latest/modules/data_access.html) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.30.0, vecorel-cli 0.4.2:

- 2022: converted 2026-11-05 from <https://drive.usercontent.google.com/download?id=1kl7wnGYNCxn-ATdoB_yBwefoZ4AUAW-P&export=download>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

GPL-2.0-or-later. Attribution: Pula Advisors and Tetra Tech, Bird's-Eye project, Enabling Crop Analytics at Scale (ECAAS)
