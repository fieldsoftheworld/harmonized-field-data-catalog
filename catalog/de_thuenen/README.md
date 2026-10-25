# Crop type map of Germany from Sentinel-1, Sentinel-2 and Landsat (Thünen Institute)

The Thünen Institute's annual map of agricultural land use in Germany: the dominant crop type or
land use of every field in the open landscape, classified from time series of Sentinel-1,
Sentinel-2 and Landsat 8 (Blickensdörfer et al., 2022). The classified raster was aggregated into
homogeneous objects (Tetteh et al., 2021, 2023), so the boundaries are inferred from imagery, not
declared by farmers. Small woody features and other areas that are no field are left out.

- **Source data provider:** [Johann Heinrich von Thünen-Institut](https://doi.org/10.5281/zenodo.10619783)
- **License:** CC-BY-4.0
- **Editions:** 2017, 2018, 2019, 2020, 2021 (one GeoParquet per year)
- **Fields in the latest edition (2021):** 5,220,733
- **Coordinate reference system:** EPSG:3035 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.4.0 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/de_thuenen.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/de_thuenen/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_thuenen/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2017 | 5,408,359 | [575.6 MB](https://data.source.coop/ftw/harmonized-field-data/de_thuenen/year=2017/de_thuenen-2017.parquet) | — | [de_thuenen-2017.json](https://data.source.coop/ftw/harmonized-field-data/de_thuenen/year=2017/de_thuenen-2017.json) |
| 2018 | 5,088,647 | [554.6 MB](https://data.source.coop/ftw/harmonized-field-data/de_thuenen/year=2018/de_thuenen-2018.parquet) | — | [de_thuenen-2018.json](https://data.source.coop/ftw/harmonized-field-data/de_thuenen/year=2018/de_thuenen-2018.json) |
| 2019 | 5,198,905 | [560.9 MB](https://data.source.coop/ftw/harmonized-field-data/de_thuenen/year=2019/de_thuenen-2019.parquet) | — | [de_thuenen-2019.json](https://data.source.coop/ftw/harmonized-field-data/de_thuenen/year=2019/de_thuenen-2019.json) |
| 2020 | 5,216,144 | [561.5 MB](https://data.source.coop/ftw/harmonized-field-data/de_thuenen/year=2020/de_thuenen-2020.parquet) | — | [de_thuenen-2020.json](https://data.source.coop/ftw/harmonized-field-data/de_thuenen/year=2020/de_thuenen-2020.json) |
| 2021 | 5,220,733 | [560.7 MB](https://data.source.coop/ftw/harmonized-field-data/de_thuenen/year=2021/de_thuenen-2021.parquet) | [449.8 MB](https://data.source.coop/ftw/harmonized-field-data/de_thuenen/year=2021/de_thuenen-2021.pmtiles) | [de_thuenen-2021.json](https://data.source.coop/ftw/harmonized-field-data/de_thuenen/year=2021/de_thuenen-2021.json) |

The latest edition is also available at a stable path: [de_thuenen/latest/de_thuenen.parquet](https://data.source.coop/ftw/harmonized-field-data/de_thuenen/latest/de_thuenen.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/de_thuenen/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_thuenen/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `DE`
- `determination:datetime`: `2021-01-01T00:00:00Z`
- `crop:code_list`: `https://fiboa.org/code/de/thuenen/ctm.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/de_thuenen/latest/de_thuenen.parquet');
-- fields | hectares
-- 5220733 | 17436742.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Johann Heinrich von Thünen-Institut](https://doi.org/10.5281/zenodo.10619783) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.4.0:

- 2017: converted 2026-10-23 from <https://zenodo.org/api/records/10619783/files/CTM_GER_2017_seg_v201.fgb/content>
- 2018: converted 2026-10-23 from <https://zenodo.org/api/records/10619783/files/CTM_GER_2018_seg_v201.fgb/content>
- 2019: converted 2026-10-23 from <https://zenodo.org/api/records/10619783/files/CTM_GER_2019_seg_v201.fgb/content>
- 2020: converted 2026-10-23 from <https://zenodo.org/api/records/10619783/files/CTM_GER_2020_seg_v201.fgb/content>
- 2021: converted 2026-10-23 from <https://zenodo.org/api/records/10619783/files/CTM_GER_2021_seg_v201.fgb/content>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: Tetteh, G.O., Schwieder, M., Blickensdörfer, L., Gocht, A., Erasmi, S. (2024): Agricultural land use (vector): National-scale crop type maps for Germany, v201, Thünen-Institut, doi:10.5281/zenodo.10619783
