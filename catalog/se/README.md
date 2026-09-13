# Swedish Crop Fields (Jordbruksskiften)

A crop field (Jordbruksskift) is a contiguous area of land within a block where a farmer grows a crop or otherwise manages the land.
To receive compensation for agricultural support (EU support), farmers apply for support from the
Swedish Agency for Agriculture via a SAM application. The data set contains parcels where the area
applied for and the area decided on are the same. The data is published at the end of a year.

    Codes found at https://jordbruksverket.se/stod/jordbruk-tradgard-och-rennaring/sam-ansokan-och-allmant-om-jordbrukarstoden/grodkoder

- **Source data provider:** [Jordbruksverket (The Swedish Board of Agriculture)](https://jordbruksverket.se)
- **License:** CC0-1.0
- **Editions:** 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025 (one GeoParquet per year)
- **Fields in the latest edition (2025):** 1,207,889
- **Coordinate reference system:** EPSG:3006 (as published by the source; not reprojected)
- **Converted with:** fiboa-cli 0.21.0, vecorel-cli 0.2.16 ([converter](https://github.com/fiboa/cli/blob/main/fiboa_cli/datasets/se.py))
- **Data survey:** [SE.md](https://github.com/fiboa/data-survey/blob/main/data/SE.md)

Browse this collection in the [data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/se/collection.json), or start from the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/se/AGENTS.md) for tested queries.

## Files

| Year | Fields | GeoParquet | PMTiles | STAC item |
|---|---:|---|---|---|
| 2015 | 1,091,146 | [288.4 MB](https://data.source.coop/ftw/harmonized-field-data/se/year=2015/se-2015.parquet) | — | [se-2015.json](https://data.source.coop/ftw/harmonized-field-data/se/year=2015/se-2015.json) |
| 2016 | 1,127,793 | [265.7 MB](https://data.source.coop/ftw/harmonized-field-data/se/year=2016/se-2016.parquet) | — | [se-2016.json](https://data.source.coop/ftw/harmonized-field-data/se/year=2016/se-2016.json) |
| 2017 | 1,125,651 | [277.0 MB](https://data.source.coop/ftw/harmonized-field-data/se/year=2017/se-2017.parquet) | — | [se-2017.json](https://data.source.coop/ftw/harmonized-field-data/se/year=2017/se-2017.json) |
| 2018 | 1,119,587 | [290.4 MB](https://data.source.coop/ftw/harmonized-field-data/se/year=2018/se-2018.parquet) | — | [se-2018.json](https://data.source.coop/ftw/harmonized-field-data/se/year=2018/se-2018.json) |
| 2019 | 1,125,696 | [298.4 MB](https://data.source.coop/ftw/harmonized-field-data/se/year=2019/se-2019.parquet) | — | [se-2019.json](https://data.source.coop/ftw/harmonized-field-data/se/year=2019/se-2019.json) |
| 2020 | 1,142,901 | [305.7 MB](https://data.source.coop/ftw/harmonized-field-data/se/year=2020/se-2020.parquet) | — | [se-2020.json](https://data.source.coop/ftw/harmonized-field-data/se/year=2020/se-2020.json) |
| 2021 | 1,147,391 | [351.7 MB](https://data.source.coop/ftw/harmonized-field-data/se/year=2021/se-2021.parquet) | — | [se-2021.json](https://data.source.coop/ftw/harmonized-field-data/se/year=2021/se-2021.json) |
| 2022 | 1,141,367 | [346.3 MB](https://data.source.coop/ftw/harmonized-field-data/se/year=2022/se-2022.parquet) | — | [se-2022.json](https://data.source.coop/ftw/harmonized-field-data/se/year=2022/se-2022.json) |
| 2023 | 1,142,785 | [345.0 MB](https://data.source.coop/ftw/harmonized-field-data/se/year=2023/se-2023.parquet) | — | [se-2023.json](https://data.source.coop/ftw/harmonized-field-data/se/year=2023/se-2023.json) |
| 2024 | 1,146,499 | [278.8 MB](https://data.source.coop/ftw/harmonized-field-data/se/year=2024/se-2024.parquet) | — | [se-2024.json](https://data.source.coop/ftw/harmonized-field-data/se/year=2024/se-2024.json) |
| 2025 | 1,207,889 | [305.3 MB](https://data.source.coop/ftw/harmonized-field-data/se/year=2025/se-2025.parquet) | [189.6 MB](https://data.source.coop/ftw/harmonized-field-data/se/year=2025/se-2025.pmtiles) | [se-2025.json](https://data.source.coop/ftw/harmonized-field-data/se/year=2025/se-2025.json) |

The latest edition is also available at a stable path: [se/latest/se.parquet](https://data.source.coop/ftw/harmonized-field-data/se/latest/se.parquet). All editions together through the S3 glob `s3://ftw/harmonized-field-data/se/year=*/*.parquet` (see the [AGENTS.md](https://source.coop/ftw/harmonized-field-data/se/AGENTS.md) for the DuckDB setup; plain https cannot expand `*`).

## Columns

| Column | Type | Description |
|---|---|---|
| `metrics:area` | float | Area of the field, in square meters (m²). Must be > 0 and <= 1,000,000,000. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name` | string | The machine-readable HCAT name of the crop (Hierarchical Crop and Agriculture Taxonomy, EuroCrops). ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `crop:code` | string | The crop code, from the code list of the source. ([spec](https://github.com/fiboa/crop-extension/blob/main/README.md)) |
| `geometry` | binary | A geometry that reflects the footprint of the field, usually a Polygon. Stored in the source CRS (see `proj:code`), not reprojected. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `collection` | string | The identifier of the collection. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:name_en` | string | The original crop name translated into English. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `id` | string | An identifier for the field. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |
| `hcat:code` | uint32 | The 10-digit HCAT code indicating the hierarchy of the crop. The first 4, 6, 8 digits select increasingly specific crop groups. ([spec](https://github.com/fiboa/hcat-extension/blob/main/README.md)) |
| `bbox` | struct<xmin: double, ymin: double, xmax: double, ymax: double> | The bounding box of the field. Per-feature covering column (GeoParquet 1.1), in the source CRS. ([spec](https://github.com/fiboa/specification/blob/main/core/README.md)) |

Properties that are the same for every field are stored once, in the GeoParquet file's `collection` metadata rather than as columns (latest edition shown; a client reading only the table will not see them):

- `determination:datetime`: `2025-01-01T00:00:00Z`
- `admin:country_code`: `SE`
- `crop:code_list`: `https://fiboa.org/code/se/se.csv`

## Access

Query the published files in place with DuckDB; nothing needs downloading first.

```sql
INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;
SELECT count(*) AS fields, round(sum("metrics:area") / 1e4) AS hectares
FROM read_parquet('https://data.source.coop/ftw/harmonized-field-data/se/latest/se.parquet');
-- fields | hectares
-- 1207889 | 2886988.0
```

## Provenance

This catalog is a mirror: the data is produced and licensed by [Jordbruksverket (The Swedish Board of Agriculture)](https://jordbruksverket.se) and republished here as cloud-native GeoParquet and PMTiles by Fields of the World. Each edition was downloaded from the source and converted with fiboa-cli 0.21.0, vecorel-cli 0.2.16:

- 2015: converted 2026-09-13 from <https://epub.sjv.se/inspire/inspire/wfs?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=inspire:arslager_skifte&outputFormat=shape-zip&CQL_FILTER=arslager=%272015%27%20and%20geom%20is%20not%20null&format_options=CHARSET:UTF-8>
- 2016: converted 2026-09-13 from <https://epub.sjv.se/inspire/inspire/wfs?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=inspire:arslager_skifte&outputFormat=shape-zip&CQL_FILTER=arslager=%272016%27%20and%20geom%20is%20not%20null&format_options=CHARSET:UTF-8>
- 2017: converted 2026-09-13 from <https://epub.sjv.se/inspire/inspire/wfs?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=inspire:arslager_skifte&outputFormat=shape-zip&CQL_FILTER=arslager=%272017%27%20and%20geom%20is%20not%20null&format_options=CHARSET:UTF-8>
- 2018: converted 2026-09-13 from <https://epub.sjv.se/inspire/inspire/wfs?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=inspire:arslager_skifte&outputFormat=shape-zip&CQL_FILTER=arslager=%272018%27%20and%20geom%20is%20not%20null&format_options=CHARSET:UTF-8>
- 2019: converted 2026-09-13 from <https://epub.sjv.se/inspire/inspire/wfs?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=inspire:arslager_skifte&outputFormat=shape-zip&CQL_FILTER=arslager=%272019%27%20and%20geom%20is%20not%20null&format_options=CHARSET:UTF-8>
- 2020: converted 2026-09-13 from <https://epub.sjv.se/inspire/inspire/wfs?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=inspire:arslager_skifte&outputFormat=shape-zip&CQL_FILTER=arslager=%272020%27%20and%20geom%20is%20not%20null&format_options=CHARSET:UTF-8>
- 2021: converted 2026-09-13 from <https://epub.sjv.se/inspire/inspire/wfs?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=inspire:arslager_skifte&outputFormat=shape-zip&CQL_FILTER=arslager=%272021%27%20and%20geom%20is%20not%20null&format_options=CHARSET:UTF-8>
- 2022: converted 2026-09-13 from <https://epub.sjv.se/inspire/inspire/wfs?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=inspire:arslager_skifte&outputFormat=shape-zip&CQL_FILTER=arslager=%272022%27%20and%20geom%20is%20not%20null&format_options=CHARSET:UTF-8>
- 2023: converted 2026-09-13 from <https://epub.sjv.se/inspire/inspire/wfs?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=inspire:arslager_skifte&outputFormat=shape-zip&CQL_FILTER=arslager=%272023%27%20and%20geom%20is%20not%20null&format_options=CHARSET:UTF-8>
- 2024: converted 2026-09-13 from <https://epub.sjv.se/inspire/inspire/wfs?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=inspire:arslager_skifte&outputFormat=shape-zip&CQL_FILTER=arslager=%272024%27%20and%20geom%20is%20not%20null&format_options=CHARSET:UTF-8>
- 2025: converted 2026-09-13 from <https://epub.sjv.se/inspire/inspire/wfs?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=inspire:arslager_skifte&outputFormat=shape-zip&CQL_FILTER=arslager=%272025%27%20and%20geom%20is%20not%20null&format_options=CHARSET:UTF-8>

The conversion is deterministic and lives in [fiboa-cli](https://github.com/fiboa/cli); changes to how a column is mapped are made there, not in this catalog.

## License

CC0-1.0. Attribution: Jordbruksverket
