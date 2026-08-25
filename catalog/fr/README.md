# Registre Parcellaire Graphique; Crop Fields France

France has published Crop Field data for many years. Crop fields are declared by farmers within the Common Agricultural Policy (CAP) subsidy scheme.

The anonymized version is distributed as part of the public service for making reference data available contains graphic data for plots (basic land unit for farmers' declaration) with their main crop. This data has been produced by the Services and Payment Agency (ASP) since 2007.

- **Source data provider:** [Anstitut National de l'Information Géographique et Forestière](https://www.data.gouv.fr/en/datasets/registre-parcellaire-graphique-rpg-contours-des-parcelles-et-ilots-culturaux-et-leur-groupe-de-cultures-majoritaire/)
- **License:** other — [Licence Ouverte / Open Licence](https://etalab.gouv.fr/licence-ouverte-open-licence) (converter: `Licence Ouverte / Open Licence <https://etalab.gouv.fr/licence-ouverte-open-licence>`)
- **Editions:** 2017, 2019, 2020, 2021, 2022, 2023, 2024 (one GeoParquet per year)
- **Fields in the latest edition (2024):** 9,678,595
- **Coordinate reference system:** EPSG:2154 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/fr.py))
- **Data survey:** [FR.md](https://github.com/fiboa/data-survey/blob/main/data/FR.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/fr/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/fr/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2017 | 9,389,450 | [2.1 GB](https://data.source.coop/ftw/harmonized-field-data/fr/year=2017/fr-2017.parquet) | — | [fr-2017.json](https://data.source.coop/ftw/harmonized-field-data/fr/year=2017/fr-2017.json) |
| 2019 | 9,599,098 | [2.2 GB](https://data.source.coop/ftw/harmonized-field-data/fr/year=2019/fr-2019.parquet) | — | [fr-2019.json](https://data.source.coop/ftw/harmonized-field-data/fr/year=2019/fr-2019.json) |
| 2020 | 9,772,794 | [2.7 GB](https://data.source.coop/ftw/harmonized-field-data/fr/year=2020/fr-2020.parquet) | — | [fr-2020.json](https://data.source.coop/ftw/harmonized-field-data/fr/year=2020/fr-2020.json) |
| 2021 | 9,848,558 | [2.3 GB](https://data.source.coop/ftw/harmonized-field-data/fr/year=2021/fr-2021.parquet) | — | [fr-2021.json](https://data.source.coop/ftw/harmonized-field-data/fr/year=2021/fr-2021.json) |
| 2022 | 9,888,801 | [2.4 GB](https://data.source.coop/ftw/harmonized-field-data/fr/year=2022/fr-2022.parquet) | — | [fr-2022.json](https://data.source.coop/ftw/harmonized-field-data/fr/year=2022/fr-2022.json) |
| 2023 | 9,788,919 | [2.4 GB](https://data.source.coop/ftw/harmonized-field-data/fr/year=2023/fr-2023.parquet) | — | [fr-2023.json](https://data.source.coop/ftw/harmonized-field-data/fr/year=2023/fr-2023.json) |
| 2024 | 9,678,595 | [2.5 GB](https://data.source.coop/ftw/harmonized-field-data/fr/year=2024/fr-2024.parquet) | [1.1 GB](https://data.source.coop/ftw/harmonized-field-data/fr/year=2024/fr-2024.pmtiles) | [fr-2024.json](https://data.source.coop/ftw/harmonized-field-data/fr/year=2024/fr-2024.json) |

The latest edition is also available at a stable path: [fr/latest/fr.parquet](https://data.source.coop/ftw/harmonized-field-data/fr/latest/fr.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/fr/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/fr/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `group_code` | string | Carried over from the source column `code_group`; the publisher documents no meaning for it. |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `FR`
- `determination:datetime`: `2024-01-01T00:00:00Z`
- `crop:code_list`: `https://raw.githubusercontent.com/maja601/EuroCrops/refs/heads/main/csvs/country_mappings/fr_2018.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/fr/latest/fr.parquet');
-- fields | hectares
-- 9678595 | 27856342.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Anstitut National de l'Information Géographique et Forestière](https://www.data.gouv.fr/en/datasets/registre-parcellaire-graphique-rpg-contours-des-parcelles-et-ilots-culturaux-et-leur-groupe-de-cultures-majoritaire/) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2017: converted 2026-08-25 from <https://data.geopf.fr/telechargement/download/RPG/RPG_2-0__SHP_LAMB93_FR-2017_2017-01-01/RPG_2-0__SHP_LAMB93_FR-2017_2017-01-01.7z>
- 2019: converted 2026-08-25 from <https://data.geopf.fr/telechargement/download/RPG/RPG_2-0_GPKG_LAMB93_FR-2019/RPG_2-0_GPKG_LAMB93_FR-2019.7z>
- 2020: converted 2026-08-25 from <https://data.geopf.fr/telechargement/download/RPG/RPG_2-0__GPKG_LAMB93_FR_2020-01-01/RPG_2-0__GPKG_LAMB93_FR_2020-01-01.7z.001>, <https://data.geopf.fr/telechargement/download/RPG/RPG_2-0__GPKG_LAMB93_FR_2020-01-01/RPG_2-0__GPKG_LAMB93_FR_2020-01-01.7z.002>
- 2021: converted 2026-08-25 from <https://data.geopf.fr/telechargement/download/RPG/RPG_2-0__GPKG_LAMB93_FXX_2021-01-01/RPG_2-0__GPKG_LAMB93_FXX_2021-01-01.7z>
- 2022: converted 2026-08-25 from <https://data.geopf.fr/telechargement/download/RPG/RPG_2-0__GPKG_LAMB93_FXX_2022-01-01/RPG_2-0__GPKG_LAMB93_FXX_2022-01-01.7z.001>
- 2023: converted 2026-08-25 from <https://data.geopf.fr/telechargement/download/RPG/RPG_2-2__GPKG_LAMB93_FXX_2023-01-01/RPG_2-2__GPKG_LAMB93_FXX_2023-01-01.7z>
- 2024: converted 2026-08-25 from <https://data.geopf.fr/telechargement/download/RPG/RPG_3-0__GPKG_LAMB93_FXX_2024-01-01/RPG_3-0__GPKG_LAMB93_FXX_2024-01-01.7z.001>, <https://data.geopf.fr/telechargement/download/RPG/RPG_3-0__GPKG_LAMB93_FXX_2024-01-01/RPG_3-0__GPKG_LAMB93_FXX_2024-01-01.7z.002>, <https://data.geopf.fr/telechargement/download/RPG/RPG_3-0__GPKG_LAMB93_FXX_2024-01-01/RPG_3-0__GPKG_LAMB93_FXX_2024-01-01.7z.003>, <https://data.geopf.fr/telechargement/download/RPG/RPG_3-0__GPKG_LAMB93_FXX_2024-01-01/RPG_3-0__GPKG_LAMB93_FXX_2024-01-01.7z.004>, <https://data.geopf.fr/telechargement/download/RPG/RPG_3-0__GPKG_LAMB93_FXX_2024-01-01/RPG_3-0__GPKG_LAMB93_FXX_2024-01-01.7z.005>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

other — [Licence Ouverte / Open Licence](https://etalab.gouv.fr/licence-ouverte-open-licence) (converter: `Licence Ouverte / Open Licence <https://etalab.gouv.fr/licence-ouverte-open-licence>`). Attribution: IGN - Original data from https://geoservices.ign.fr/rpg
