# Portolan Conformance

Conformance means passing [rashid](https://github.com/portolan-sdi/rashid),
not claiming to conform, so it runs in CI:

```bash
python3 tests/test_conformance.py
```

That gate fails on any error-severity finding whose rule is not listed below.
The list starts empty and it must never grow without a row here. A known
deviation with an issue number is a debt someone can pay off. A silently
widened allow-list is a false claim about what this catalog conforms to.

This file also records workarounds for the other validator CI runs. Those are
not conformance debts, because the catalog is correct and the validator is not.
They live here so nobody has to read CI code to find out why a gate skips
something.

## Accepted deviations

None. (`ACCEPTED` in `tests/test_conformance.py` only gates error-severity
findings; the warnings below are not blocking and need no waiver.)

## Notes on the current rashid run

- **Fan-out (`PTL-CAT-001`, warning, pre-existing since v0.1.2)**: the root
  catalog (79 children) and the `ch` (40) and `nl` (22) collections exceed
  the twenty-child guideline for subcatalog grouping (`PORTO-CORE-078`).
  Restructuring a flat catalog of this size into thematic subcatalogs is a
  user-visible change to every collection's URL and is explicitly a
  checkpoint in the migration guidance, not a Portolan v0.3.0 delta item.
  Left for a maintainer decision; tracked as a follow-up rather than fixed
  in the v0.3.0 migration.
- **Partition data checks are not run locally**: every collection's
  `partition:glob` is an absolute `s3://` URL (already compliant with the
  v0.3.0 `PORTO-FMT-064` requirement). `rashid check catalog --no-data`
  cannot list or read those partitions from a local relative tree, so a
  clean local run says nothing about `PTL-DAT-*` row-group, schema, or
  spatial-order checks on the data itself. Those only run against the
  published catalog with `rashid check <url> --live` (or
  `--live-base-url`), which needs the data on Source Cooperative and is out
  of scope for a metadata-only migration PR.

<!--
When you accept one, add a row and a section explaining it, like this:

| Rule | Where | Why accepted | Tracking |
|---|---|---|---|
| PTL-VIZ-001 | all thumbnails | WebP is not yet permitted; the size saving is 4x | portolan-spec#121 |

Then add the rule id to ACCEPTED in tests/test_conformance.py. Both, or
neither.
-->

## Validator workarounds

### Data hrefs are not checked in CI

`tests/test_links.py` resolves every relative href against the working tree. Data
files (`*.parquet`, `*.pmtiles`) are gitignored, so a clean checkout in CI has the
metadata but not the bytes. With `CI_LIGHT=1` (set in `.github/workflows/ci.yml`)
the gate skips hrefs with those two suffixes, counts them, and prints the count.
Everything else is still checked. Run the gates locally without `CI_LIGHT`, with
`staging/` populated, before publishing.


### stac-check reports a dialect crash on every collection

`tests/test_stac_valid.py` exempts one stac-check failure:

```
'list' object has no attribute 'get'
[Schema: https://schemas.portolan-sdi.org/portolan/vX.Y.Z/schema.json]. Error in Extensions.
```

The Portolan schema is valid draft-07, and rashid validates catalogs against it
cleanly. `stac-validator`, which stac-check uses, hardcodes the JSON Schema
2020-12 dialect and ignores the `$schema` a schema declares. The profile schema
uses the draft-07 tuple form of `items` in `valid_bbox`, which means something
different under 2020-12, so the library raises instead of validating.

Tracked upstream at <https://github.com/stac-utils/stac-check/issues/159>,
and on the Portolan side at
<https://github.com/portolan-sdi/portolan-spec/issues/157>.

The exemption matches that exact message, and only when the failing schema is a
Portolan profile schema. Every other stac-check error still fails the build,
and the gate prints how many objects took the exemption.

The exemption expires on its own. The gate fails once stac-check stops emitting
the crash on a collection or item that declares the profile schema, and tells
you to delete both the exemption and this section. CI installs stac-check
unpinned, so the next release triggers that without anyone watching for it.
