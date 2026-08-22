#!/usr/bin/env bash
# Build many datasets one after another, never stopping on a failure.
#
#   tools/batch.sh lu es_cn de_sh ...      # build each (fiboa publish → catalogize → thumbnail)
#   BATCH_UPLOAD=1 tools/batch.sh ...      # and upload each dataset's data when it succeeds
#
# Per-dataset logs go to staging/logs/<id>.log; a one-line verdict per dataset
# to staging/logs/batch.tsv. Safe to re-run: build.py reuses existing staging
# files. Needs FIBOA_CMD / FIBOA_PYTHON when fiboa-cli is not on PATH.
set -u
cd "$(dirname "$0")/.."
mkdir -p staging/logs
for id in "$@"; do
  start=$(date +%s)
  if pixi run python tools/build.py "$id" > "staging/logs/$id.log" 2>&1; then
    verdict=ok
    if [ "${BATCH_UPLOAD:-0}" = "1" ]; then
      pixi run python tools/upload_data.py "$id" --confirm >> "staging/logs/$id.log" 2>&1 && verdict=uploaded || verdict=upload-failed
    fi
  else
    verdict=FAILED
  fi
  printf '%s\t%s\t%ss\t%s\n' "$id" "$verdict" "$(( $(date +%s) - start ))" "$(date -u +%FT%TZ)" | tee -a staging/logs/batch.tsv
done
