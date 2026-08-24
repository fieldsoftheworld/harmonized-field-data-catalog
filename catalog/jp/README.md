# Japan Fude Parcels

Japanese Farmland Parcel Polygons (Fude Polygons in Japanese) represent parcel information of farmland.
The polygons are manually digitized data derived from aerial imagery, such as satellite images. Since no
on-site verification or similar procedures have been conducted, the data may not necessarily match the actual
current conditions. Fude Polygons are created for the purpose of roughly indicating the locations of farmland.

- **Source data provider:** [Japanese Ministry of Agriculture, Forestry and Fisheries (MAFF, 農林水産省)](https://www.maff.go.jp/)
- **License:** CC-BY-4.0
- **Editions:** 2021, 2022, 2023, 2024 (one GeoParquet per year)
- **Fields in the latest edition (2024):** 29,418,076
- **Coordinate reference system:** EPSG:4326 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/jp.py))
- **Data survey:** [JP.md](https://github.com/fiboa/data-survey/blob/main/data/JP.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/jp/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/jp/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2021 | 30,165,774 | [5.9 GB](https://data.source.coop/ftw/harmonized-field-data/jp/year=2021/jp-2021.parquet) | — | [jp-2021.json](https://data.source.coop/ftw/harmonized-field-data/jp/year=2021/jp-2021.json) |
| 2022 | 29,778,783 | [5.8 GB](https://data.source.coop/ftw/harmonized-field-data/jp/year=2022/jp-2022.parquet) | — | [jp-2022.json](https://data.source.coop/ftw/harmonized-field-data/jp/year=2022/jp-2022.json) |
| 2023 | 29,673,005 | [5.8 GB](https://data.source.coop/ftw/harmonized-field-data/jp/year=2023/jp-2023.parquet) | — | [jp-2023.json](https://data.source.coop/ftw/harmonized-field-data/jp/year=2023/jp-2023.json) |
| 2024 | 29,418,076 | [5.8 GB](https://data.source.coop/ftw/harmonized-field-data/jp/year=2024/jp-2024.parquet) | [3.2 GB](https://data.source.coop/ftw/harmonized-field-data/jp/year=2024/jp-2024.pmtiles) | [jp-2024.json](https://data.source.coop/ftw/harmonized-field-data/jp/year=2024/jp-2024.json) |

The latest edition is also available at a stable path: [jp/latest/jp.parquet](https://data.source.coop/ftw/harmonized-field-data/jp/latest/jp.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/jp/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/jp/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `land_type_en` | string | land_typeコードの英語表記（rice_field または field） (per the fiboa data survey) |
| `admin_local_code` | string | ポリゴンの重心点と重なる市区町村の総務省地方公共団体コード (source column `local_government_cd`, per the fiboa data survey) |
| `determination:datetime` | timestamp[us, tz=UTC] | The last timestamp at which the field did exist and was observed. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/jp/latest/jp.parquet');
-- fields
-- 29418076
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Japanese Ministry of Agriculture, Forestry and Fisheries (MAFF, 農林水産省)](https://www.maff.go.jp/) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2021: converted 2026-08-24 from <https://data.source.coop/pacificspatial/field-polygon-jp/parquet/jp_field_polygons_2021.parquet>
- 2022: converted 2026-08-24 from <https://data.source.coop/pacificspatial/field-polygon-jp/parquet/jp_field_polygons_2022.parquet>
- 2023: converted 2026-08-24 from <https://data.source.coop/pacificspatial/field-polygon-jp/parquet/jp_field_polygons_2023.parquet>
- 2024: converted 2026-08-24 from <https://data.source.coop/pacificspatial/field-polygon-jp/parquet/jp_field_polygons_2024.parquet>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: Fude Polygon Data (2021-2024). Japanese Ministry of Agriculture, Forestry and Fisheries. Processed by Pacific Spatial Solutions, Inc
