# Mapping Africa: crop field boundary labels for Africa, 2017-2023

Crop field boundaries digitised by trained labellers over Planet NICFI monthly basemaps at
sites (0.005° cells, about 550 m) across 39 African countries, 2017-2023, from the
[Lacuna Fund](https://lacunafund.org/) project led by [Farmerline](https://farmerline.co/)
with [Spatial Collective](https://spatialcollective.com/) and the Agricultural Impacts
Research Group at Clark University ([lacunalabels](https://github.com/agroimpacts/lacunalabels)).

Only the assignments in the project's filtered label catalog are kept, which is one labelling
per site; sites labelled with no fields have no rows. Each field is dated by the month of the
basemap it was digitised on. `label_class` is the catalog's assignment class (1a, 1b, 1d:
expert-labelled quality-control sites; 2: one labeller; 4: one of three labellers), and
`qscore` / `rscore` are the labeller's quality scores against the expert labels: one value
per labeller, not per field.

The labels are not wall-to-wall: fields can be missing from a site, so unlabelled land is
unknown, not non-field.

Estes, L. D., Wussah, A., Asipunu, M., Gathigi, M., Kovačič, P., Muhando, J.,
Yeboah, B. V., Addai, F. K., Akakpo, E. S., Allotey, M. K., Amkoya, P., Amponsem, E.,
Donkoh, K. D., Ha, N., Heltzel, E., Juma, C., Mdawida, R., Miroyo, A., Mucha, J.,
Mugami, J., Mwawaza, F., Nyarko, D. A., Oduor, P., Ohemeng, K. N., Segbefia, S. I. D.,
Tumbula, T., Wambua, F., Xeflide, G. H., Ye, S., Yeboah, F.(2024). A region-wide,
multi-year set of crop field boundary labels for Africa. arXiv:2412.18483.

The labels are published at https://zenodo.org/records/11060871 and can be used in accordance
with [Planet's participant license agreement for the NICFI contract](https://go.planet.com/nicfi-pla-2024).

- **Source data provider:** [Agricultural Impacts Research Group, Clark University](https://github.com/agroimpacts/lacunalabels)
- **License:** other — [Planet NICFI participant license agreement](https://go.planet.com/nicfi-pla-2024) (converter: `Planet NICFI participant license agreement <https://go.planet.com/nicfi-pla-2024>`)
- **Editions:** 2024 (one GeoParquet per year)
- **Fields in the latest edition (2024):** 663,726
- **Coordinate reference system:** EPSG:4326 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.30.0, vecorel-cli 0.4.2 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/lacuna_labels.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/lacuna_labels/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/lacuna_labels/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2024 | 663,726 | [60.9 MB](https://data.source.coop/ftw/harmonized-field-data/lacuna_labels/year=2024/lacuna_labels-2024.parquet) | [88.8 MB](https://data.source.coop/ftw/harmonized-field-data/lacuna_labels/year=2024/lacuna_labels-2024.pmtiles) | [lacuna_labels-2024.json](https://data.source.coop/ftw/harmonized-field-data/lacuna_labels/year=2024/lacuna_labels-2024.json) |

The latest edition is also available at a stable path: [lacuna_labels/latest/lacuna_labels.parquet](https://data.source.coop/ftw/harmonized-field-data/lacuna_labels/latest/lacuna_labels.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/lacuna_labels/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/lacuna_labels/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

Presence-only: labellers did not always digitise every field in a site, so land outside the polygons is unknown, not non-field. One labelling per site, the one in the project's filtered label catalog; sites labelled with no fields are left out. `qscore` and `rscore` score the labeller against expert labels, not the individual field. The labels are licensed under Planet's NICFI participant license agreement, not an open license.

## Columns

| Column | Type | Description |
|---|---|---|
| `rscore` | float | Source-specific column; the publisher documents no meaning for it. |
| `admin:country_code` | string | ISO 3166-1 alpha-2 country code (aka admin0). Two-letter country code for the country that contains the field. ([spec](https://github.com/vecorel/administrative-division-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `label_category` | string | Carried over from the source column `category`; the publisher documents no meaning for it. |
| `assignment_id` | int64 | Source-specific column; the publisher documents no meaning for it. |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `site` | string | Carried over from the source column `name`; the publisher documents no meaning for it. |
| `label_class` | string | Source-specific column; the publisher documents no meaning for it. |
| `determination:datetime` | timestamp[ms, tz=UTC] | The last timestamp at which the field did exist and was observed. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `qscore` | float | Source-specific column; the publisher documents no meaning for it. |
| `labeller` | string | Source-specific column; the publisher documents no meaning for it. |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/lacuna_labels/latest/lacuna_labels.parquet');
-- fields | hectares
-- 663726 | 628850.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Agricultural Impacts Research Group, Clark University](https://github.com/agroimpacts/lacunalabels) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.30.0, vecorel-cli 0.4.2:

- 2024: converted 2026-11-06 from <https://africa-field-boundary-labels.s3.us-west-2.amazonaws.com/mapped_fields_final.parquet>, <https://africa-field-boundary-labels.s3.us-west-2.amazonaws.com/label-catalog-filtered.csv>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

other — [Planet NICFI participant license agreement](https://go.planet.com/nicfi-pla-2024) (converter: `Planet NICFI participant license agreement <https://go.planet.com/nicfi-pla-2024>`). Attribution: Estes et al. (2024), Lacuna Fund; labels digitised over Planet NICFI basemaps
