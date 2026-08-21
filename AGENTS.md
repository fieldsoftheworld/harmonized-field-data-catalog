# Working in this repository

Developer and agent guide for `harmonized-field-data-catalog`. The published catalog has its own, separate guide at `catalog/AGENTS.md` (generated).

## The two boundaries

**`catalog/` is the published catalog.** Everything in it is synced 1:1 to `s3://ftw/harmonized-field-data/` by `tools/publish.py`, and nothing outside it ever is. Do not move a file into `catalog/` to make it publish, and do not widen the walk in `publish.py`. Data files are gitignored (`*.parquet`, `*.pmtiles`); locally they appear under `catalog/` only as symlinks into `staging/`, created by `catalogize.py` so the link gate can resolve them. They are uploaded from `staging/` by `tools/upload_data.py`, which is scoped by directory (`year=*`, `latest`) and suffix.

**Conversion logic lives in fiboa-cli.** This repository never transforms data. If a column is mapped wrongly, a source URL moved, a license string is off, or a year is missing, the fix goes to `fiboa_cli/datasets/<id>.py` in [fiboa/cli](https://github.com/fiboa/cli); this repository only chooses what to publish (`datasets.yaml`) and wraps the converter's output in Portolan metadata.

## Edit the generator, not the output

`tools/catalogize.py` writes every file under `catalog/<id>/` and the root documents. A hand edit there is overwritten on the next build. Change the template code, the manifest, `tools/field_descriptions.yaml` (specification wording for fiboa columns, each with its source), or the upstream facts (converter, data survey).

Every sentence in the generated documentation is one of three kinds, and stays that way:

- **attested** — copied from the converter, the fiboa data survey, or the specification, with the link;
- **derived** — measured from the files while generating; the query is printed and its output follows as comments;
- nothing else. When a column has no documented meaning the text says so instead of guessing.

## Build, check, publish

```bash
pixi run python tools/build.py <id>        # fiboa publish → catalogize → thumbnail → catalogize
pixi run python tests/run_all.py           # manifest, links, publish contract, stac-check, rashid
pixi run rashid check catalog              # full pass incl. byte checks (CI runs --no-data)
pixi run python tools/upload_data.py <id> --confirm
pixi run python tools/publish.py --confirm
pixi run rashid check catalog --live --live-base-url https://data.source.coop/ftw/harmonized-field-data
```

Look at every thumbnail you generate. `thumbnail.py`'s blank-probe gate only proves that some data landed in the frame.

## Rules that keep the gates honest

- `ACCEPTED` in `tests/test_conformance.py` is empty. Never add a rule there without a row in `docs/conformance.md` naming where it fires, why, and the tracking issue.
- `CI_LIGHT=1` (set in CI) lets `tests/test_links.py` skip hrefs to data files that are not in git; it skips nothing else and prints how many it skipped. Run the gates without it locally, with `staging/` populated.
- `stac-check` is advisory, `rashid` is the gate. Do not add a `self` link to silence stac-check; Portolan forbids it.
- Pin `rashid` identically in `pyproject.toml` and `.github/workflows/ci.yml`.
- Commit metadata changes with the build that produced them; a collection whose `updated` or checksums disagree with the bucket is a conformance failure.

## Publishers and state

Two publishers exist in the Portolan world. This repository uses the template's stateless `tools/publish.py` (size + MD5 against the bucket listing), not `portolan push` and its `versions.json`. Content-type changes need `--force`, because a listing does not carry content types. Publishing never deletes: remove stale objects in the bucket deliberately.

## Pointing back at this repository

`catalog/catalog.json` carries `rel: vcs` and `rel: issues` links to this repository (absolute URLs). No `git:*` fields; the Portolan spec has not standardised them ([portolan-spec#145](https://github.com/portolan-sdi/portolan-spec/issues/145)).
