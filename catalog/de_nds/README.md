# Crop Fields for Lower Saxony / Bremen / Hamburg, Germany

A Crop Field (German: "Schlaege") is a contiguous agricultural area surrounded by permanent boundaries, which is cultivated with a single crop.

- **Source data provider:** [ML/SLA Niedersachsen](https://sla.niedersachsen.de/landentwicklung/LEA/)
- **License:** DL-DE-BY-2.0
- **Editions:** 2025 (one GeoParquet per year)
- **Fields in the latest edition (2025):** 881,956
- **Coordinate reference system:** EPSG:25832 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.16 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/de_nds.py))
- **Data survey:** [DE-NDS.md](https://github.com/fiboa/data-survey/blob/main/data/DE-NDS.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/de_nds/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_nds/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2025 | 881,956 | [208.2 MB](https://data.source.coop/ftw/harmonized-field-data/de_nds/year=2025/de_nds-2025.parquet) | [80.8 MB](https://data.source.coop/ftw/harmonized-field-data/de_nds/year=2025/de_nds-2025.pmtiles) | [de_nds-2025.json](https://data.source.coop/ftw/harmonized-field-data/de_nds/year=2025/de_nds-2025.json) |

The latest edition is also available at a stable path: [de_nds/latest/de_nds.parquet](https://data.source.coop/ftw/harmonized-field-data/de_nds/latest/de_nds.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/de_nds/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_nds/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `flik` | string | The area identifier (FLIK code) is a 16-character string. ([spec](https://github.com/fiboa/flik-extension/blob/main/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `subfield_id` | int64 | Numeric sub-field / parcel number within the application (source column `SCHLAGNR`, per the fiboa data survey) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2025-01-01T00:00:00Z`
- `admin:country_code`: `DE`
- `admin:subdivision_code`: `NI`
- `crop:code_list`: `https://raw.githubusercontent.com/maja601/EuroCrops/refs/heads/main/csvs/country_mappings/de.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/de_nds/latest/de_nds.parquet');
-- fields | hectares
-- 881956 | 2564322.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [ML/SLA Niedersachsen](https://sla.niedersachsen.de/landentwicklung/LEA/) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.16:

- 2025: converted 2026-09-04 from <https://sla.niedersachsen.de/mapbender_sla/download/schlaege_aktuell_2025.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

DL-DE-BY-2.0. Attribution: © ML/SLA Niedersachsen (2024), DL-DE-BY-2.0 (www.govdata.de/DL-DE-BY-2.0), Daten bearbeitet
