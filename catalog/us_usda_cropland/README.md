# U.S. Department of Agriculture Crop Sequence Boundaries

The Crop Sequence Boundaries (CSB) developed with USDA's Economic Research Service, produces estimates of field boundaries, crop acreage, and crop rotations across the contiguous United States. It uses satellite imagery with other public data and is open source allowing users to conduct area and statistical analysis of planted U.S. commodities and provides insight on farmer cropping decisions.

NASS needed a representative field to predict crop planting based on common crop rotations such as corn-soy and ERS is using this product to study changes in farm management practices like tillage or cover cropping over time.

CSB represents non-confidential single crop field boundaries over a set time frame. It does not contain personal identifying information. The boundaries captured are of crops grown only, not ownership boundaries or tax parcels (unit of property). The data are from satellite imagery and publicly available data, it does not come from producers or agencies like the Farm Service Agency.

- **Source data provider:** [United States Department of Agriculture](https://www.nass.usda.gov)
- **License:** other — [License and Liability](https://gee-community-catalog.org/projects/csb/#license-and-liability) (converter: `License and Liability <https://gee-community-catalog.org/projects/csb/#license-and-liability>`)
- **Editions:** 2024 (one GeoParquet per year)
- **Fields in the latest edition (2024):** 7,522,713
- **Coordinate reference system:** None (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/us_usda_cropland.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/us_usda_cropland/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/us_usda_cropland/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2024 | 7,522,713 | [2.8 GB](https://data.source.coop/ftw/harmonized-field-data/us_usda_cropland/year=2024/us_usda_cropland-2024.parquet) | [658.4 MB](https://data.source.coop/ftw/harmonized-field-data/us_usda_cropland/year=2024/us_usda_cropland-2024.pmtiles) | [us_usda_cropland-2024.json](https://data.source.coop/ftw/harmonized-field-data/us_usda_cropland/year=2024/us_usda_cropland-2024.json) |

The latest edition is also available at a stable path: [us_usda_cropland/latest/us_usda_cropland.parquet](https://data.source.coop/ftw/harmonized-field-data/us_usda_cropland/latest/us_usda_cropland.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/us_usda_cropland/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/us_usda_cropland/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `administrative_area_level_2` | string | Carried over from the source column `CNTY`; the publisher documents no meaning for it. |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2023-05-01T00:00:00Z`
- `admin:country_code`: `US`
- `crop:code_list`: `https://fiboa.org/code/us/usda/cropland.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/us_usda_cropland/latest/us_usda_cropland.parquet');
-- fields
-- 7522713
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [United States Department of Agriculture](https://www.nass.usda.gov) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2024: converted 2026-08-24 from <https://www.nass.usda.gov/Research_and_Science/Crop-Sequence-Boundaries/datasets/NationalCSB_2017-2024_rev23.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

other — [License and Liability](https://gee-community-catalog.org/projects/csb/#license-and-liability) (converter: `License and Liability <https://gee-community-catalog.org/projects/csb/#license-and-liability>`). Attribute the data to United States Department of Agriculture.
