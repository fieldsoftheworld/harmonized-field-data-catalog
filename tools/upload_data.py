#!/usr/bin/env python3
"""Upload a dataset's data files from staging/ to the bucket.

``tools/publish.py`` syncs ``catalog/`` and nothing else — that boundary keeps
scratch out of the public bucket, so it is not widened here. Data files are
too large for git; they live only in ``staging/`` and are uploaded by this
script into the *same* prefix, beside the metadata that describes them:

    staging/<id>/year=<Y>/<id>-<Y>.parquet  ->  <write_prefix>/<id>/year=<Y>/<id>-<Y>.parquet
    staging/<id>/year=<Y>/<id>-<Y>.pmtiles  ->  <write_prefix>/<id>/year=<Y>/<id>-<Y>.pmtiles
    staging/<id>/latest/<id>.parquet        ->  <write_prefix>/<id>/latest/<id>.parquet

Scope is an allow-list of suffixes (``ALLOWED``) under an allow-list of
directories (``year=*`` and ``latest``). ``collection.json``, ``converter.json``
and anything else in staging never upload from here; the STAC comes from
``catalog/`` through publish.py.

    python tools/upload_data.py nl             # dry run: per-suffix breakdown
    python tools/upload_data.py nl --confirm   # upload (source-coop login first)
    python tools/upload_data.py --all --confirm

Change detection, content types, the sentinel guard and the S3 client are
imported from publish.py so the two uploaders cannot drift.
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from collections import Counter

from common import STAGING_DIR, Manifest
from publish import (
    Upload,
    content_type_for,
    is_unchanged,
    load_config,
    remote_index,
    s3_client,
    split_s3_uri,
    unedited_sentinels,
)

ALLOWED = (".parquet", ".pmtiles")
DIR_PATTERN = re.compile(r"^(year=\d{4}|latest)$")

# The Source Cooperative proxy answers a part upload with a 520 now and then. It is
# not in botocore's retryable set, so without this one bad part ends a batch that
# takes hours, having already paid for the transfer of everything before it.
UPLOAD_ATTEMPTS = 5


def collect(dataset_id: str, prefix: str) -> list[Upload]:
    base = STAGING_DIR / dataset_id
    if not base.is_dir():
        sys.exit(f"no staging directory for {dataset_id}: {base}")
    uploads = []
    for path in sorted(base.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        rel = path.relative_to(base)
        if len(rel.parts) != 2 or not DIR_PATTERN.match(rel.parts[0]):
            continue
        if path.suffix.lower() not in ALLOWED:
            continue
        key = "/".join(p for p in (prefix, dataset_id, rel.as_posix()) if p)
        uploads.append(Upload(path, key, content_type_for(path)))
    return uploads


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("datasets", nargs="*")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--confirm", action="store_true", help="actually upload")
    parser.add_argument("--force", action="store_true", help="re-upload everything")
    args = parser.parse_args()

    config = load_config()
    stale = unedited_sentinels(config)
    if stale:
        print("catalog.publish.yaml still carries template values: " + ", ".join(stale))
        return 1
    manifest = Manifest.load()
    ids = list(manifest.datasets) if args.all else args.datasets
    if not ids:
        parser.error("name a dataset or pass --all")

    bucket, prefix = split_s3_uri(config["write_prefix"])
    uploads: list[Upload] = []
    for dataset_id in ids:
        if dataset_id not in manifest.datasets:
            sys.exit(f"{dataset_id} is not in datasets.yaml")
        uploads += collect(dataset_id, prefix)

    by_suffix = Counter()
    size_by_suffix = Counter()
    for u in uploads:
        by_suffix[u.local.suffix] += 1
        size_by_suffix[u.local.suffix] += u.local.stat().st_size
    print(f"target: s3://{bucket}/{prefix} via {config.get('endpoint_url') or 'default endpoint'} (profile {config.get('profile') or 'default'})")
    for suffix, n in sorted(by_suffix.items()):
        print(f"  {suffix:9s} {n:4d} file(s)  {size_by_suffix[suffix] / 1e9:8.2f} GB")
    print(f"  total     {len(uploads):4d} file(s)  {sum(size_by_suffix.values()) / 1e9:8.2f} GB")

    index = {} if args.force else remote_index(bucket, prefix, config)
    changed = [u for u in uploads if args.force or not is_unchanged(u, index)]
    print(f"{len(changed)} to upload, {len(uploads) - len(changed)} unchanged")
    print("this never deletes; removing a file from staging does not unpublish it")
    if not args.confirm:
        for u in changed[:30]:
            print(f"  would upload  {u.key}  ({u.local.stat().st_size / 1e6:.1f} MB)")
        if len(changed) > 30:
            print(f"  ... and {len(changed) - 30} more")
        print("\ndry run. re-run with --confirm to upload.")
        return 0
    if not changed:
        print("nothing to upload")
        return 0

    from boto3.s3.transfer import TransferConfig

    client = s3_client(config)
    transfer = TransferConfig(multipart_threshold=64 * 1024 * 1024, multipart_chunksize=64 * 1024 * 1024, max_concurrency=8)
    failed = []
    for u in changed:
        print(f"  uploading  {u.key}  ({u.local.stat().st_size / 1e6:.1f} MB)", flush=True)
        for attempt in range(1, UPLOAD_ATTEMPTS + 1):
            try:
                client.upload_file(str(u.local), bucket, u.key, ExtraArgs={"ContentType": u.content_type}, Config=transfer)
                break
            except Exception as e:
                if attempt == UPLOAD_ATTEMPTS:
                    # Keep going: the files after this one are independent, and a
                    # re-run skips whatever landed, by checksum.
                    print(f"  FAILED     {u.key}: {e}", flush=True)
                    failed.append(u.key)
                    break
                wait = min(2**attempt * 5, 120)
                print(f"  retry {attempt}/{UPLOAD_ATTEMPTS - 1} in {wait}s  ({str(e)[:120]})", flush=True)
                time.sleep(wait)

    print(f"\nuploaded {len(changed) - len(failed)} file(s)")
    if failed:
        print(f"{len(failed)} file(s) failed after {UPLOAD_ATTEMPTS} attempts; re-run to retry them:")
        for key in failed:
            print(f"  {key}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
