# Finnish Crop Fields (Maatalousmaa)

The Finnish Food Authority (FFA) since 2020 produces spatial data sets,
more specifically in this context the "Field parcel register" and "Agricultural parcel containing spatial data".
A set called "Agricultural land: arable land, permanent grassland or permanent crop (land use)".

- **Source data provider:** [Finnish Food Authority](https://www.ruokavirasto.fi/en/about-us/open-information/spatial-data-sets/)
- **License:** CC-BY-4.0
- **Editions:** 2020, 2021, 2022, 2023, 2024, 2025 (one GeoParquet per year)
- **Fields in the latest edition (2025):** 985,486
- **Coordinate reference system:** EPSG:3067 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.16 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/fi.py))
- **Data survey:** [FI.md](https://github.com/fiboa/data-survey/blob/main/data/FI.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/fi/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/fi/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2020 | 1,088,750 | [285.4 MB](https://data.source.coop/ftw/harmonized-field-data/fi/year=2020/fi-2020.parquet) | — | [fi-2020.json](https://data.source.coop/ftw/harmonized-field-data/fi/year=2020/fi-2020.json) |
| 2021 | 1,086,365 | [286.1 MB](https://data.source.coop/ftw/harmonized-field-data/fi/year=2021/fi-2021.parquet) | — | [fi-2021.json](https://data.source.coop/ftw/harmonized-field-data/fi/year=2021/fi-2021.json) |
| 2022 | 1,086,997 | [287.0 MB](https://data.source.coop/ftw/harmonized-field-data/fi/year=2022/fi-2022.parquet) | — | [fi-2022.json](https://data.source.coop/ftw/harmonized-field-data/fi/year=2022/fi-2022.json) |
| 2023 | 1,006,588 | [274.1 MB](https://data.source.coop/ftw/harmonized-field-data/fi/year=2023/fi-2023.parquet) | — | [fi-2023.json](https://data.source.coop/ftw/harmonized-field-data/fi/year=2023/fi-2023.json) |
| 2024 | 998,336 | [273.8 MB](https://data.source.coop/ftw/harmonized-field-data/fi/year=2024/fi-2024.parquet) | — | [fi-2024.json](https://data.source.coop/ftw/harmonized-field-data/fi/year=2024/fi-2024.json) |
| 2025 | 985,486 | [273.5 MB](https://data.source.coop/ftw/harmonized-field-data/fi/year=2025/fi-2025.parquet) | [150.1 MB](https://data.source.coop/ftw/harmonized-field-data/fi/year=2025/fi-2025.pmtiles) | [fi-2025.json](https://data.source.coop/ftw/harmonized-field-data/fi/year=2025/fi-2025.json) |

The latest edition is also available at a stable path: [fi/latest/fi.parquet](https://data.source.coop/ftw/harmonized-field-data/fi/latest/fi.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/fi/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/fi/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `block_id` | string | Official Identifier (source column `PERUSLOHKOTUNNUS`, per the fiboa data survey) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2025-01-01T00:00:00Z`
- `admin:country_code`: `FI`
- `crop:code_list`: `https://fiboa.org/code/fi/fi_2023.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/fi/latest/fi.parquet');
-- fields | hectares
-- 985486 | 2292382.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Finnish Food Authority](https://www.ruokavirasto.fi/en/about-us/open-information/spatial-data-sets/) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.16:

- 2020: converted 2026-09-10 from <https://download.inspire.ruokavirasto-awsa.com/data/2020/LandUse.ExistingLandUse.GSAAAgriculturalParcel.gpkg>
- 2021: converted 2026-09-10 from <https://download.inspire.ruokavirasto-awsa.com/data/2021/LandUse.ExistingLandUse.GSAAAgriculturalParcel.gpkg>
- 2022: converted 2026-09-10 from <https://download.inspire.ruokavirasto-awsa.com/data/2022/LandUse.ExistingLandUse.GSAAAgriculturalParcel.gpkg>
- 2023: converted 2026-09-10 from <https://download.inspire.ruokavirasto-awsa.com/data/2023/LandUse.ExistingLandUse.GSAAAgriculturalParcel.gpkg>
- 2024: converted 2026-09-10 from <https://download.inspire.ruokavirasto-awsa.com/data/2024/LandUse.ExistingLandUse.GSAAAgriculturalParcel.gpkg>
- 2025: converted 2026-09-10 from <https://download.inspire.ruokavirasto-awsa.com/data/2025/LandUse.ExistingLandUse.GSAAAgriculturalParcel.gpkg>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: Finnish Food Authority
