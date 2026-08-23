# Field boundaries for Mecklenburg-Western Pomerania, Germany

Field block register of the Ministry of Agriculture and Environment M-V

- **Source data provider:** [Ministerium für Landwirtschaft und Umwelt M-V](https://www.geodaten-mv.de/dienste/feldblock_atom?type=dataset&id=f18122c4-2585-4c22-9c48-9e960e8dhd34)
- **License:** other — [No restrictions apply](https://www.geodaten-mv.de/dienste/feldblock_atom?type=dataset&id=f18122c4-2585-4c22-9c48-9e960e8dhd34) (converter: `No restrictions apply <https://www.geodaten-mv.de/dienste/feldblock_atom?type=dataset&id=f18122c4-2585-4c22-9c48-9e960e8dhd34>`)
- **Editions:** 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 20,000
- **Coordinate reference system:** EPSG:25833 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/de_mv.py))
- **Data survey:** [DE-MV.md](https://github.com/fiboa/data-survey/blob/main/data/DE-MV.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/de_mv/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_mv/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2026 | 20,000 | [43.7 MB](https://data.source.coop/ftw/harmonized-field-data/de_mv/year=2026/de_mv.parquet) | [14.0 MB](https://data.source.coop/ftw/harmonized-field-data/de_mv/year=2026/de_mv.pmtiles) | [de_mv-2026.json](https://data.source.coop/ftw/harmonized-field-data/de_mv/year=2026/de_mv-2026.json) |

The latest edition is also available at a stable path: [de_mv/latest/de_mv.parquet](https://data.source.coop/ftw/harmonized-field-data/de_mv/latest/de_mv.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/de_mv/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/de_mv/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `bez_kreis` | string | District name (Kreisbezeichnung) (per the fiboa data survey) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `erwater` | string | Water-erosion class per Direktzahlungen-Verordnung (per the fiboa data survey) |
| `dgl_jahr` | int16 | Permanent-grassland year (DGL Jahr) (per the fiboa data survey) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `erwind` | string | Wind-erosion class per Direktzahlungen-Verordnung (per the fiboa data survey) |
| `erwater_l` | string | Water-erosion class per DIN 19708 (per the fiboa data survey) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `metrics:perimeter` | float | Perimeter of the field, in meters (m). Must be > 0 and <= 125,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `erwind_l` | string | Wind-erosion class per DIN 19708 (per the fiboa data survey) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `flik` | string | The area identifier (FLIK code) is a 16-character string. ([spec](https://github.com/fiboa/flik-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `crop:code_list`: `https://fiboa.org/code/de/de_mv.csv`
- `admin:country_code`: `DE`
- `admin:subdivision_code`: `MV`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/de_mv/latest/de_mv.parquet');
-- fields | hectares
-- 20000 | 546751.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Ministerium für Landwirtschaft und Umwelt M-V](https://www.geodaten-mv.de/dienste/feldblock_atom?type=dataset&id=f18122c4-2585-4c22-9c48-9e960e8dhd34) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2026: converted 2026-08-22 from <https://www.geodaten-mv.de/dienste/gdimv_feldblock_wfs?SERVICE=WFS&VERSION=1.1.0&REQUEST=GetFeature&TYPENAME=mv:feldbloecke&OUTPUTFORMAT=shape-zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

other — [No restrictions apply](https://www.geodaten-mv.de/dienste/feldblock_atom?type=dataset&id=f18122c4-2585-4c22-9c48-9e960e8dhd34) (converter: `No restrictions apply <https://www.geodaten-mv.de/dienste/feldblock_atom?type=dataset&id=f18122c4-2585-4c22-9c48-9e960e8dhd34>`). Attribute the data to Ministerium für Landwirtschaft und Umwelt M-V.
