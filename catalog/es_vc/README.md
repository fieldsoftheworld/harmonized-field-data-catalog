# Spain Valencia Crop Fields

Graphic layer of the plots and enclosures with defined agricultural uses that accompany the information of the
Geographic Information System (SIGPAC) in the Valencian Community valid for the SIGPAC 2024 campaign
(data dated 15-01-2024).

- **Source data provider:** [Spanish Agricultural Guarantee Fund (FEGA) of the Ministry of Agriculture, Fisheries and Food](https://www.fega.gob.es/es/PwfGcp/es/el_fega/index.jsp)
- **License:** CC-BY-4.0
- **Editions:** 2024 (one GeoParquet per year)
- **Fields in the latest edition (2024):** 2,319,893
- **Coordinate reference system:** EPSG:25830 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/es_vc.py))
- **Data survey:** [ES-VC.md](https://github.com/fiboa/data-survey/blob/main/data/ES-VC.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/es_vc/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es_vc/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2024 | 2,319,893 | [969.3 MB](https://data.source.coop/ftw/harmonized-field-data/es_vc/year=2024/es_vc-2024.parquet) | [368.1 MB](https://data.source.coop/ftw/harmonized-field-data/es_vc/year=2024/es_vc-2024.pmtiles) | [es_vc-2024.json](https://data.source.coop/ftw/harmonized-field-data/es_vc/year=2024/es_vc-2024.json) |

The latest edition is also available at a stable path: [es_vc/latest/es_vc.parquet](https://data.source.coop/ftw/harmonized-field-data/es_vc/latest/es_vc.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/es_vc/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es_vc/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `admin_province_code` | string | Province ID (source column `PROVINCIA`, per the fiboa data survey) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name_en` | string | Crop name in English. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `admin_municipality_code` | string | Municipality ID (source column `MUNICIPIO`, per the fiboa data survey) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `ES`
- `crop:code_list`: `https://fiboa.org/code/es/sigpac/land_use.csv`
- `admin:subdivision_code`: `VC`
- `determination:datetime`: `2024-01-01T00:00:00Z`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/es_vc/latest/es_vc.parquet');
-- fields | hectares
-- 2319893 | 1407583.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Spanish Agricultural Guarantee Fund (FEGA) of the Ministry of Agriculture, Fisheries and Food](https://www.fega.gob.es/es/PwfGcp/es/el_fega/index.jsp) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2024: converted 2026-08-24 from <https://descargas.icv.gva.es/dcd/14_mediorural/03_pac/2024_SIGPAC_0050/1403_2024PALI_SIGPAC_RECINTOS_25830_SHP.7z>, <https://descargas.icv.gva.es/dcd/14_mediorural/03_pac/2024_SIGPAC_0050/1403_2024PCAS_SIGPAC_RECINTOS_25830_SHP.7z>, <https://descargas.icv.gva.es/dcd/14_mediorural/03_pac/2024_SIGPAC_0050/1403_2024PVAL_SIGPAC_RECINTOS_25830_SHP.7z>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: © Institut Cartogràfic Valencià, Generalitat
