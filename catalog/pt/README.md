# Field boundaries for Portugal

Open field boundaries (identificação de parcelas) from Portugal

- **Source data provider:** [IPAP - Instituto de Financiamento da Agricultura e Pescas](https://www.ifap.pt/isip/ows/)
- **License:** other — [No conditions apply](https://inspire.ec.europa.eu/metadata-codelist/ConditionsApplyingToAccessAndUse/noConditionsApply) (converter: `No conditions apply <https://inspire.ec.europa.eu/metadata-codelist/ConditionsApplyingToAccessAndUse/noConditionsApply>`)
- **Editions:** 2023 (one GeoParquet per year)
- **Fields in the latest edition (2023):** 4,805,469
- **Coordinate reference system:** EPSG:3763 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/pt.py))
- **Data survey:** [PT.md](https://github.com/fiboa/data-survey/blob/main/data/PT.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/pt/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/pt/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2023 | 4,805,469 | [1.2 GB](https://data.source.coop/ftw/harmonized-field-data/pt/year=2023/pt-2023.parquet) | [652.7 MB](https://data.source.coop/ftw/harmonized-field-data/pt/year=2023/pt-2023.pmtiles) | [pt-2023.json](https://data.source.coop/ftw/harmonized-field-data/pt/year=2023/pt-2023.json) |

The latest edition is also available at a stable path: [pt/latest/pt.parquet](https://data.source.coop/ftw/harmonized-field-data/pt/latest/pt.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/pt/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/pt/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `metrics:perimeter` | float | Perimeter of the field, in meters (m). Must be > 0 and <= 125,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `block_id` | int64 | Field block identifier (source column `CUL_ID`, per the fiboa data survey) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2023-01-01T00:00:00Z`
- `admin:country_code`: `PT`
- `crop:code_list`: `https://fiboa.org/code/pt/pt.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/pt/latest/pt.parquet');
-- fields | hectares
-- 4805469 | 4090352.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [IPAP - Instituto de Financiamento da Agricultura e Pescas](https://www.ifap.pt/isip/ows/) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2023: converted 2026-08-24 from <https://www.ifap.pt/isip/ows/resources/2023/Continente.gpkg>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

other — [No conditions apply](https://inspire.ec.europa.eu/metadata-codelist/ConditionsApplyingToAccessAndUse/noConditionsApply) (converter: `No conditions apply <https://inspire.ec.europa.eu/metadata-codelist/ConditionsApplyingToAccessAndUse/noConditionsApply>`). Attribute the data to IPAP - Instituto de Financiamento da Agricultura e Pescas.
