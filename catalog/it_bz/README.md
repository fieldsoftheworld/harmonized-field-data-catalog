# Field boundaries for South Tyrol, Italy

The utilised agricultural area of South Tyrol, the autonomous Italian province of Bolzano, held in
the province's LAFIS system. The polygons are digitised manually from orthophotos or GPS survey and
aggregated by crop type, crop protection and crop-type detail, so a feature is an area of one crop
type rather than one farmer's application parcel. The source carries no farm or parcel identifier.

- **Source data provider:** [Autonome Provinz Bozen - Südtirol](https://agricoltura.provincia.bz.it/it/home)
- **License:** CC0-1.0
- **Editions:** 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 152,990
- **Coordinate reference system:** EPSG:25832 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.3.1 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/it_bz.py))
- **Data survey:** [IT-BZ.md](https://github.com/fiboa/data-survey/blob/main/data/IT-BZ.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/it_bz/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/it_bz/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2026 | 152,990 | [64.2 MB](https://data.source.coop/ftw/harmonized-field-data/it_bz/year=2026/it_bz.parquet) | [35.0 MB](https://data.source.coop/ftw/harmonized-field-data/it_bz/year=2026/it_bz.pmtiles) | [it_bz-2026.json](https://data.source.coop/ftw/harmonized-field-data/it_bz/year=2026/it_bz-2026.json) |

The latest edition is also available at a stable path: [it_bz/latest/it_bz.parquet](https://data.source.coop/ftw/harmonized-field-data/it_bz/latest/it_bz.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/it_bz/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/it_bz/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2026-09-24T00:00:00Z`
- `crop:code_list`: `https://fiboa.org/code/it/bz/crop.csv`
- `admin:country_code`: `IT`
- `admin:subdivision_code`: `BZ`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/it_bz/latest/it_bz.parquet');
-- fields | hectares
-- 152990 | 205656.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Autonome Provinz Bozen - Südtirol](https://agricoltura.provincia.bz.it/it/home) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.3.1:

- 2026: converted 2026-09-27 from <https://geoservices6.civis.bz.it/geoserver/p_bz-Agriculture/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=p_bz-Agriculture%3AFields-Used&outputFormat=application%2Fjson&count=50000&startIndex=0>, <https://geoservices6.civis.bz.it/geoserver/p_bz-Agriculture/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=p_bz-Agriculture%3AFields-Used&outputFormat=application%2Fjson&count=50000&startIndex=50000>, <https://geoservices6.civis.bz.it/geoserver/p_bz-Agriculture/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=p_bz-Agriculture%3AFields-Used&outputFormat=application%2Fjson&count=50000&startIndex=100000>, <https://geoservices6.civis.bz.it/geoserver/p_bz-Agriculture/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=p_bz-Agriculture%3AFields-Used&outputFormat=application%2Fjson&count=50000&startIndex=150000>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC0-1.0. Attribution: © Autonome Provinz Bozen - Südtirol
