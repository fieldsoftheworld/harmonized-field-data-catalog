# GloCAB cropland field boundaries (Brazil, Canada, Russia, Ukraine, USA)

190,832 cropland field boundaries in 22 regions of Brazil, Canada, Russia, Ukraine and the United
States, digitised by hand over 20 m Sentinel-2 imagery by geospatial analysts at the University of
Maryland and quality-checked by a senior team member, as a by-product of the Global Cropland Area
Burned (GloCAB) product. The readme gives each region a mapping date (a month, Table A), which is
each field's determination date here (2016 to 2020, by region).
Where fields were too small to identify, the analyst digitised a larger boundary around several
fields and set the `no_area` flag: those polygons are not true field boundaries.
`predominant_crop` is the predominant crop type of the region, not of the field.

- **Source data provider:** [University of Maryland](https://doi.org/10.5281/zenodo.10479122)
- **License:** CC-BY-4.0
- **Editions:** 2016, 2017, 2018, 2019, 2020 (one GeoParquet per year)
- **Fields in the latest edition (2020):** 124,417
- **Coordinate reference system:** EPSG:4326 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.30.0, vecorel-cli 0.4.2 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/glocab.py))

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/glocab/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/glocab/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2016 | 5,212 | [765.1 KB](https://data.source.coop/ftw/harmonized-field-data/glocab/year=2016/glocab-2016.parquet) | — | [glocab-2016.json](https://data.source.coop/ftw/harmonized-field-data/glocab/year=2016/glocab-2016.json) |
| 2017 | 40,948 | [5.4 MB](https://data.source.coop/ftw/harmonized-field-data/glocab/year=2017/glocab-2017.parquet) | — | [glocab-2017.json](https://data.source.coop/ftw/harmonized-field-data/glocab/year=2017/glocab-2017.json) |
| 2018 | 5,615 | [626.9 KB](https://data.source.coop/ftw/harmonized-field-data/glocab/year=2018/glocab-2018.parquet) | — | [glocab-2018.json](https://data.source.coop/ftw/harmonized-field-data/glocab/year=2018/glocab-2018.json) |
| 2019 | 14,640 | [2.0 MB](https://data.source.coop/ftw/harmonized-field-data/glocab/year=2019/glocab-2019.parquet) | — | [glocab-2019.json](https://data.source.coop/ftw/harmonized-field-data/glocab/year=2019/glocab-2019.json) |
| 2020 | 124,417 | [13.8 MB](https://data.source.coop/ftw/harmonized-field-data/glocab/year=2020/glocab-2020.parquet) | [7.7 MB](https://data.source.coop/ftw/harmonized-field-data/glocab/year=2020/glocab-2020.pmtiles) | [glocab-2020.json](https://data.source.coop/ftw/harmonized-field-data/glocab/year=2020/glocab-2020.json) |

The latest edition is also available at a stable path: [glocab/latest/glocab.parquet](https://data.source.coop/ftw/harmonized-field-data/glocab/latest/glocab.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/glocab/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/glocab/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

Each region was digitised over Sentinel-2 imagery of one month (Table A of the readme), recorded as the determination:datetime of its fields; an edition holds the regions digitised in its year. `predominant_crop` is the region's predominant crop, the same for every field of a region. Polygons with `no_area` enclose several fields too small to identify and are not true field boundaries.

## Columns

| Column | Type | Description |
|---|---|---|
| `region` | string | Carried over from the source column `Ctry_Reg`; the publisher documents no meaning for it. |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `predominant_crop` | string | Carried over from the source column `CropType`; the publisher documents no meaning for it. |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `admin:country_code` | string | ISO 3166-1 alpha-2 country code (aka admin0). Two-letter country code for the country that contains the field. ([spec](https://github.com/vecorel/administrative-division-extension/blob/main/README.md)) |
| `determination:datetime` | timestamp[ms, tz=UTC] | The last timestamp at which the field did exist and was observed. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `no_area` | bool | Carried over from the source column `No_Area`; the publisher documents no meaning for it. |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/glocab/latest/glocab.parquet');
-- fields | hectares
-- 124417 | 3866093.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [University of Maryland](https://doi.org/10.5281/zenodo.10479122) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.30.0, vecorel-cli 0.4.2:

- 2016: converted 2026-11-06 from <https://zenodo.org/api/records/10479122/files/GloCAB_Field_Boundaries.zip/content>
- 2017: converted 2026-11-06 from <https://zenodo.org/api/records/10479122/files/GloCAB_Field_Boundaries.zip/content>
- 2018: converted 2026-11-06 from <https://zenodo.org/api/records/10479122/files/GloCAB_Field_Boundaries.zip/content>
- 2019: converted 2026-11-06 from <https://zenodo.org/api/records/10479122/files/GloCAB_Field_Boundaries.zip/content>
- 2020: converted 2026-11-06 from <https://zenodo.org/api/records/10479122/files/GloCAB_Field_Boundaries.zip/content>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC-BY-4.0. Attribution: Hall, J. V., Argueta, F., Giglio, L.: GloCAB Cropland Field Boundary Dataset, Zenodo, doi:10.5281/zenodo.10479122
