# harmonized-field-data-catalog

Git-backed [Portolan](https://www.portolan-sdi.org/) catalog of **harmonized field boundary data**: official, non-AI datasets — typically published by government bodies from their agricultural subsidy registers (IACS/LPIS), cadastres and statistics — converted to the [fiboa](https://fiboa.org/) schema with [fiboa-cli](https://github.com/fiboa/cli) and republished as cloud-native GeoParquet and PMTiles.

**This repository holds the catalog *metadata* and the publication tooling.** The data lives on Source Cooperative and is never committed here.

- Live catalog & data: <https://source.coop/ftw/harmonized-field-data> (bytes at `https://data.source.coop/ftw/harmonized-field-data/`)
- Browse: [Portolan data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/ftw/harmonized-field-data/catalog.json)
- For agents: [`AGENTS.md`](https://source.coop/ftw/harmonized-field-data/AGENTS.md) and [`llms.txt`](https://data.source.coop/ftw/harmonized-field-data/llms.txt) in the published catalog
- Predecessor: [source.coop/fiboa/data](https://source.coop/fiboa/data), which this catalog supersedes

## How the catalog is organised

One collection per source dataset (one fiboa-cli converter), partitioned by edition year in a hive layout so every edition can be queried at once, and with the newest edition at a stable path so all datasets can be queried at once:

```
catalog/
  catalog.json, README.md, AGENTS.md, llms.txt
  nl/
    collection.json, README.md, AGENTS.md, llms.txt, thumbnail.png
    styles/hcat-crops.json, field-size.json, outline.json
    year=2024/nl-2024.json  nl-2024.parquet  nl-2024.pmtiles      ← data only in the bucket
    year=2025/nl-2025.json  nl-2025.parquet  nl-2025.pmtiles
    latest/nl.parquet                                             ← copy of the newest edition
```

- all editions of one dataset: `https://data.source.coop/ftw/harmonized-field-data/nl/year=*/*.parquet` (`hive_partitioning = true` adds `year`)
- newest edition of every dataset: `https://data.source.coop/ftw/harmonized-field-data/*/latest/*.parquet` (`union_by_name = true`)

Each collection declares this with the STAC [partition extension](https://github.com/portolan-sdi/stac-partition-extension) (`partition:glob`).

## Where things live

| What | Where | Notes |
|---|---|---|
| How a dataset is converted | [fiboa-cli](https://github.com/fiboa/cli), `fiboa_cli/datasets/<id>.py` | **All conversion logic.** Fix column mappings, sources, licenses there; never here. |
| What is published | [`datasets.yaml`](datasets.yaml) | converter ids, the editions (years) to publish, keywords |
| The published catalog | [`catalog/`](catalog/) | synced 1:1 to the bucket; everything in it is public, nothing outside it is |
| Generators | [`tools/`](tools/) | `build.py` orchestrates; `catalogize.py` writes STAC + docs; `styles.py`, `thumbnail.py`; `upload_data.py` (data), `publish.py` (metadata) |
| Gates | [`tests/`](tests/) | links, publish contract, manifest ↔ catalog, stac-check, rashid (Portolan conformance); CI runs them on every push and PR |
| Accepted conformance deviations | [`docs/conformance.md`](docs/conformance.md) | empty, and meant to stay that way |

Edit the generator, not the generated output: `catalog/**/README.md`, `AGENTS.md`, `llms.txt`, `collection.json`, items and styles are all written by `tools/catalogize.py` from the converter's metadata, the [fiboa data survey](https://github.com/fiboa/data-survey), the specification texts in `tools/field_descriptions.yaml`, and measurements of the files. Every query printed in an `AGENTS.md` was executed while generating it; its output follows as comments.

## Adding or updating a dataset

Prerequisites: [pixi](https://pixi.sh), a fiboa-cli install (the `fiboa` command; set `FIBOA_CMD`/`FIBOA_PYTHON` to use a checkout), and for thumbnails a running [chiitiler](https://github.com/Kanahiro/chiitiler) (see `tools/thumbnail.py`).

```bash
pixi install
# 1. declare the dataset and its editions
$EDITOR datasets.yaml
# 2. convert → validate → PMTiles → STAC → styles → docs → thumbnail
pixi run python tools/build.py nl
# 3. run the gates, look at catalog/nl/ (and the thumbnail!), commit
pixi run python tests/run_all.py
git add catalog datasets.yaml && git commit -m "nl: add 2025 edition"
# 4. upload the data files, then the metadata (needs `source-coop login`, see below)
pixi run python tools/upload_data.py nl            # dry run
pixi run python tools/upload_data.py nl --confirm
pixi run python tools/publish.py                   # dry run
pixi run python tools/publish.py --confirm
```

`build.py` is idempotent: existing files in `staging/` are reused, delete them to reconvert. A new edition is a new `year=<Y>` partition; `latest/` follows automatically. Publishing never deletes objects in the bucket.

If a conversion is wrong, fix the converter in fiboa-cli, release it, bump the pin, and rebuild — the collection records the fiboa-cli version that produced it (`processing:software`).

## Uploading to Source Cooperative

Uploads go through the [Source Cooperative CLI](https://github.com/source-cooperative/source-coop-cli), which hands temporary credentials to the AWS SDK:

```bash
source-coop login          # opens the browser once; re-run when the session expires
```

with this profile in `~/.aws/config` (the scripts use it via `catalog.publish.yaml`):

```ini
[profile source-coop]
credential_process = source-coop creds
endpoint_url = https://data.source.coop
```

The bucket is addressed through the proxy as `s3://ftw/harmonized-field-data/`.

## Scope

In: field boundaries published by the responsible public body (or an official mirror such as INSPIRE/EuroCrops of such data). Out: AI-generated boundaries (see [Fields of the World](https://fieldsofthe.world)), commercial products, and research label sets — fiboa-cli has converters for those too, but they are not listed in `datasets.yaml`.

## License

The tooling and catalog metadata are Apache-2.0 ([LICENSE](LICENSE)). Each collection carries the license of its source data provider, stated in its `collection.json` and README.
