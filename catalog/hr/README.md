# Croatian Field Boundaries

Field boundary data for Croatia, provided as part of national agricultural datasets.

This dataset contains spatial data related to agricultural land use in Croatia, including ARKOD parcel information,
environmentally sensitive areas, High Nature Value Grasslands, protective buffer strips around watercourses, and vineyard
classifications. The data is crucial for managing agricultural activities, ensuring compliance with environmental regulations,
and supporting sustainable land use practices.

- **Source data provider:** [Agencija za plaćanja u poljoprivredi, ribarstvu i ruralnom razvoju](https://www.apprrr.hr/prostorni-podaci-servisi/)
- **License:** other — [Prostorni podaci i servisi](https://www.apprrr.hr/prostorni-podaci-servisi/) (converter: `Prostorni podaci i servisi <https://www.apprrr.hr/prostorni-podaci-servisi/>`)
- **Editions:** 2024 (one GeoParquet per year)
- **Fields in the latest edition (2024):** 1,284,769
- **Coordinate reference system:** EPSG:3765 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/hr.py))
- **Data survey:** [HR.md](https://github.com/fiboa/data-survey/blob/main/data/HR.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/hr/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/hr/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2024 | 1,284,769 | [218.5 MB](https://data.source.coop/ftw/harmonized-field-data/hr/year=2024/hr-2024.parquet) | [164.9 MB](https://data.source.coop/ftw/harmonized-field-data/hr/year=2024/hr-2024.pmtiles) | [hr-2024.json](https://data.source.coop/ftw/harmonized-field-data/hr/year=2024/hr-2024.json) |

The latest edition is also available at a stable path: [hr/latest/hr.parquet](https://data.source.coop/ftw/harmonized-field-data/hr/latest/hr.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/hr/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/hr/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `rp` | int32 | RP flag (per the fiboa data survey) |
| `ot_nat` | int32 | Other nature flag (per the fiboa data survey) |
| `irrigation_source` | int32 | Irrigation source code (per the fiboa data survey) |
| `slope` | double | Average slope (per the fiboa data survey) |
| `natura2000_povs` | double | Natura 2000 POVS overlap (per the fiboa data survey) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `anc_area` | double | ANC area (per the fiboa data survey) |
| `irrigation_type` | int32 | Irrigation type code (per the fiboa data survey) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `mines_year_removed` | int32 | Year mines were removed (per the fiboa data survey) |
| `home_name` | string | Locality / home name (per the fiboa data survey) |
| `mines_status` | string | Mine contamination status (per the fiboa data survey) |
| `water_protect_zone` | string | Water protection zone code (per the fiboa data survey) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `anc` | int32 | Area with Natural Constraints flag (per the fiboa data survey) |
| `natura2000` | double | Natura 2000 overlap area (per the fiboa data survey) |
| `ot_nat_area` | double | Other nature area (per the fiboa data survey) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `natura2000_pop` | double | Natura 2000 POP overlap (per the fiboa data survey) |
| `height` | double | Average elevation (mapped to `height`) (source column `z_avg`, per the fiboa data survey) |
| `jpaid` | string | Unique single application identifier (per the fiboa data survey) |
| `metrics:perimeter` | float | Perimeter of the field, in meters (m). Must be > 0 and <= 125,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `irrigation` | int32 | Irrigation flag (per the fiboa data survey) |
| `tvpv` | int32 | TVPV flag (per the fiboa data survey) |
| `eligibility_coef` | double | Eligibility coefficient (per the fiboa data survey) |
| `natura2000_ok` | string | Natura 2000 status (per the fiboa data survey) |
| `sanitary_protection_zone` | string | Sanitary protection zone code (per the fiboa data survey) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `HR`
- `determination:datetime`: `2024-01-01T00:00:00Z`
- `crop:code_list`: `https://raw.githubusercontent.com/maja601/EuroCrops/refs/heads/main/csvs/country_mappings/hr_2020.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/hr/latest/hr.parquet');
-- fields | hectares
-- 1284769 | 1143805.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Agencija za plaćanja u poljoprivredi, ribarstvu i ruralnom razvoju](https://www.apprrr.hr/prostorni-podaci-servisi/) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2024: converted 2026-08-23 from <https://www.apprrr.hr/wp-content/uploads/nipp/land_parcels.gpkg>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

other — [Prostorni podaci i servisi](https://www.apprrr.hr/prostorni-podaci-servisi/) (converter: `Prostorni podaci i servisi <https://www.apprrr.hr/prostorni-podaci-servisi/>`). Attribution: copyright © 2024. Agencija za plaćanja u poljoprivredi, ribarstvu i ruralnom razvoju
