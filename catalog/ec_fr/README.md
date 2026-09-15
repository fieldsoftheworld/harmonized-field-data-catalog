# Field boundaries for France - Eurocrops 2018

The 2018 campaign of the Registre Parcellaire Graphique, which IGN never released as an
archive of its own: the RPG downloads run 2017 and 2019 onwards. EuroCrops publishes it
with its HCAT columns already resolved.

- **Source data provider:** [Institut National de l'Information Géographique et Forestière <https://geoservices.ign.fr/rpg>, EuroCrops](https://github.com/maja601/EuroCrops)
- **License:** CC-BY-SA-4.0
- **Editions:** 2018 (one GeoParquet per year)
- **Fields in the latest edition (2018):** 9,517,891
- **Coordinate reference system:** EPSG:2154 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.16 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ec_fr.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/ec_fr/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ec_fr/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2018 | 9,517,891 | [2.2 GB](https://data.source.coop/ftw/harmonized-field-data/ec_fr/year=2018/ec_fr.parquet) | [1.0 GB](https://data.source.coop/ftw/harmonized-field-data/ec_fr/year=2018/ec_fr.pmtiles) | [ec_fr-2018.json](https://data.source.coop/ftw/harmonized-field-data/ec_fr/year=2018/ec_fr-2018.json) |

The latest edition is also available at a stable path: [ec_fr/latest/ec_fr.parquet](https://data.source.coop/ftw/harmonized-field-data/ec_fr/latest/ec_fr.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/ec_fr/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ec_fr/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

The 2018 campaign of the Registre Parcellaire Graphique, which IGN publishes no archive for: its downloads run 2017 and 2019 onwards. SURF_PARC is rounded to 0.01 ha, so 4,913 parcels under 50 m2 take their area from the geometry.

## Columns

| Column | Type | Description |
|---|---|---|
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `group_code` | string | Carried over from the source column `CODE_GROUP`; the publisher documents no meaning for it. |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `crop:code_list`: `https://raw.githubusercontent.com/maja601/EuroCrops/refs/heads/main/csvs/country_mappings/fr_2018.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/ec_fr/latest/ec_fr.parquet');
-- fields | hectares
-- 9517891 | 27917501.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Institut National de l'Information Géographique et Forestière <https://geoservices.ign.fr/rpg>, EuroCrops](https://github.com/maja601/EuroCrops) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.16:

- 2018: converted 2026-09-15 from <https://zenodo.org/records/14094196/files/FR_2018.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-SA-4.0. Attribution: IGN - Original data from https://geoservices.ign.fr/rpg
