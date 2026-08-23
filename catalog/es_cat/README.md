# Catalonia Crop Fields (Mapa de cultius)

The Department of Agriculture, Livestock, Fisheries and Food makes available to the public the data from the crop map of Catalonia.
This map allows you to locate the crops declared in the Agrarian Declaration - DUN submitted to the DACC.

- **Source data provider:** [Catalonia Department of Agriculture, Livestock, Fisheries and Food](https://agricultura.gencat.cat/ca/ambits/desenvolupament-rural/sigpac/mapa-cultius/)
- **License:** other — [The Open Information Use License - Catalonia](https://administraciodigital.gencat.cat/ca/dades/dades-obertes/informacio-practica/llicencies/) (converter: `The Open Information Use License - Catalonia <https://administraciodigital.gencat.cat/ca/dades/dades-obertes/informacio-practica/llicencies/>`)
- **Editions:** 2024 (one GeoParquet per year)
- **Fields in the latest edition (2024):** 723,039
- **Coordinate reference system:** EPSG:25831 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/es_cat.py))
- **Data survey:** [ES-CAT.md](https://github.com/fiboa/data-survey/blob/main/data/ES-CAT.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/es_cat/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es_cat/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2024 | 723,039 | [282.4 MB](https://data.source.coop/ftw/harmonized-field-data/es_cat/year=2024/es_cat-2024.parquet) | [114.7 MB](https://data.source.coop/ftw/harmonized-field-data/es_cat/year=2024/es_cat-2024.pmtiles) | [es_cat-2024.json](https://data.source.coop/ftw/harmonized-field-data/es_cat/year=2024/es_cat-2024.json) |

The latest edition is also available at a stable path: [es_cat/latest/es_cat.parquet](https://data.source.coop/ftw/harmonized-field-data/es_cat/latest/es_cat.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/es_cat/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es_cat/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `crop:name_en` | string | Crop name in English. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2024-01-01T00:00:00Z`
- `crop:code_list`: `https://fiboa.org/code/es/cat/crop.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/es_cat/latest/es_cat.parquet');
-- fields | hectares
-- 723039 | 757593.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Catalonia Department of Agriculture, Livestock, Fisheries and Food](https://agricultura.gencat.cat/ca/ambits/desenvolupament-rural/sigpac/mapa-cultius/) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2024: converted 2026-08-22 from <https://analisi.transparenciacatalunya.cat/api/views/yh94-j2n9/files/d90f5fca-ddd8-405d-a0d5-90609985e98e?download=true&filename=Cultius_DUN2024_SHP.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

other — [The Open Information Use License - Catalonia](https://administraciodigital.gencat.cat/ca/dades/dades-obertes/informacio-practica/llicencies/) (converter: `The Open Information Use License - Catalonia <https://administraciodigital.gencat.cat/ca/dades/dades-obertes/informacio-practica/llicencies/>`). Attribution: Catalonia Department of Agriculture, Livestock, Fisheries and Food
