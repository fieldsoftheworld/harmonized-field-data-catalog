# Brazil Crop Fields (CONAB)

CONAB, Brazil's National Supply Company, is the government agency responsible for providing information on the country's agricultural harvest.

These 29 mappings, after inspecting all boundaries in the CONAB public database, appear to be hand-drawn field boundaries.

The content of the Mappings comes from Conab, total or partial reproduction without profit motives is authorized,
as long as the source is cited and the integrity of the information is maintained.

Further information or suggestions can be sent to the email address conab.geote@conab.gov.br

- **Source data provider:** [Conab](https://portaldeinformacoes.conab.gov.br/mapeamentos-agricolas-downloads.html)
- **License:** CC-BY-NC-4.0
- **Editions:** 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 390,805
- **Coordinate reference system:** EPSG:4674 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.4.0 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/br_conab.py))
- **Data survey:** [BR-CONAB.md](https://github.com/fiboa/data-survey/blob/main/data/BR-CONAB.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/br_conab/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/br_conab/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2026 | 390,805 | [202.5 MB](https://data.source.coop/ftw/harmonized-field-data/br_conab/year=2026/br_conab.parquet) | [106.8 MB](https://data.source.coop/ftw/harmonized-field-data/br_conab/year=2026/br_conab.pmtiles) | [br_conab-2026.json](https://data.source.coop/ftw/harmonized-field-data/br_conab/year=2026/br_conab-2026.json) |

The latest edition is also available at a stable path: [br_conab/latest/br_conab.parquet](https://data.source.coop/ftw/harmonized-field-data/br_conab/latest/br_conab.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/br_conab/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/br_conab/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

Licensed CC-BY-NC-4.0: Conab authorises reproduction without profit motive, citing the source. The 29 files are the mappings that, on inspection, hold hand-drawn field boundaries; Conab publishes more (259 downloads in 2026). Minas Gerais coffee (2017) holds most of the fields. Polygons under 100 m² are left out as digitising slivers: some 74,800, nearly all in Minas Gerais, where they are a fifth of the polygons. There is no crop column: the crop is the mapping's subject, named in `id`.

## Columns

| Column | Type | Description |
|---|---|---|
| `admin_municipality_code` | string | Municipality code (source column `cd_mun`, per the fiboa data survey) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `admin_municipality_name` | string | Municipality name (source column `nm_mun`, per the fiboa data survey) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `admin:country_code`: `BR`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/br_conab/latest/br_conab.parquet');
-- fields | hectares
-- 390805 | 5040599.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Conab](https://portaldeinformacoes.conab.gov.br/mapeamentos-agricolas-downloads.html) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.4.0:

- 2026: converted 2026-10-08 from <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1784839922_algodao-go-safra-2019-2020.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1784839955_algodao-go-safra-2018-2019.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1784839890_go-algodao-2021.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1784558283_go-algodao-2223.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1784840252_ms-algodao-2021.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1784840209_ms-algodao-2122.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1784840479_go-arroz-irrig-2122.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1784840507_go-arroz-irrig-inund-23241.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1784840800_arroz-go-safra-2018-2019.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1784840902_arroz-ms-safra-2018-2019.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1784841005_arroz-pr-safra-2017-2018.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1784841189_arroz-rs-safra-2019-2020.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1784841407_arroz-sc-safra-2018-2019.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1784841526_arroz-to-safra-2017-2018.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1784841496_to-arroz-irrig-2324.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1785258893_cana-go-11-12.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1789672175_cafe-ba-19.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1785251263_cafe-df-18.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1785251314_cafe-go-18.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1785251334_cafe-go-19.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1785251366_cafe-pr-17.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1787760927_cafe-mg-safra-2017.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1785251294_cafe-df-24.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1785251350_cafe-go-21.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1785251708_cafe-rj-21.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1785335351_cv-df-safra-2013-2014.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1785335351_cv-df-safra-2014-2015.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1785335352_cv-df-safra-2017-2018.zip>, <https://portaldeinformacoes.conab.gov.br/downloads/mapas/1785335410_cv-to-safra-2019-2020.zip>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-NC-4.0. Attribution: CONAB - conab.gov.br
