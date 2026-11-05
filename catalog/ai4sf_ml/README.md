# Field boundaries for Cambodia and Vietnam (AI4SmallFarms) with splits

Agricultural field polygons within smallholder farming systems are essential to facilitate the collection of geo-spatial data useful for farmers, managers, and policymakers.
However, the limited availability of training labels poses a challenge in developing supervised methods to accurately delineate field boundaries using Earth Observation (EO) data.
This data set allows researchers to test and benchmark machine learning methods to delineate agricultural field boundaries in polygon format.
The large-scale data set consists of 439,001 field polygons divided into 62 tiles of approximately 5×5 km distributed across Vietnam and Cambodia, covering a range of fields and diverse landscape types.
The field polygons have been meticulously digitized from satellite images, following a rigorous multi-step quality control process and topological consistency checks.
Multi-temporal composites of Sentinel-2 (S2) images are provided to ensure cloud-free data.

- **Source data provider:** [DATA Archiving and Networked Services (DANS)](https://research.tudelft.nl/en/publications/ai4smallfarms-a-dataset-for-crop-field-delineation-in-southeast-a)
- **License:** CC-BY-4.0
- **Editions:** 2021 (one GeoParquet per year)
- **Fields in the latest edition (2021):** 439,001
- **Coordinate reference system:** EPSG:32648 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.30.0, vecorel-cli 0.4.2 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/ai4sf_ml.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/ai4sf_ml/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ai4sf_ml/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2021 | 439,001 | [36.5 MB](https://data.source.coop/ftw/harmonized-field-data/ai4sf_ml/year=2021/ai4sf_ml-2021.parquet) | [33.4 MB](https://data.source.coop/ftw/harmonized-field-data/ai4sf_ml/year=2021/ai4sf_ml-2021.pmtiles) | [ai4sf_ml-2021.json](https://data.source.coop/ftw/harmonized-field-data/ai4sf_ml/year=2021/ai4sf_ml-2021.json) |

The latest edition is also available at a stable path: [ai4sf_ml/latest/ai4sf_ml.parquet](https://data.source.coop/ftw/harmonized-field-data/ai4sf_ml/latest/ai4sf_ml.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/ai4sf_ml/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/ai4sf_ml/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `group` | uint8 | Carried over from the source column `id`; the publisher documents no meaning for it. |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `admin:country_code` | string | ISO 3166-1 alpha-2 country code (aka admin0). Two-letter country code for the country that contains the field. ([spec](https://github.com/vecorel/administrative-division-extension/blob/main/README.md)) |
| `split` | string | Source-specific column; the publisher documents no meaning for it. |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `_predicate`: `INTERSECTS`
- `determination:datetime`: `2021-08-01T00:00:00Z`
- `determination:method`: `manual`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/ai4sf_ml/latest/ai4sf_ml.parquet');
-- fields | hectares
-- 439001 | 129490.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [DATA Archiving and Networked Services (DANS)](https://research.tudelft.nl/en/publications/ai4smallfarms-a-dataset-for-crop-field-delineation-in-southeast-a) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.30.0, vecorel-cli 0.4.2:

- 2021: converted 2026-11-05 from <https://phys-techsciences.datastations.nl/api/access/datafile/100634?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100282?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100392?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100252?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100072?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100169?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100348?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100487?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100084?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100155?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100475?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100372?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100196?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100006?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100248?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100397?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100217?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100652?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100326?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100625?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100413?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100593?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100057?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100536?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100343?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100711?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100313?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100679?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100191?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100023?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100025?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100543?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100297?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100636?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100574?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100095?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100398?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100187?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100065?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100425?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100589?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100021?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100043?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100562?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100437?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100549?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100039?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100427?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100466?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100014?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100464?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100416?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100115?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100510?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100459?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100340?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100119?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100086?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100467?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100176?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100145?gbrecs=true>, <https://phys-techsciences.datastations.nl/api/access/datafile/100492?gbrecs=true>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: Persello, C., Grift, J., Fan, X., Paris, C., Hansch, R., Koeva, M., & Nelson, A. (2023). AI4SmallFarms: A Dataset for Crop Field Delineation in Southeast Asian Smallholder Farms. IEEE Geoscience and Remote Sensing Letters, 20, 1-5. Article 2505705. https://doi.org/10.1109/LGRS.2023.3323095
