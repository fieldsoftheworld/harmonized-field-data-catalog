# Field boundaries for Austria

**Crop Field boundaries for Austria - INVEKOS Schläge Österreich 2025.**

This layer includes all field uses recorded by the applicants, which serve as the basis for the funding process. A field
is a contiguous area of a piece of land that is cultivated for a growing season with only one crop (field use type) and
uniform management requirements or as a landscape element type in accordance with Annex 1 of the regulation of the responsible
Federal Ministry with horizontal rules for the area of the Common Agricultural Policy (Horizontal CAP Regulation)
StF: BGBl. II No. 100/2015 or is simply maintained in good agricultural and ecological condition in accordance with
Art. 94 of Regulation (EU) No. 1306/2013 and is digitized in the GIS as a polygon or as a point.

- **Source data provider:** [Agrarmarkt Austria](https://geometadatensuche.inspire.gv.at/metadatensuche/inspire/api/records/9db8a0c3-e92a-4df4-9d55-8210e326a7ed)
- **License:** CC-BY-4.0
- **Editions:** 2025 (one GeoParquet per year)
- **Fields in the latest edition (2025):** 2,944,405
- **Coordinate reference system:** EPSG:31287 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/at.py))
- **Data survey:** [AT.md](https://github.com/fiboa/data-survey/blob/main/data/AT.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/at/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/at/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2025 | 2,944,405 | [812.1 MB](https://data.source.coop/ftw/harmonized-field-data/at/year=2025/at-2025.parquet) | [604.1 MB](https://data.source.coop/ftw/harmonized-field-data/at/year=2025/at-2025.pmtiles) | [at-2025.json](https://data.source.coop/ftw/harmonized-field-data/at/year=2025/at-2025.json) |

The latest edition is also available at a stable path: [at/latest/at.parquet](https://data.source.coop/ftw/harmonized-field-data/at/latest/at.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/at/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/at/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `determination:datetime` | timestamp[ms, tz=UTC] | The last timestamp at which the field did exist and was observed. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `AT`
- `crop:code_list`: `https://fiboa.org/code/at/at.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/at/latest/at.parquet');
-- fields | hectares
-- 2944405 | 3150555.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Agrarmarkt Austria](https://geometadatensuche.inspire.gv.at/metadatensuche/inspire/api/records/9db8a0c3-e92a-4df4-9d55-8210e326a7ed) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2025: converted 2026-08-23 from <https://inspire.lfrz.gv.at/009501/ds/inspire_schlaege_2025-1_polygon.gpkg.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribute the data to Agrarmarkt Austria.
