# BRP Crop Field Boundaries for The Netherlands (CAP-based)

BasisRegistratie Percelen (BRP) combines the location of
agricultural plots with the crop grown. The data set
is published by RVO (Netherlands Enterprise Agency). The boundaries of the agricultural plots
are based within the reference parcels (formerly known as AAN). A user an agricultural plot
annually has to register his crop fields with crops (for the Common Agricultural Policy scheme).
A dataset is generated for each year with reference date May 15.
A view service and a download service are available for the most recent BRP crop plots.

<https://service.pdok.nl/rvo/gewaspercelen/atom/index.xml>

Data is currently available for the years 2009 to 2025 (final) and 2026 (concept).
The editions 2005 to 2008 were published by RVO before and are no longer
downloadable; convert a copy with `--variant <year> -i "<zip>|<shapefile>"`.

- **Source data provider:** [RVO / PDOK](https://www.pdok.nl/introductie/-/article/basisregistratie-gewaspercelen-brp-)
- **License:** CC0-1.0
- **Editions:** 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 (one GeoParquet per year)
- **Fields in the latest edition (2026):** 1,266,361
- **Coordinate reference system:** EPSG:28992 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.30.0, vecorel-cli 0.4.4 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/nl.py))
- **Data survey:** [NL.md](https://github.com/fiboa/data-survey/blob/main/data/NL.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/nl/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/nl/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2005 | 731,927 | [129.4 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2005/nl-2005.parquet) | — | [nl-2005.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2005/nl-2005.json) |
| 2006 | 771,385 | [122.8 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2006/nl-2006.parquet) | — | [nl-2006.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2006/nl-2006.json) |
| 2007 | 759,230 | [119.6 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2007/nl-2007.parquet) | — | [nl-2007.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2007/nl-2007.json) |
| 2008 | 755,057 | [115.1 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2008/nl-2008.parquet) | — | [nl-2008.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2008/nl-2008.json) |
| 2009 | 809,814 | [170.9 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2009/nl-2009.parquet) | — | [nl-2009.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2009/nl-2009.json) |
| 2010 | 776,291 | [147.8 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2010/nl-2010.parquet) | — | [nl-2010.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2010/nl-2010.json) |
| 2011 | 773,361 | [151.7 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2011/nl-2011.parquet) | — | [nl-2011.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2011/nl-2011.json) |
| 2012 | 763,436 | [148.1 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2012/nl-2012.parquet) | — | [nl-2012.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2012/nl-2012.json) |
| 2013 | 754,002 | [147.7 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2013/nl-2013.parquet) | — | [nl-2013.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2013/nl-2013.json) |
| 2014 | 756,224 | [153.7 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2014/nl-2014.parquet) | — | [nl-2014.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2014/nl-2014.json) |
| 2015 | 782,549 | [178.9 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2015/nl-2015.parquet) | — | [nl-2015.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2015/nl-2015.json) |
| 2016 | 777,237 | [194.8 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2016/nl-2016.parquet) | — | [nl-2016.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2016/nl-2016.json) |
| 2017 | 774,043 | [206.0 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2017/nl-2017.parquet) | — | [nl-2017.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2017/nl-2017.json) |
| 2018 | 765,478 | [206.6 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2018/nl-2018.parquet) | — | [nl-2018.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2018/nl-2018.json) |
| 2019 | 758,306 | [205.9 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2019/nl-2019.parquet) | — | [nl-2019.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2019/nl-2019.json) |
| 2020 | 760,693 | [245.2 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2020/nl-2020.parquet) | — | [nl-2020.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2020/nl-2020.json) |
| 2021 | 760,000 | [266.9 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2021/nl-2021.parquet) | — | [nl-2021.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2021/nl-2021.json) |
| 2022 | 746,083 | [430.1 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2022/nl-2022.parquet) | — | [nl-2022.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2022/nl-2022.json) |
| 2023 | 1,371,363 | [914.1 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2023/nl-2023.parquet) | — | [nl-2023.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2023/nl-2023.json) |
| 2024 | 1,356,754 | [892.8 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2024/nl-2024.parquet) | — | [nl-2024.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2024/nl-2024.json) |
| 2025 | 1,295,261 | [721.3 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2025/nl-2025.parquet) | — | [nl-2025.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2025/nl-2025.json) |
| 2026 | 1,266,361 | [707.0 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2026/nl-2026.parquet) | [495.1 MB](https://data.source.coop/ftw/harmonized-field-data/nl/year=2026/nl-2026.pmtiles) | [nl-2026.json](https://data.source.coop/ftw/harmonized-field-data/nl/year=2026/nl-2026.json) |

The latest edition is also available at a stable path: [nl/latest/nl.parquet](https://data.source.coop/ftw/harmonized-field-data/nl/latest/nl.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/nl/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/nl/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

The editions 2005-2008 were published by RVO under the same license and are no longer downloadable from PDOK; they are converted from copies of the original shapefiles, which also keep fallow (`Braakland`) and crops without a category. RVO gave some crop codes a new crop over the years: an edition before the new meaning carries the code with an `o` suffix (`1934o`, starch potatoes, against `1934`, shallots, from 2019), which the code list maps to the old crop.

## Columns

| Column | Type | Description |
|---|---|---|
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `coverage` | string | Land-cover category (Grass land, Arable field, Ditch, Landscape element) (source column `category`, per the fiboa data survey) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `crop:name` | string | Crop name in the original language. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2026-05-15T00:00:00Z`
- `admin:country_code`: `NL`
- `crop:code_list`: `https://fiboa.org/code/nl/nl.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/nl/latest/nl.parquet');
-- fields | hectares
-- 1266361 | 1799320.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [RVO / PDOK](https://www.pdok.nl/introductie/-/article/basisregistratie-gewaspercelen-brp-) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.30.0, vecorel-cli 0.4.4:

- 2005: converted 2026-11-18 from a manually obtained file
- 2006: converted 2026-11-18 from a manually obtained file
- 2007: converted 2026-11-18 from a manually obtained file
- 2008: converted 2026-11-18 from a manually obtained file
- 2009: converted 2026-11-18 from <https://service.pdok.nl/rvo/gewaspercelen/atom/downloads/brpgewaspercelen_definitief_2009.zip>
- 2010: converted 2026-11-18 from <https://service.pdok.nl/rvo/gewaspercelen/atom/downloads/brpgewaspercelen_definitief_2010.zip>
- 2011: converted 2026-11-18 from <https://service.pdok.nl/rvo/gewaspercelen/atom/downloads/brpgewaspercelen_definitief_2011.zip>
- 2012: converted 2026-11-18 from <https://service.pdok.nl/rvo/gewaspercelen/atom/downloads/brpgewaspercelen_definitief_2012.zip>
- 2013: converted 2026-11-18 from <https://service.pdok.nl/rvo/gewaspercelen/atom/downloads/brpgewaspercelen_definitief_2013.zip>
- 2014: converted 2026-11-18 from <https://service.pdok.nl/rvo/gewaspercelen/atom/downloads/brpgewaspercelen_definitief_2014.zip>
- 2015: converted 2026-11-18 from <https://service.pdok.nl/rvo/gewaspercelen/atom/downloads/brpgewaspercelen_definitief_2015.zip>
- 2016: converted 2026-11-18 from <https://service.pdok.nl/rvo/gewaspercelen/atom/downloads/brpgewaspercelen_definitief_2016.zip>
- 2017: converted 2026-11-18 from <https://service.pdok.nl/rvo/gewaspercelen/atom/downloads/brpgewaspercelen_definitief_2017.zip>
- 2018: converted 2026-11-18 from <https://service.pdok.nl/rvo/gewaspercelen/atom/downloads/brpgewaspercelen_definitief_2018.zip>
- 2019: converted 2026-11-18 from <https://service.pdok.nl/rvo/gewaspercelen/atom/downloads/brpgewaspercelen_definitief_2019.zip>
- 2020: converted 2026-11-18 from <https://service.pdok.nl/rvo/gewaspercelen/atom/downloads/brpgewaspercelen_definitief_2020.gpkg>
- 2021: converted 2026-11-18 from <https://service.pdok.nl/rvo/gewaspercelen/atom/downloads/brpgewaspercelen_definitief_2021.gpkg>
- 2022: converted 2026-11-18 from <https://service.pdok.nl/rvo/gewaspercelen/atom/downloads/brpgewaspercelen_definitief_2022.gpkg>
- 2023: converted 2026-11-18 from <https://service.pdok.nl/rvo/gewaspercelen/atom/downloads/brpgewaspercelen_definitief_2023.gpkg>
- 2024: converted 2026-11-18 from <https://service.pdok.nl/rvo/gewaspercelen/atom/downloads/brpgewaspercelen_definitief_2024.gpkg>
- 2025: converted 2026-11-18 from <https://service.pdok.nl/rvo/gewaspercelen/atom/downloads/brpgewaspercelen_definitief_2025.gpkg>
- 2026: converted 2026-11-18 from <https://service.pdok.nl/rvo/gewaspercelen/atom/downloads/gewaspercelen_concept_2026.gpkg>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC0-1.0. Attribute the data to RVO / PDOK.
