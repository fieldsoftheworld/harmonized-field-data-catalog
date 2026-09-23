# Field boundaries for Portugal

Open field boundaries (identificação de parcelas) from Portugal

- **Source data provider:** [IPAP - Instituto de Financiamento da Agricultura e Pescas](https://www.ifap.pt/isip/ows/)
- **License:** other — [No conditions apply](https://inspire.ec.europa.eu/metadata-codelist/ConditionsApplyingToAccessAndUse/noConditionsApply) (converter: `No conditions apply <https://inspire.ec.europa.eu/metadata-codelist/ConditionsApplyingToAccessAndUse/noConditionsApply>`)
- **Editions:** 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2025 (one GeoParquet per year)
- **Fields in the latest edition (2025):** 3,571,255
- **Coordinate reference system:** EPSG:4326 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.16 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/pt.py))
- **Data survey:** [PT.md](https://github.com/fiboa/data-survey/blob/main/data/PT.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/pt/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/pt/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2017 | 3,732,091 | [1.2 GB](https://data.source.coop/ftw/harmonized-field-data/pt/year=2017/pt-2017.parquet) | — | [pt-2017.json](https://data.source.coop/ftw/harmonized-field-data/pt/year=2017/pt-2017.json) |
| 2018 | 3,798,241 | [1.3 GB](https://data.source.coop/ftw/harmonized-field-data/pt/year=2018/pt-2018.parquet) | — | [pt-2018.json](https://data.source.coop/ftw/harmonized-field-data/pt/year=2018/pt-2018.json) |
| 2019 | 4,038,298 | [1.3 GB](https://data.source.coop/ftw/harmonized-field-data/pt/year=2019/pt-2019.parquet) | — | [pt-2019.json](https://data.source.coop/ftw/harmonized-field-data/pt/year=2019/pt-2019.json) |
| 2020 | 4,766,789 | [1.6 GB](https://data.source.coop/ftw/harmonized-field-data/pt/year=2020/pt-2020.parquet) | — | [pt-2020.json](https://data.source.coop/ftw/harmonized-field-data/pt/year=2020/pt-2020.json) |
| 2021 | 4,882,314 | [1.6 GB](https://data.source.coop/ftw/harmonized-field-data/pt/year=2021/pt-2021.parquet) | — | [pt-2021.json](https://data.source.coop/ftw/harmonized-field-data/pt/year=2021/pt-2021.json) |
| 2022 | 4,953,834 | [1.6 GB](https://data.source.coop/ftw/harmonized-field-data/pt/year=2022/pt-2022.parquet) | — | [pt-2022.json](https://data.source.coop/ftw/harmonized-field-data/pt/year=2022/pt-2022.json) |
| 2023 | 4,805,442 | [1.2 GB](https://data.source.coop/ftw/harmonized-field-data/pt/year=2023/pt-2023.parquet) | — | [pt-2023.json](https://data.source.coop/ftw/harmonized-field-data/pt/year=2023/pt-2023.json) |
| 2025 | 3,571,255 | [1.3 GB](https://data.source.coop/ftw/harmonized-field-data/pt/year=2025/pt-2025.parquet) | [540.0 MB](https://data.source.coop/ftw/harmonized-field-data/pt/year=2025/pt-2025.pmtiles) | [pt-2025.json](https://data.source.coop/ftw/harmonized-field-data/pt/year=2025/pt-2025.json) |

The latest edition is also available at a stable path: [pt/latest/pt.parquet](https://data.source.coop/ftw/harmonized-field-data/pt/latest/pt.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/pt/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/pt/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

No crop code for a fifth to a third of the fields in every edition before 2025 (22.8% of 2017, 18.7% of 2018, 20.9% of 2019, 29.4-33.4% of 2020-2023): mostly IFAP recorded a land cover class and declared no crop. It is written as an empty string rather than null, because crop:code is required and the writer rejects nulls; in 2023 it is a single space, so test with strip(). 2020 is worse for the islands specifically (199,123 fields), its crop table covering the mainland only; 2021's does cover them and 2022 carries the code on the layer. 2017 publishes no identifier for Madeira or the Azores, so those 177,614 fields carry ids synthesised from 10^12 upward, a sort position rather than a provider key. 2018 ships the north twice; the 154,980 duplicated fields are dropped, leaving 3,798,241.

## Columns

| Column | Type | Description |
|---|---|---|
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `metrics:perimeter` | float | Perimeter of the field, in meters (m). Must be > 0 and <= 125,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `block_id` | int64 | Crop field identifier (source column `OSA_ID`, per the fiboa data survey) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) *(not a column in the 2025 edition)* |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `PT`
- `determination:datetime`: `2025-01-01T00:00:00Z`
- `crop:code_list`: `https://fiboa.org/code/pt/pt.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/pt/latest/pt.parquet');
-- fields | hectares
-- 3571255 | 3622080.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [IPAP - Instituto de Financiamento da Agricultura e Pescas](https://www.ifap.pt/isip/ows/) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.16:

- 2017: converted 2026-09-21 from <https://www.ifap.pt/isip/ows/resources/2017-2020/2017.zip>
- 2018: converted 2026-09-21 from <https://www.ifap.pt/isip/ows/resources/2017-2020/2018.zip>
- 2019: converted 2026-09-21 from <https://www.ifap.pt/isip/ows/resources/2017-2020/2019.zip>
- 2020: converted 2026-09-08 from <https://www.ifap.pt/isip/ows/resources/2017-2020/2020.zip>
- 2021: converted 2026-09-09 from <https://www.ifap.pt/isip/ows/resources/2021/2021.zip>
- 2022: converted 2026-09-08 from <https://www.ifap.pt/isip/ows/resources/2022/2022.zip>
- 2023: converted 2026-09-09 from <https://www.ifap.pt/isip/ows/resources/2023/Continente.gpkg>
- 2025: converted 2026-09-09 from <https://www.ifap.pt/isip/ows/resources/2025/culturas.gpkg>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

other — [No conditions apply](https://inspire.ec.europa.eu/metadata-codelist/ConditionsApplyingToAccessAndUse/noConditionsApply) (converter: `No conditions apply <https://inspire.ec.europa.eu/metadata-codelist/ConditionsApplyingToAccessAndUse/noConditionsApply>`). Attribute the data to IPAP - Instituto de Financiamento da Agricultura e Pescas.
