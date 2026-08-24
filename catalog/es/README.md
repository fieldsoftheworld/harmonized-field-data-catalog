# Spain Declared Crops (Cultivos Declarados SIGPAC)

National declared-crop dataset (Cultivos Declarados SIGPAC) published by the Spanish Agricultural Guarantee Fund
(FEGA) via the unified SIGPAC Hub Cloud portal (sigpac-hubcloud.es). Each record is a declaration line within a
farmer's Single Application (Solicitud Única) for Common Agricultural Policy (CAP) direct payments, mapped onto
SIGPAC cadastral divisions. Data is distributed as one GeoPackage per Spanish province, harmonised across the
country since the 2025 campaign year.

This is a high-value dataset (HVD) under EU Implementing Regulation 2023/138.

- **Source data provider:** [Fondo Español de Garantía Agraria (FEGA)](https://www.fega.gob.es)
- **License:** CC-BY-4.0
- **Editions:** 2025 (one GeoParquet per year)
- **Fields in the latest edition (2025):** 17,857,146
- **Coordinate reference system:** EPSG:4258 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.15 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/es.py))
- **Data survey:** [ES.md](https://github.com/fiboa/data-survey/blob/main/data/ES.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/es/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2025 | 17,857,146 | [10.4 GB](https://data.source.coop/ftw/harmonized-field-data/es/year=2025/es-2025.parquet) | [3.7 GB](https://data.source.coop/ftw/harmonized-field-data/es/year=2025/es-2025.pmtiles) | [es-2025.json](https://data.source.coop/ftw/harmonized-field-data/es/year=2025/es-2025.json) |

The latest edition is also available at a stable path: [es/latest/es.parquet](https://data.source.coop/ftw/harmonized-field-data/es/latest/es.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/es/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/es/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `irrigation_system` | string | Carried over from the source column `parc_sistexp`; the publisher documents no meaning for it. |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:subdivision_code`: `01`
- `admin:country_code`: `ES`
- `determination:datetime`: `2025-01-01T00:00:00Z`
- `crop:code_list`: `https://fiboa.org/code/es/es.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/es/latest/es.parquet');
-- fields | hectares
-- 17857146 | 27689701.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Fondo Español de Garantía Agraria (FEGA)](https://www.fega.gob.es) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.15:

- 2025: converted 2026-08-24 from <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/01_ALAVA_cd_2025_20250105_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/02_ALBACETE_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/03_ALICANTE_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/04_ALMERIA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/05_AVILA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/06_BADAJOZ_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/07_ILLES%20BALEARS_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/08_BARCELONA_cd_2025_20241126_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/09_BURGOS_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/10_CACERES_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/11_CADIZ_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/12_CASTELLON_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/13_CIUDAD%20REAL_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/14_CORDOBA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/15_A%20CORU%C3%91A_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/16_CUENCA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/17_GIRONA_cd_2025_20241126_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/18_GRANADA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/19_GUADALAJARA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/20_GUIPUZCOA_cd_2025_20250105_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/21_HUELVA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/22_HUESCA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/23_JAEN_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/24_LEON_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/25_LLEIDA_cd_2025_20241126_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/26_LA%20RIOJA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/27_LUGO_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/28_MADRID_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/29_MALAGA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/30_MURCIA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/31_NAVARRA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/32_OURENSE_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/33_ASTURIAS_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/34_PALENCIA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/35_LAS%20PALMAS_cd_2025_20241026_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/36_PONTEVEDRA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/37_SALAMANCA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/38_SANTA%20CRUZ%20DE%20TENERIFE_cd_2025_20241026_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/39_CANTABRIA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/40_SEGOVIA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/41_SEVILLA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/42_SORIA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/43_TARRAGONA_cd_2025_20241126_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/44_TERUEL_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/45_TOLEDO_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/46_VALENCIA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/47_VALLADOLID_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/48_VIZCAYA_cd_2025_20250105_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/49_ZAMORA_cd_2025_20250110_gpkg.zip>, <https://sigpac-hubcloud.es/geopackages/2025/cultivo_declarado/50_ZARAGOZA_cd_2025_20250110_gpkg.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: ©FEGA / Ministerio de Agricultura, Pesca y Alimentación
