#!/usr/bin/env bash
# Pre-download source files into cache/ so `fiboa publish` finds them.
#
# vecorel-cli's downloader gives up after ~300 s, which multi-GB sources and
# slow servers exceed, and it keeps the truncated file. This fetches each
# file resumably with stall detection and retries, writing to <name>.part
# and moving it into place only when complete.
#
#   tools/prefetch.sh staging/logs/prefetch.tsv     # lines: <cache name>\t<url>
#
# Cache names are what vecorel-cli derives: the URL's basename, or the name a
# converter gives in its sources/variants dict (tools/converter_meta.py shows
# the URLs; the name rule is vecorel_cli.vecorel.util.name_from_uri).
set -u
cd "$(dirname "$0")/.."
mkdir -p cache
[ -f "${1:-}" ] || { echo "FAILED: input list ${1:-<missing>} does not exist"; exit 1; }
while IFS=$'\t' read -r name url; do
  [ -z "${name:-}" ] && continue
  case "$name" in \#*) continue;; esac
  if [ -s "cache/$name" ] && [ ! -f "cache/$name.part" ]; then echo "have    $name"; continue; fi
  echo "$(date +%T) fetch   $name"
  ok=0
  for attempt in $(seq 1 40); do
    if curl -sS -L -C - --http1.1 --speed-limit 10000 --speed-time 120 --connect-timeout 30 \
         -o "cache/$name.part" "$url"; then ok=1; break; fi
    rc=$?
    if [ "$rc" = 33 ]; then  # server does not support byte ranges: start over
      echo "$(date +%T) restart $name (no range support)"; rm -f "cache/$name.part"
    fi
    echo "$(date +%T) retry   $name (attempt $attempt, rc $rc, $(wc -c < "cache/$name.part" 2>/dev/null || echo 0) bytes)"
    sleep 15
  done
  if [ "$ok" = 1 ]; then mv -f "cache/$name.part" "cache/$name"; echo "$(date +%T) done    $name $(wc -c < "cache/$name") bytes"
  else echo "$(date +%T) FAILED  $name"; fi
done < "${1:?usage: prefetch.sh <tsv>}"
echo PREFETCH_DONE
