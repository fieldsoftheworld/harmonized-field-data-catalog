# Field blocks for Poland

The maximum eligible area (MKO JPO, "maksymalny kwalifikowalny obszar") of Poland's Land Parcel
Identification System, published by the paying agency ARiMR. Poland's reference parcel is the
cadastral parcel; each polygon is the part of one parcel that is eligible for the single area
payment. The layer carries no crop or land-cover class. ARiMR publishes only the current state.

- **Source data provider:** [Agencja Restrukturyzacji i Modernizacji Rolnictwa](https://geoportal.arimr.gov.pl/mapy/apps/sites/#/portal)
- **License:** other — [Publiczne dane ARiMR, no licence stated](https://geoportal.arimr.gov.pl/mapy/apps/sites/#/portal) (converter: `Publiczne dane ARiMR, no licence stated <https://geoportal.arimr.gov.pl/mapy/apps/sites/#/portal>`)
- **Editions:** 2025 (one GeoParquet per year)
- **Fields in the latest edition (2025):** 12,955,563
- **Coordinate reference system:** EPSG:2180 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.3.1 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/pl_block.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/pl_block/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/pl_block/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2025 | 12,955,563 | [1.5 GB](https://data.source.coop/ftw/harmonized-field-data/pl_block/year=2025/pl_block.parquet) | [940.8 MB](https://data.source.coop/ftw/harmonized-field-data/pl_block/year=2025/pl_block.pmtiles) | [pl_block-2025.json](https://data.source.coop/ftw/harmonized-field-data/pl_block/year=2025/pl_block-2025.json) |

The latest edition is also available at a stable path: [pl_block/latest/pl_block.parquet](https://data.source.coop/ftw/harmonized-field-data/pl_block/latest/pl_block.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/pl_block/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/pl_block/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `admin:subdivision_code` | string | ISO 3166-2 code for the principal subdivision (e.g., province or state, aka admin1) of a country that contains the field. Only the second part of the ISO 3166-2 code is stored. ([spec](https://github.com/vecorel/administrative-division-extension/blob/main/README.md)) |
| `parcel_id` | string | Carried over from the source column `id_ewidenc`; the publisher documents no meaning for it. |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2025-11-25T00:00:00Z`
- `admin:country_code`: `PL`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/pl_block/latest/pl_block.parquet');
-- fields | hectares
-- 12955563 | 14319566.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Agencja Restrukturyzacji i Modernizacji Rolnictwa](https://geoportal.arimr.gov.pl/mapy/apps/sites/#/portal) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.3.1:

- 2025: converted 2026-09-27 from <https://geoportal.arimr.gov.pl/mapy/sharing/rest/content/items/dacf163ee97149cc8e5da0f0c4435b41/data>, <https://geoportal.arimr.gov.pl/mapy/sharing/rest/content/items/3cfcdbb6660245019059ab144e1cd3ac/data>, <https://geoportal.arimr.gov.pl/mapy/sharing/rest/content/items/f5ec9c02e0494fba9e35dbbc0b861fa6/data>, <https://geoportal.arimr.gov.pl/mapy/sharing/rest/content/items/a3b8ff265dff475e9050b5ff44164c8e/data>, <https://geoportal.arimr.gov.pl/mapy/sharing/rest/content/items/f83dfac145b043268c950b7c93af0cc6/data>, <https://geoportal.arimr.gov.pl/mapy/sharing/rest/content/items/3e8c2d1dff494e28b009494286cf4418/data>, <https://geoportal.arimr.gov.pl/mapy/sharing/rest/content/items/659540c4407e493f82e834566beb4d1d/data>, <https://geoportal.arimr.gov.pl/mapy/sharing/rest/content/items/f97243dcfe6b4b1ab15e7791205e2168/data>, <https://geoportal.arimr.gov.pl/mapy/sharing/rest/content/items/caa2a7cd257f413b8897fb2b135a9cda/data>, <https://geoportal.arimr.gov.pl/mapy/sharing/rest/content/items/4d8e2c9ba02c449f878b2df838f857ad/data>, <https://geoportal.arimr.gov.pl/mapy/sharing/rest/content/items/b4d1334a6b2e497a921a8045ad31b070/data>, <https://geoportal.arimr.gov.pl/mapy/sharing/rest/content/items/1f0761da4f7b4f30b472933219cf9292/data>, <https://geoportal.arimr.gov.pl/mapy/sharing/rest/content/items/92fc87fcb4e14145a7e13f6a1717cd12/data>, <https://geoportal.arimr.gov.pl/mapy/sharing/rest/content/items/25dce1d8be1347058b2ec19c73067c2f/data>, <https://geoportal.arimr.gov.pl/mapy/sharing/rest/content/items/56cc149b96714fcd8bf56905e6e7d1f2/data>, <https://geoportal.arimr.gov.pl/mapy/sharing/rest/content/items/25bb8cc0d91a40a980179dbaa2366f83/data>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

other — [Publiczne dane ARiMR, no licence stated](https://geoportal.arimr.gov.pl/mapy/apps/sites/#/portal) (converter: `Publiczne dane ARiMR, no licence stated <https://geoportal.arimr.gov.pl/mapy/apps/sites/#/portal>`). Attribution: © ARiMR
