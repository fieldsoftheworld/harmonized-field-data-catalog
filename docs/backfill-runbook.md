# Multi-year backfill — team runbook

The catalog publishes every available edition of every dataset. The table at the
bottom lists what still needs converting (~140 dataset-years as of 2026-08-25).
This document is written to be handed to Claude Code: copy the prompt below into
your own Claude session, fill in the dataset, and it has everything it needs.

## Prerequisites (once)

- A machine with ≥32 GB RAM and ≥100 GB free disk for the small/medium datasets;
  the heavy ones (es_ga, nl early years, dk early years) want ≥64 GB RAM.
- [Pixi](https://pixi.sh). GDAL with Parquet support and tippecanoe come from the
  pixi environments — never use a system ogr2ogr without checking it has Parquet.
- Clones of both repos:
  - `github.com/fiboa/cli`, branch **`publish-portolan`** (the publication branch;
    conversion fixes are PRed against it) — `pixi install -e dev`
  - `github.com/fieldsoftheworld/harmonized-field-data-catalog`, branch `main`
    — `pixi install`
- A [Source Cooperative](https://source.coop) account with **write access to
  `ftw/harmonized-field-data`** (ask Ivor), and the `source-coop` CLI for
  `source-coop login` (temporary AWS credentials, valid ~1 hour — re-login per
  upload batch).
- Claim your dataset first: open an issue titled `backfill: <dataset>` in the
  catalog repo so two people never convert the same years.

## The prompt

Copy everything between the lines into Claude Code, started in the catalog
repo clone, and replace `<DATASET>`:

---

I'm backfilling historical editions of the `<DATASET>` dataset for the
harmonized field-boundary data catalog (this repo). Read
`docs/backfill-runbook.md` fully first — it defines the workflow, the
policies, and the known traps. My fiboa-cli clone (branch `publish-portolan`)
is at `../cli` (adjust if elsewhere).

Work through the missing years for `<DATASET>` listed in the runbook table,
newest first:

1. In fiboa-cli, verify each year's `variants` entry actually works: URLs
   respond, the archive contains what the target glob expects (old editions
   rename files and change schemas — check before burning a long conversion),
   and the converter sets per-edition determination dates
   (`use_variant_as_determination = True` when the source has no per-feature
   date). Fix what's broken, run `pixi run -e dev pytest tests/test_convert.py
   -k <DATASET>`, and commit on a branch off `publish-portolan`; open a PR and
   flag it to Ivor.
2. Extend the `years:` list for `<DATASET>` in `datasets.yaml` (newest last).
3. Pre-download any source larger than ~2 GB into `cache/` with
   `tools/prefetch.sh` (vecorel-cli's own downloader gives up after 300 s and
   keeps the truncated file). Write the prefetch list BEFORE starting, and
   check the `.out` log for FAILED lines.
4. Build with `python tools/build.py <DATASET>` (use the pixi env's python;
   note `fi` is a pixi-shell reserved word — call the env python directly).
   Already-built years are skipped; only the newest edition gets PMTiles
   (build.py passes --no-pmtiles for the rest automatically). Export
   TMPDIR to a partition with >50 GB free — tippecanoe fills /tmp otherwise.
   Long conversions belong in `screen`/`tmux` with output to a log file.
5. Sanity-check every new parquet: row count is plausible against the latest
   edition, `determination:datetime` reflects the edition year (constant
   values live in the parquet's collection-level KV metadata, not as a
   column — that is by design), and `fiboa validate` passes (build.py runs it).
6. Upload only the data files with `python tools/upload_data.py <DATASET>`
   (dry run first, then `--confirm` after `source-coop login`). Uploads never
   delete; re-uploading unchanged files is skipped by checksum.
7. Regenerate the catalog root with `python tools/catalogize.py --root
   --remote` (measures the published bucket — run it only after the upload).
8. Commit `catalog/<DATASET>/` + the root files + `datasets.yaml` on a branch
   and open a PR against this repo (CI validates the metadata). Do NOT run
   `tools/publish.py` — publishing the metadata happens when the PR merges.

Ask me before anything destructive, before any upload, and whenever a year's
source turns out to differ structurally from what the converter expects.

---

## Policies

- **PMTiles latest-only**: older editions ship as parquet only. The browser
  renders just the newest edition; tiles for old years double storage unseen.
- **Newest first**: backfill the most recent missing year first; `latest/`
  must always be the newest edition (build.py handles the copy).
- **Truth over labels**: if an upstream archive's real vintage differs from its
  name (fr's "2018" archive contains 2017 data), name the variant after the
  data. Note it in the converter.
- **Never delete from the bucket**; uploads are add/replace only.
- **Thumbnails**: existing collections keep their thumbnail; nothing to do
  during a backfill. New collections need one (see `tools/thumbnail.py`).

## Known traps (all hit in production)

| Trap | Symptom | Fix |
|---|---|---|
| vecorel 300 s download cap | conversion fails ~300 s in, empty error; truncated file stays in cache | prefetch with `tools/prefetch.sh`, delete the truncated file first |
| tippecanoe fills /tmp | "Write to temporary file failed: No space left on device" after the full feature read | `export TMPDIR=<big disk>`; publish passes it via `-t` |
| Old editions change layout | "Can not match ... to a single file", missing columns, uppercase columns | inspect the archive before converting; fix the variant target/migrate |
| First variant = publish default | publishing without `--variant` silently builds the first dict entry | keep the newest year first in `variants`; never put test fixtures first |
| Constant columns "disappear" | `determination:datetime` etc. not a parquet column | they collapse into collection-level KV metadata — by design, not a bug |
| REST/WFS sources | only the current state is served | no backfill possible; the year is captured going forward |
| `pixi run ... fi ...` | "Unsupported reserved word" | call `.pixi/envs/default/bin/python` directly |
| Partial extraction after a killed run | reader errors (e.g. "fread failed on DBF") with a complete archive | delete the `extracted.*` dir and re-extract |

## Backlog (as of 2026-08-25)

Availability = years the fiboa-cli converter declares; each year still needs
its URL/schema verified before conversion. Ordered by size of the gap.

| dataset | published | missing years | notes |
|---|---|---|---|
| dk | 2026 | 2008–2025 (18) | large; verify early-year URLs |
| nl | 2025 | 2010–2024, 2026 (16) | 2026 is an UPDATE, do it first |
| ee | 2024 | 2010–2023 (14) | |
| es_cb | 2024 | 2010–2023 (14) | |
| es_ga | 2024 | 2010–2023 (14) | 13M+ features/yr — needs a big machine |
| hr | 2024 | 2011–2023 (13) | |
| es_pv | 2025 | 2016–2024 (9) | |
| es_an | 2025 | 2017–2024 (8) | |
| es_vc | 2024 | 2016–2023 (8) | |
| pt | 2023 | 2015–2022 (8) | 9 GB gpkg per year — prefetch |
| at | 2025 | 2018–2024 (7) | |
| cz | 2026 | 2019–2025 (7) | |
| it_1 | 2023 | 2016–2022 (7) | |
| be_vlg | 2023–2025 | 2018–2022, 2026 (6) | 2026 is an UPDATE |
| es_cm | 2024 | 2018–2023 (6) | |
| es_cat | 2024 | 2019–2023 (5) | |
| de_sh | 2026 | 2023–2025 (3) | |
| si | 2024 | 2021–2023 (3) | |
| ie | 2024 | 2022–2023 (2) | |

Done (all available editions published): fr, jp, nz, us_usda_cropland, es.
No backfill possible (single-edition or current-state sources): everything
listed with "(no variants)" in `datasets.yaml` — at_block, be_wal, ch, de_*,
ec_ro, es_ar, es_cl, es_cn, es_ib, es_md, fi, lt, lu, lv, nl_block, sk.
