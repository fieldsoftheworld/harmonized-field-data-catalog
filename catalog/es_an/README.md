# Spain Andalusia Crop fields

SIGPAC is the Geographic Information System for the Identification of Agricultural Plots ,
created through collaboration between the Spanish Agricultural Guarantee Fund (FEGA) and
the different Autonomous Communities, within the scope of their territories, as an element
of the Integrated Management and Control System of the direct aid regimes. It has the character
of a public register of administrative profile, and contains updated information on the
plots that may benefit from community aid related to the surface area, providing graphic
support for these and their subdivisions (ENCLOSURES) with defined agricultural uses or
developments.

- **Source data provider:** [Junta de Andalucía](https://www.juntadeandalucia.es)
- **License:** other — [Pursuant to Law 37/2007 of 16 November on the reuse of public sector information and Law 3/2013 of 24 July approving the Statistical and Cartographic Plan of Andalusia 2013-2017, the geographic information of SIGPAC is made available to the public.](https://www.juntadeandalucia.es/organismos/agriculturapescaaguaydesarrollorural/servicios/sigpac/visor/paginas/sigpac-descarga-informacion-geografica-shapes-provincias.html#toc-condiciones-de-uso-para-la-licencia-de-uso-comercial) (converter: `Pursuant to Law 37/2007 of 16 November on the reuse of public sector information and Law 3/2013 of 24 July approving the Statistical and Cartographic Plan of Andalusia 2013-2017, the geographic information of SIGPAC is made available to the public. <https://www.juntadeandalucia.es/organismos/agriculturapescaaguaydesarrollorural/servicios/sigpac/visor/paginas/sigpac-descarga-informacion-geografica-shapes-provincias.html#toc-condiciones-de-uso-para-la-licencia-de-uso-comercial>`)
- **Editions:** 2025 (one GeoParquet per year)
- **Fields in the latest edition (2025):** 4,415,113
- **Coordinate reference system:** EPSG:25830 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/es_an.py))
- **Data survey:** [ES-AN.md](https://github.com/fiboa/data-survey/blob/main/data/ES-AN.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/es_an/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es_an/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2025 | 4,415,113 | [1.6 GB](https://data.source.coop/ftw/harmonized-field-data/es_an/year=2025/es_an-2025.parquet) | [515.8 MB](https://data.source.coop/ftw/harmonized-field-data/es_an/year=2025/es_an-2025.pmtiles) | [es_an-2025.json](https://data.source.coop/ftw/harmonized-field-data/es_an/year=2025/es_an-2025.json) |

The latest edition is also available at a stable path: [es_an/latest/es_an.parquet](https://data.source.coop/ftw/harmonized-field-data/es_an/latest/es_an.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/es_an/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es_an/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `admin_province_code` | string | Province code (source column `CD_PROV`, per the fiboa data survey) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `admin_municipality_code` | string | Municipality code (source column `CD_MUN`, per the fiboa data survey) |
| `crop:name_en` | string | Crop name in English. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `ES`
- `crop:code_list`: `https://fiboa.org/code/es/sigpac/land_use.csv`
- `admin:subdivision_code`: `AN`
- `determination:datetime`: `2025-01-01T00:00:00Z`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/es_an/latest/es_an.parquet');
-- fields | hectares
-- 4415113 | 6773412.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Junta de Andalucía](https://www.juntadeandalucia.es) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2025: converted 2026-08-23 from <https://www.juntadeandalucia.es/ssdigitales/festa/agriculturapescaaguaydesarrollorural/2025/SP25_REC_PROV_04.zip>, <https://www.juntadeandalucia.es/ssdigitales/festa/agriculturapescaaguaydesarrollorural/2025/SP25_REC_PROV_11.zip>, <https://www.juntadeandalucia.es/ssdigitales/festa/agriculturapescaaguaydesarrollorural/2025/SP25_REC_PROV_14.zip>, <https://www.juntadeandalucia.es/ssdigitales/festa/agriculturapescaaguaydesarrollorural/2025/SP25_REC_PROV_18.zip>, <https://www.juntadeandalucia.es/ssdigitales/festa/agriculturapescaaguaydesarrollorural/2025/SP25_REC_PROV_21.zip>, <https://www.juntadeandalucia.es/ssdigitales/festa/agriculturapescaaguaydesarrollorural/2025/SP25_REC_PROV_23.zip>, <https://www.juntadeandalucia.es/ssdigitales/festa/agriculturapescaaguaydesarrollorural/2025/SP25_REC_PROV_29.zip>, <https://www.juntadeandalucia.es/ssdigitales/festa/agriculturapescaaguaydesarrollorural/2025/SP25_REC_PROV_41.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

other — [Pursuant to Law 37/2007 of 16 November on the reuse of public sector information and Law 3/2013 of 24 July approving the Statistical and Cartographic Plan of Andalusia 2013-2017, the geographic information of SIGPAC is made available to the public.](https://www.juntadeandalucia.es/organismos/agriculturapescaaguaydesarrollorural/servicios/sigpac/visor/paginas/sigpac-descarga-informacion-geografica-shapes-provincias.html#toc-condiciones-de-uso-para-la-licencia-de-uso-comercial) (converter: `Pursuant to Law 37/2007 of 16 November on the reuse of public sector information and Law 3/2013 of 24 July approving the Statistical and Cartographic Plan of Andalusia 2013-2017, the geographic information of SIGPAC is made available to the public. <https://www.juntadeandalucia.es/organismos/agriculturapescaaguaydesarrollorural/servicios/sigpac/visor/paginas/sigpac-descarga-informacion-geografica-shapes-provincias.html#toc-condiciones-de-uso-para-la-licencia-de-uso-comercial>`). Attribution: ©Junta de Andalucía
